import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

def create_pdf(filename):
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter
    
    c.setFont("Helvetica-Bold", 16)
    c.drawString(100, height - 80, "GeekyAnts Interview Guide")
    
    c.setFont("Helvetica", 12)
    textobject = c.beginText(50, height - 120)
    
    content = [
        "Introduction to Large Language Models (LLMs)",
        "Large Language Models are advanced artificial intelligence systems designed to",
        "understand, generate, and interact with human language. They are built on",
        "transformer architectures and trained on massive datasets of text.",
        "",
        "What is Prompt Engineering?",
        "Prompt engineering is the practice of designing and refining inputs (prompts) to",
        "guide an LLM toward generating desired outputs. A well-crafted prompt can",
        "significantly improve the quality and accuracy of the model's response.",
        "",
        "Retrieval-Augmented Generation (RAG)",
        "RAG is an architecture that combines the reasoning capabilities of LLMs with",
        "external knowledge retrieval. Instead of relying solely on the model's internal",
        "training data, RAG retrieves relevant information from a separate database and",
        "provides it to the model as context. This helps reduce hallucinations.",
        "",
        "LangChain and Agents",
        "LangChain is a framework for developing applications powered by language models.",
        "It provides abstractions for chaining together different components. Agents in",
        "LangChain use LLMs to make decisions about which actions to take."
    ]
    
    for line in content:
        textobject.textLine(line)
        
    c.drawText(textobject)
    c.save()

os.makedirs("data", exist_ok=True)
create_pdf("data/sample.pdf")
print("Successfully created data/sample.pdf")
