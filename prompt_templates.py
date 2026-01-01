from langchain_core.prompts import PromptTemplate


def get_prompt(style):
    # Different prompts based on answer style
    if style == "Short and concise":
        prompt_instruction = "Provide a brief, direct answer in 2-3 sentences."
    elif style == "Detailed explanation":
        prompt_instruction = "Provide a comprehensive explanation with all relevant details. Reorganize the information logically without preserving arbitrary labels like 'Part 1', 'Part 2', etc."
    elif style == "Exam-oriented with examples":
        prompt_instruction = "Provide an educational answer with examples. Structure it clearly but use natural language, not document labels."
    elif style == "Bullet points":
        prompt_instruction = "Provide key points in bullet format. Use meaningful bullet points, not document labels."
    elif style == "Teach me like a beginner":
        prompt_instruction = "Explain as if teaching a beginner. Use simple language and avoid technical jargon or document numbering."
    else:
        prompt_instruction = "Provide a clear, well-organized answer."
    
    return PromptTemplate(
        template=f"""You are a helpful assistant that answers questions ONLY based on the provided document content.

Answer style: {style}
Instructions: {prompt_instruction}

CRITICAL RULES:
1. ONLY use information from the Context section below
2. If the answer is not in the Context, MUST say: "Not available in the provided document"
3. Do NOT use any external knowledge or assumptions
4. Reorganize and rephrase the information naturally - do NOT preserve arbitrary document labels like "Part 1", "Part 2", "Section A", etc.
5. Be clear, structured, and factual
6. Always cite which part of the document you're referencing when relevant

Context (from the uploaded document):
{{context}}

User Question:
{{question}}

Answer (ONLY from the context above, reorganized naturally):
""",
        input_variables=["context", "question"]
    )

