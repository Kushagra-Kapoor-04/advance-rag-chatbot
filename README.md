# 📚 Advanced RAG Chatbot

A powerful **Retrieval-Augmented Generation (RAG)** chatbot that allows you to upload PDF documents and ask questions about them. The chatbot uses **Mistral-7B** running locally via **Ollama** for fast, offline inference.

## ✨ Features

- **📄 PDF Upload**: Upload multiple PDF files
- **🔍 Smart Retrieval**: Finds relevant content from your documents
- **🤖 Local LLM**: Uses Mistral-7B via Ollama (no cloud API needed)
- **⚡ Fast**: Runs entirely on your machine
- **🔐 Private**: Your data never leaves your computer
- **💾 Caching**: Vector embeddings are cached for faster subsequent queries

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- 8GB+ RAM (for Mistral-7B)
- [Ollama](https://ollama.ai) installed

### Installation

1. **Clone/download the project**
```bash
cd "D:\FINAL PROJECTS\RAG-CHATBOT"
```

2. **Create virtual environment** (if not already created)
```bash
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Start Ollama** (in a new terminal)
```bash
ollama serve
```

5. **Pull Mistral model** (first time only, in another terminal)
```bash
ollama pull mistral
```

6. **Run the Streamlit app**
```bash
.\.venv\Scripts\streamlit.exe run app.py
```

7. **Open in browser**
Navigate to: `http://localhost:8501`

## 📖 How to Use

1. **Upload PDFs**: Use the file uploader to select one or more PDF files
2. **Wait for Processing**: PDFs are processed and embeddings are cached
3. **Ask Questions**: Type your question in the text input
4. **View Answer**: Get AI-generated answers based on your documents
5. **Check Sources**: Expand "Source Documents" to see which parts were used

## 🏗️ Project Structure

```
RAG-CHATBOT/
├── app.py                  # Streamlit UI
├── rag_pipeline.py         # RAG chain logic
├── llm_factory.py          # Ollama LLM initialization
├── embedding_manager.py    # Vector store (FAISS) management
├── prompt_templates.py     # Customizable prompts
├── config.py               # Configuration settings
├── utils.py                # Helper functions
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables (no secrets needed)
└── data/
    ├── uploads/            # Uploaded PDFs
    └── vector_cache/       # Cached embeddings
```

## ⚙️ Configuration

Edit `config.py` to customize:
- **CHUNK_SIZE**: Size of text chunks (default: 1000)
- **CHUNK_OVERLAP**: Overlap between chunks (default: 200)
- **TOP_K**: Number of relevant documents to retrieve (default: 3)
- **EMBEDDING_MODEL**: HuggingFace embedding model

Edit `prompt_templates.py` to customize system prompts.

## 🔧 Troubleshooting

### "Ollama is not running"
**Solution**: Start Ollama in a new terminal:
```bash
ollama serve
```

### "Mistral model not found"
**Solution**: Pull the model:
```bash
ollama pull mistral
```

### "Read timeout" errors
**Solution**: Mistral is slow on CPU. It can take 30-60 seconds per response.
- For faster responses, try: `ollama pull neural-chat`
- Or use: `ollama pull llama2:7b`

Update `llm_factory.py` line 36 with the new model name.

### Large PDFs taking too long
**Solution**: The app limits context to 1000 characters per query to avoid timeouts. This is by design for reasonable response times.

## 📊 Response Quality vs Speed

| Model | Speed | Quality | RAM |
|-------|-------|---------|-----|
| neural-chat | ⚡⚡⚡ Fast | ⭐⭐⭐ Good | 7GB |
| mistral | ⚡⚡ Medium | ⭐⭐⭐⭐ Excellent | 8GB |
| llama2:7b | ⚡⚡ Medium | ⭐⭐⭐ Good | 8GB |

## 🔐 Privacy & Security

- ✅ Runs 100% offline
- ✅ No API keys required
- ✅ PDFs processed locally
- ✅ No data sent to external servers

## 🛠️ Architecture

```
PDF Upload
    ↓
PDF Parsing (PyPDF)
    ↓
Text Chunking
    ↓
Embeddings (sentence-transformers)
    ↓
Vector Store (FAISS) → Cached
    ↓
User Query
    ↓
Retrieval (Find top-3 similar chunks)
    ↓
Prompt Formatting
    ↓
LLM Generation (Mistral via Ollama)
    ↓
Response Display
```

## 📝 Answer Styles

Choose from 5 different answer styles:
- **Short and concise**: Quick, focused answers
- **Detailed explanation**: In-depth, comprehensive answers
- **Exam-oriented with examples**: Educational format with examples
- **Bullet points**: Organized, scannable format
- **Teach me like a beginner**: Simple, easy-to-understand explanations

## 🚀 Performance Tips

1. **Smaller PDFs**: Process faster
2. **Specific questions**: Get better answers
3. **Short answer style**: Faster responses
4. **GPU usage**: Install CUDA for faster processing (advanced)

## 📦 Dependencies

- `streamlit`: Web UI
- `langchain`: RAG framework
- `sentence-transformers`: Embeddings
- `faiss-cpu`: Vector database
- `pypdf`: PDF parsing
- `requests`: Ollama API calls

## 🐛 Known Issues

- Mistral can be slow on CPU (30-60 seconds per query)
- Very large PDFs may have truncated context
- Some PDF formats may not parse correctly

## 📄 License

Use freely for personal projects.

Live Demo
https://advance-rag-chatbot.streamlit.app/

