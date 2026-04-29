# GeekyAnts Installation Guide 📦

Complete step-by-step instructions to set up and run the GeekyAnts LLM Showcase application.

## 📋 Prerequisites

Before you begin, ensure you have:
- **Python 3.9 or higher** ([Download Python](https://www.python.org/downloads/))
- **pip** (Python package manager - comes with Python)
- **Git** (optional, for cloning the repository)
- **Anthropic API Key** ([Get API Key](https://console.anthropic.com/))
- **~500MB disk space** for dependencies and vector database

### Check Prerequisites

```bash
# Check Python version
python --version

# Check pip
pip --version
```

## 🔧 Installation Steps

### 1. Clone or Download the Repository

```bash
# Using Git
git clone <repository-url>
cd GeekyAnts

# Or download and extract the ZIP file
```

### 2. Create a Virtual Environment

A virtual environment isolates project dependencies from your system Python.

**On Windows (PowerShell):**
```powershell
# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\Activate.ps1
```

**On Windows (Command Prompt):**
```cmd
# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate.bat
```

**On macOS/Linux:**
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
source venv/bin/activate
```

### 3. Install Python Dependencies

```bash
# Upgrade pip first
pip install --upgrade pip

# Install all dependencies
pip install -r requirements.txt
```

**Installation Details:**
- FastAPI 0.110.0+ - Web framework
- Anthropic 0.25.0+ - LLM API client
- LangChain - LLM orchestration
- ChromaDB - Vector database
- Sentence Transformers - Embeddings
- PyPDF - PDF processing

### 4. Configure Environment Variables

Create a `.env` file in the project root:

```bash
# Windows (PowerShell)
New-Item -Path ".env" -ItemType File

# macOS/Linux
touch .env
```

Edit `.env` and add:
```
ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxxxxxxxxx
LOG_LEVEL=INFO
```

**Get your API Key:**
1. Visit [console.anthropic.com](https://console.anthropic.com/)
2. Sign in or create an account
3. Go to API keys section
4. Create a new API key
5. Copy and paste into `.env`

### 5. Create Required Directories

```bash
# These directories may need to exist for uploads
mkdir data
mkdir data/uploads
mkdir data/chroma
```

Or using Python:
```bash
python -c "import os; os.makedirs('data/uploads', exist_ok=True); os.makedirs('data/chroma', exist_ok=True)"
```

### 6. Verify Installation

Test that everything is set up correctly:

```bash
# Test Python imports
python -c "import fastapi; import langchain; import chromadb; print('✓ All packages installed successfully')"
```

## 🚀 Running the Application

### Method 1: Using PowerShell Script (Recommended for Windows)

```powershell
# Windows PowerShell
.\run-geekyants.ps1
```

### Method 2: Manual Start (All Platforms)

```bash
# Make sure virtual environment is activated
# (venv) should be visible in your terminal prompt

# Start the FastAPI server
python -m uvicorn app.main:app --reload
```

### Method 3: Using Uvicorn Directly

```bash
# With auto-reload on code changes
uvicorn app.main:app --reload

# Specific port (if 8000 is in use)
uvicorn app.main:app --reload --port 8001

# Production mode (no reload)
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## 🌐 Access the Application

Once the server is running, open your browser and visit:

```
http://localhost:8000
```

### Login Credentials

Default credentials for initial access:
- **Username**: `admin`
- **Password**: `secretpassword`

## ✅ Verification Checklist

After installation, verify:

- [ ] Python version 3.9+
- [ ] Virtual environment created and activated
- [ ] All dependencies installed without errors
- [ ] `.env` file created with valid `ANTHROPIC_API_KEY`
- [ ] Data directories exist (`data/uploads`, `data/chroma`)
- [ ] Server starts without errors
- [ ] Browser can access `http://localhost:8000`
- [ ] Login works with default credentials
- [ ] Frontend loads properly (styling visible)

## 🔍 First-Time Testing

### 1. Test LLM Generation
1. Login with default credentials
2. Go to the "LLM Generation" section
3. Enter a prompt (e.g., "Hello, who are you?")
4. Click "Generate"
5. Verify response appears

### 2. Test RAG Pipeline
1. Use the "Upload PDF" feature
2. Select a PDF file or use `create_sample_pdf.py`
3. Upload the PDF
4. Wait for processing to complete
5. Query the document
6. Verify search results

### 3. Check Logs
- Look for `server.err.log` for any errors
- Check console output for startup messages

## 🛠️ Troubleshooting

### Python not found
```bash
# Ensure Python is in PATH
# Try using python3 instead
python3 --version
python3 -m venv venv
```

### Virtual environment activation fails
```bash
# On Windows, if PowerShell scripts are disabled
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Or use cmd.exe instead of PowerShell
venv\Scripts\activate.bat
```

### Pip install fails
```bash
# Upgrade pip and setuptools
pip install --upgrade pip setuptools wheel

# Try installing with --no-cache-dir
pip install --no-cache-dir -r requirements.txt
```

### Port 8000 already in use
```bash
# Find and kill the process using port 8000
# Windows
netstat -ano | findstr :8000

# macOS/Linux
lsof -i :8000

# Or use a different port
python -m uvicorn app.main:app --reload --port 8001
```

### ANTHROPIC_API_KEY not found
```bash
# Check .env file exists and has the key
cat .env  # macOS/Linux
type .env  # Windows

# Ensure the variable is set (should print your key)
echo $env:ANTHROPIC_API_KEY  # PowerShell
echo %ANTHROPIC_API_KEY%     # Command Prompt
```

### Chroma database errors
```bash
# Clear Chroma cache if needed
rm -r data/chroma  # macOS/Linux
rmdir /s data\chroma  # Windows

# The directory will be recreated automatically
```

### Server crashes on startup
1. Check `server.err.log` for error messages
2. Verify all dependencies are installed: `pip list | grep fastapi`
3. Verify `.env` file is valid
4. Check that port 8000 is available

## 📦 Creating Sample PDFs

To test the RAG pipeline with sample data:

```bash
python create_sample_pdf.py
```

This creates test PDF files in `data/uploads/` that you can use to test document upload and querying.

## 📚 Next Steps

After successful installation:

1. **Read the Documentation**
   - Review [FRONTEND_GUIDE.md](FRONTEND_GUIDE.md) for UI features
   - Check [README.md](README.md) for project overview

2. **Explore Features**
   - Test each section of the application
   - Experiment with different prompts
   - Upload various PDFs to test RAG

3. **Configuration**
   - Adjust API parameters in the UI
   - Set temperature and token limits
   - Customize system prompts

4. **Development**
   - Explore the code structure in `app/` directory
   - Modify endpoints in `app/api/`
   - Enhance the frontend in `frontend/`

## 🆘 Getting Help

If you encounter issues:

1. **Check Logs**
   - Review `server.err.log`
   - Check console output for error messages

2. **Verify Setup**
   - Re-run the prerequisites checklist
   - Ensure `.env` file is correct
   - Confirm virtual environment is activated

3. **Restart Clean**
   ```bash
   # Deactivate and reactivate virtual environment
   deactivate
   ./venv/Scripts/Activate.ps1  # Windows PowerShell
   source venv/bin/activate      # macOS/Linux
   
   # Reinstall dependencies
   pip install --force-reinstall -r requirements.txt
   ```

4. **Internet Connection**
   - Verify internet is working
   - Check Anthropic API is accessible
   - Ensure firewall isn't blocking requests

## 📞 Support Resources

- **Anthropic Documentation**: https://docs.anthropic.com/
- **FastAPI Docs**: https://fastapi.tiangolo.com/
- **LangChain Docs**: https://python.langchain.com/
- **ChromaDB Docs**: https://docs.trychroma.com/

---

**Installation Complete!** 🎉

You're now ready to explore GeekyAnts. Happy coding! 🚀
