# GeekyAnts - LLM Showcase Application 🚀
Live Application Link: https://geekyants-c6qb.onrender.com/

A modern, full-stack application demonstrating advanced Large Language Model (LLM) capabilities with a beautiful responsive frontend and powerful backend powered by FastAPI.

#Screenshots
<img width="1887" height="900" alt="image" src="https://github.com/user-attachments/assets/9f50e8e7-9045-4424-96bb-05b9a4eab3af" />

<img width="1627" height="808" alt="image" src="https://github.com/user-attachments/assets/345595af-cb5c-4f41-821d-cf6781e862e5" />

<img width="1503" height="808" alt="image" src="https://github.com/user-attachments/assets/1f2fb16f-c10a-432e-8ff4-399360751e50" />

<img width="501" height="569" alt="image" src="https://github.com/user-attachments/assets/bddddbb8-81c3-49b1-a60b-fc2097c98c1c" />

## 🎯 What is GeekyAnts?

GeekyAnts is a showcase application that combines:
- **LLM Integration**: Direct integration with Claude (Anthropic API)
- **Retrieval-Augmented Generation (RAG)**: Query and analyze uploaded PDF documents
- **LangChain Agents**: Intelligent agents for complex task automation
- **Modern Frontend**: Responsive web interface with real-time features
- **Vector Database**: Chroma-based vector storage for semantic search

## ✨ Key Features

### 🔑 Authentication
- Secure login system with token-based sessions
- Default credentials: `admin` / `secretpassword`
- User session management

### 💬 LLM Text Generation
- Real-time text generation using Claude 3.5
- Customizable system prompts
- Temperature and token limit controls
- Token usage statistics
- Response history tracking

### 📄 RAG Pipeline
- Drag-and-drop PDF upload interface
- Automatic document chunking and embedding
- Vector similarity search over documents
- Query results with source citations
- Support for multiple documents

### 🤖 LangChain Agents
- Agent-based task execution
- Multi-step reasoning capabilities
- Tool integration for extended functionality

### 🎨 Modern UI
- Beautiful dark theme with gradient accents
- Fully responsive design (mobile, tablet, desktop)
- Smooth animations and transitions
- Professional card-based layout
- Real-time feedback and error handling

## 🛠️ Technology Stack

### Backend
- **Framework**: FastAPI 0.110.0+
- **LLM Provider**: Anthropic (Claude)
- **RAG Framework**: LangChain + LangChain Community
- **Vector Database**: ChromaDB
- **Embeddings**: Sentence Transformers
- **Document Processing**: PyPDF
- **Data Validation**: Pydantic

### Frontend
- **HTML5** - Semantic markup
- **CSS3** - Modern styling with gradients and animations
- **JavaScript (Vanilla)** - Interactive functionality
- **REST API** - Communication with backend

### Additional Libraries
- Python Multipart - File uploads
- DuckDuckGo Search - Web search integration
- Numexpr - Numerical expression evaluation
- Python Dotenv - Environment configuration

## 📁 Project Structure

```
GeekyAnts/
├── app/
│   ├── main.py              # FastAPI application entry point
│   ├── api/
│   │   ├── agent.py         # Agent endpoints
│   │   ├── basic_llm.py     # LLM generation endpoints
│   │   ├── rag.py           # RAG pipeline endpoints
│   │   └── dependencies.py  # Shared dependencies
│   ├── core/
│   │   └── config.py        # Configuration settings
│   └── services/
│       ├── agent_service.py # Agent service logic
│       └── rag_service.py   # RAG service logic
├── frontend/
│   ├── index.html           # Main HTML template
│   ├── main.js              # Frontend logic
│   └── styles.css           # Styling
├── data/
│   ├── chroma/              # Vector database storage
│   └── uploads/             # Uploaded PDF files
├── requirements.txt         # Python dependencies
├── create_sample_pdf.py     # Utility to create sample PDFs
└── run-geekyants.ps1       # PowerShell startup script
```

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- pip (Python package manager)
- An Anthropic API key

### Installation
See [INSTALL.md](INSTALL.md) for detailed setup instructions.

### Running the Application
```bash
# Windows
.\run-geekyants.ps1

# Or manually
python -m uvicorn app.main:app --reload
```

Access the application at: `http://localhost:8000`

## 📋 API Endpoints

### LLM Generation
- `POST /api/generate` - Generate text using LLM

### RAG Pipeline
- `POST /api/upload-pdf` - Upload and process PDF
- `POST /api/query-rag` - Query uploaded documents
- `GET /api/documents` - List uploaded documents

### Agents
- `POST /api/agent/run` - Execute agent task

## 🔒 Environment Configuration

Create a `.env` file in the project root:
```
ANTHROPIC_API_KEY=your_api_key_here
LOG_LEVEL=INFO
```

## 📚 Documentation

- [FRONTEND_GUIDE.md](FRONTEND_GUIDE.md) - Frontend setup and features
- [FRONTEND_COMPLETE.md](FRONTEND_COMPLETE.md) - Complete frontend documentation
- [INSTALL.md](INSTALL.md) - Detailed installation instructions

## 🐛 Troubleshooting

### Port 8000 already in use
```bash
python -m uvicorn app.main:app --reload --port 8001
```

### PDF upload fails
- Ensure `data/uploads/` directory exists
- Check file permissions
- Verify PDF is not corrupted

### LLM requests timeout
- Check Anthropic API key is valid
- Verify internet connection
- Check API rate limits

## 📞 Support

For issues or questions:
1. Check the documentation files
2. Review the frontend guides
3. Check application logs in `server.err.log`

## 📄 License

This project is a showcase application for LLM capabilities.

## 🎓 Learning Resources

This project demonstrates:
- Modern FastAPI application structure
- RAG pipeline implementation
- LangChain integration
- Vector database usage
- Frontend-backend integration
- Token-based authentication
- Error handling and logging

---

**Happy exploring with GeekyAnts!** 🐜✨
