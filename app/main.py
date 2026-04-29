from GeekyAnts.app.api import agent, basic_llm
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
from GeekyAnts.app.api import rag

app = FastAPI(
    title="GeekyAnts LLM Showcase API",
    description="API showcasing LLM usage, RAG pipeline, and LangChain Agents.",
    version="1.0.0"
)

# CORS Middleware (allowing all origins for demo purposes)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global Exception Handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"message": "An unexpected error occurred.", "details": str(exc)},
    )

# Include Routers
app.include_router(basic_llm.router, prefix="/api")
app.include_router(rag.router, prefix="/api")
app.include_router(agent.router, prefix="/api")

# Mount static files (frontend)
frontend_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend")
if os.path.exists(frontend_path):
    app.mount("/static", StaticFiles(directory=frontend_path), name="static")

@app.get("/")
async def root():
    """Serve the frontend or welcome message"""
    frontend_index = os.path.join(frontend_path, "index.html")
    if os.path.exists(frontend_index):
        return FileResponse(frontend_index, media_type="text/html")
    return {"message": "Welcome to the GeekyAnts LLM Showcase API. Visit /docs for the Swagger UI."}
