# 📄 LastMin

An offline GUI tool that lets you **query any PDF and text like ChatGPT for last minute endsem preparation**, powered by local LLMs and vector embeddings.  
No internet required — your data stays completely private.

---

## 🔥 Features

- 🍃 **100% Offline** — runs without internet  
- 🧠 Ask questions directly from the PDF or Text Files
- 📚 Uses embeddings + vector search (RAG)  
- ⚡ Fast semantic search across large documents  
- 🤖 Works with local LLMs like **Llama3, Mistral, Gemma, etc.** via Ollama  
- 🔐 Privacy-friendly: PDF never leaves your device


## 🏗️ Tech Stack

| Component | Technology |
|----------|------------|
| PDF Text Extraction | PyPDFLoader / PyPDF2 |
| Embeddings | Ollama (nomic-embed-text) |
| Vector DB | Chroma |
| Local LLM | Ollama (Llama3.1) |
| Pipeline | LangChain RAG |

## 📦 Installation

```bash
git clone https://github.com/yourusername/AskPDF-Offline.git
cd AskPDF-Offline
pip install -r requirements.txt
```
## Insalling LLM and EmbeddingModel
# Embedding Model (for vector search) (nomic-embed-text recommended)
# Primary LLM (choose any) (llama3.1 recommended)
```bash
ollama pull nomic-embed-text 
ollama pull llama3.1
```