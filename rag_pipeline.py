from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter


from config import CHUNK_SIZE, CHUNK_OVERLAP, TOP_K
from embedding_manager import get_vectorstore
from prompt_templates import get_prompt
from llm_factory import get_llm


def load_pdfs(file_paths):
    documents = []
    for path in file_paths:
        loader = PyPDFLoader(path)
        documents.extend(loader.load())
    return documents


def split_documents(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP
    )
    return splitter.split_documents(documents)


def build_qa_chain(file_paths, answer_style, llm_provider):
    documents = load_pdfs(file_paths)
    chunks = split_documents(documents)

    vectorstore = get_vectorstore(chunks, file_paths)
    retriever = vectorstore.as_retriever(search_kwargs={"k": TOP_K})

    llm = get_llm(llm_provider)
    prompt = get_prompt(answer_style)

    # Create a simple chain using the retriever and LLM
    class SimpleRAGChain:
        def __init__(self, retriever, llm, prompt):
            self.retriever = retriever
            self.llm = llm
            self.prompt = prompt
        
        def invoke(self, inputs):
            query = inputs.get("input") if isinstance(inputs, dict) else inputs
            docs = self.retriever.invoke(query)
            
            # Check if we have documents
            if not docs or len(docs) == 0:
                return {
                    "output_text": "No relevant documents found in the uploaded PDFs.",
                    "source_documents": []
                }
            
            # Limit context to keep response time reasonable
            # Use only the first 1000 chars of the most relevant document
            context = docs[0].page_content[:1000] if docs else ""
            
            # Format the prompt with context and question
            formatted_prompt = self.prompt.format(context=context, question=query)
            
            # Truncate to keep request fast (1500 chars ~= 500 tokens for Mistral)
            if len(formatted_prompt) > 1500:
                formatted_prompt = formatted_prompt[:1500]
            
            try:
                # Get response from LLM
                response = self.llm.invoke(formatted_prompt)
                
                # Handle response - should be a string
                if isinstance(response, str):
                    output_text = response.strip()
                else:
                    output_text = str(response).strip()
                
                if not output_text:
                    output_text = "Unable to generate a response."
                    
            except Exception as e:
                output_text = f"Error generating response: {str(e)}"
            
            return {
                "output_text": output_text,
                "source_documents": docs
            }
    
    return SimpleRAGChain(retriever, llm, prompt)
