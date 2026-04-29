// API Configuration
const API_BASE_URL = 'http://localhost:8000/api';
let authToken = localStorage.getItem('authToken') || null;
let isLoggedIn = !!authToken;

// Show Loading Spinner
function showLoading(show = true) {
    const spinner = document.getElementById('loadingSpinner');
    if (show) {
        spinner.classList.remove('hidden');
    } else {
        spinner.classList.add('hidden');
    }
}

// Show Section
function showSection(sectionId) {
    // Hide all sections
    document.querySelectorAll('.section').forEach(section => {
        section.classList.add('hidden');
    });

    // Show selected section
    const section = document.getElementById(sectionId);
    if (section) {
        section.classList.remove('hidden');
    }

    // Scroll to top
    window.scrollTo(0, 0);
}

// ========================
// Authentication
// ========================
async function handleLogin(event) {
    event.preventDefault();
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    const statusDiv = document.getElementById('authStatus');

    try {
        showLoading(true);
        
        // Create Basic Auth header
        const credentials = btoa(`${username}:${password}`);
        
        // Test authentication by making a request to protected endpoint
        const response = await fetch(`${API_BASE_URL}/llm/generate`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Basic ${credentials}`
            },
            body: JSON.stringify({
                prompt: 'test',
                system_prompt: 'You are a helpful assistant.',
                temperature: 0.7,
                max_tokens: 10
            })
        });

        if (response.status === 401) {
            throw new Error('Invalid credentials');
        }

        // Store credentials
        authToken = credentials;
        isLoggedIn = true;
        localStorage.setItem('authToken', credentials);

        statusDiv.className = 'auth-status success';
        statusDiv.textContent = '✓ Login successful! Redirecting...';

        setTimeout(() => {
            showSection('home');
        }, 1500);

        showLoading(false);
    } catch (error) {
        statusDiv.className = 'auth-status error';
        statusDiv.textContent = `✗ ${error.message}`;
        showLoading(false);
    }
}

// Helper: Make API Request with Auth
async function apiRequest(endpoint, method = 'GET', body = null) {
    if (!isLoggedIn) {
        throw new Error('Please login first');
    }

    const options = {
        method,
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Basic ${authToken}`
        }
    };

    if (body) {
        options.body = JSON.stringify(body);
    }

    const response = await fetch(`${API_BASE_URL}${endpoint}`, options);

    if (response.status === 401) {
        isLoggedIn = false;
        localStorage.removeItem('authToken');
        showSection('auth');
        throw new Error('Session expired. Please login again.');
    }

    if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'API Error');
    }

    return await response.json();
}

// ========================
// LLM Section
// ========================
document.getElementById('llmForm')?.addEventListener('submit', async (e) => {
    e.preventDefault();

    const systemPrompt = document.getElementById('systemPrompt').value;
    const userPrompt = document.getElementById('userPrompt').value;
    const temperature = parseFloat(document.getElementById('temperature').value);
    const maxTokens = parseInt(document.getElementById('maxTokens').value);

    const responseDiv = document.getElementById('llmResponse');
    const statsDiv = document.getElementById('llmStats');

    try {
        showLoading(true);

        const data = await apiRequest('/llm/generate', 'POST', {
            prompt: userPrompt,
            system_prompt: systemPrompt,
            temperature,
            max_tokens: maxTokens
        });

        responseDiv.textContent = data.text;
        document.getElementById('promptTokens').textContent = data.input_tokens;
        document.getElementById('completionTokens').textContent = data.output_tokens;
        document.getElementById('totalTokens').textContent = data.total_tokens;
        
        statsDiv.classList.remove('hidden');

        showLoading(false);
    } catch (error) {
        responseDiv.textContent = `Error: ${error.message}`;
        statsDiv.classList.add('hidden');
        showLoading(false);
    }
});

// ========================
// RAG Section
// ========================
function handleDragOver(event) {
    event.preventDefault();
    event.stopPropagation();
    document.getElementById('uploadArea').classList.add('dragover');
}

function handleDrop(event) {
    event.preventDefault();
    event.stopPropagation();
    document.getElementById('uploadArea').classList.remove('dragover');

    const files = event.dataTransfer.files;
    if (files.length > 0) {
        document.getElementById('pdfFile').files = files;
        handleFileSelect({ target: { files } });
    }
}

function handleFileSelect(event) {
    const files = event.target.files;
    const uploadBtn = document.getElementById('uploadBtn');
    const statusDiv = document.getElementById('uploadStatus');

    if (files.length > 0) {
        const file = files[0];
        if (file.type === 'application/pdf') {
            uploadBtn.classList.remove('hidden');
            statusDiv.classList.add('hidden');
        } else {
            statusDiv.className = 'status-message error';
            statusDiv.textContent = '✗ Please select a PDF file';
            statusDiv.classList.remove('hidden');
            uploadBtn.classList.add('hidden');
        }
    }
}

async function uploadPDF() {
    const fileInput = document.getElementById('pdfFile');
    const file = fileInput.files[0];
    const statusDiv = document.getElementById('uploadStatus');

    if (!file) {
        statusDiv.className = 'status-message error';
        statusDiv.textContent = '✗ No file selected';
        statusDiv.classList.remove('hidden');
        return;
    }

    try {
        showLoading(true);

        const formData = new FormData();
        formData.append('file', file);

        const response = await fetch(`${API_BASE_URL}/rag/upload-pdf`, {
            method: 'POST',
            headers: {
                'Authorization': `Basic ${authToken}`
            },
            body: formData
        });

        if (response.status === 401) {
            isLoggedIn = false;
            localStorage.removeItem('authToken');
            showSection('auth');
            throw new Error('Session expired');
        }

        if (!response.ok) {
            throw new Error('Upload failed');
        }

        const data = await response.json();
        statusDiv.className = 'status-message success';
        statusDiv.textContent = `✓ PDF uploaded! ${data.chunks_added} chunks added to knowledge base`;
        statusDiv.classList.remove('hidden');

        fileInput.value = '';
        document.getElementById('uploadBtn').classList.add('hidden');

        showLoading(false);
    } catch (error) {
        statusDiv.className = 'status-message error';
        statusDiv.textContent = `✗ Error: ${error.message}`;
        statusDiv.classList.remove('hidden');
        showLoading(false);
    }
}

// Set upload button click handler
document.addEventListener('DOMContentLoaded', () => {
    const uploadBtn = document.getElementById('uploadBtn');
    if (uploadBtn) {
        uploadBtn.addEventListener('click', uploadPDF);
    }
});

async function queryRAG() {
    const query = document.getElementById('ragQuery').value;
    const responseDiv = document.getElementById('ragResponse');
    const responseText = document.getElementById('ragResponseText');

    if (!query.trim()) {
        responseText.textContent = 'Please enter a question';
        responseDiv.classList.remove('hidden');
        return;
    }

    try {
        showLoading(true);

        const data = await apiRequest('/rag/query', 'POST', {
            question: query
        });

        responseText.textContent = data.answer;
        responseDiv.classList.remove('hidden');

        showLoading(false);
    } catch (error) {
        responseText.textContent = `Error: ${error.message}`;
        responseDiv.classList.remove('hidden');
        showLoading(false);
    }
}

// ========================
// Agent Section
// ========================
async function sendAgentMessage() {
    const input = document.getElementById('agentInput');
    const message = input.value.trim();
    const chatBox = document.getElementById('chatBox');

    if (!message) return;

    // Add user message to chat
    const userMsgDiv = document.createElement('div');
    userMsgDiv.className = 'chat-message user';
    userMsgDiv.textContent = message;
    chatBox.appendChild(userMsgDiv);

    input.value = '';
    chatBox.scrollTop = chatBox.scrollHeight;

    try {
        showLoading(true);

        const data = await apiRequest('/agent/chat', 'POST', {
            question: message
        });

        // Add assistant message to chat
        const assistantMsgDiv = document.createElement('div');
        assistantMsgDiv.className = 'chat-message assistant';
        assistantMsgDiv.textContent = data.answer;
        chatBox.appendChild(assistantMsgDiv);

        chatBox.scrollTop = chatBox.scrollHeight;

        showLoading(false);
    } catch (error) {
        // Add error message to chat
        const errorMsgDiv = document.createElement('div');
        errorMsgDiv.className = 'chat-message assistant';
        errorMsgDiv.textContent = `Error: ${error.message}`;
        chatBox.appendChild(errorMsgDiv);

        chatBox.scrollTop = chatBox.scrollHeight;

        showLoading(false);
    }
}

// ========================
// Initialization
// ========================
window.addEventListener('DOMContentLoaded', () => {
    // Restore system prompt default
    const systemPrompt = document.getElementById('systemPrompt');
    if (systemPrompt) {
        systemPrompt.value = 'You are a helpful assistant.';
    }

    // Check if already logged in
    if (isLoggedIn) {
        showSection('home');
    } else {
        showSection('auth');
    }

    // Add enter key support for agent input
    const agentInput = document.getElementById('agentInput');
    if (agentInput) {
        agentInput.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                sendAgentMessage();
            }
        });
    }

    // Add enter key support for RAG query
    const ragQuery = document.getElementById('ragQuery');
    if (ragQuery) {
        ragQuery.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                queryRAG();
            }
        });
    }
});
