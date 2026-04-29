from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from pydantic import BaseModel
from GeekyAnts.app.api.dependencies import verify_credentials

router = APIRouter(prefix="/rag", tags=["RAG Pipeline"], dependencies=[Depends(verify_credentials)])

class QueryRequest(BaseModel):
    question: str

class QueryResponse(BaseModel):
    answer: str

@router.post("/ingest")
@router.post("/upload-pdf")
async def ingest_document(file: UploadFile = File(...)):
    """
    Upload a PDF document.
    The document will be chunked, embedded, and stored in the local ChromaDB.
    """
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")
    
    try:
        from GeekyAnts.app.services.rag_service import rag_service
        chunks_added = await rag_service.ingest_pdf(file)
        return {"message": f"Successfully ingested {file.filename}", "chunks_added": chunks_added}
    except ImportError as e:
        raise HTTPException(status_code=503, detail=f"RAG dependencies are not installed: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to ingest document: {str(e)}")

@router.post("/query", response_model=QueryResponse)
async def query_documents(request: QueryRequest):
    """
    Query the ingested documents using the RAG pipeline.
    """
    try:
        from GeekyAnts.app.services.rag_service import rag_service
        answer = rag_service.query(request.question)
        return QueryResponse(answer=answer)
    except ImportError as e:
        raise HTTPException(status_code=503, detail=f"RAG dependencies are not installed: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to query documents: {str(e)}")
