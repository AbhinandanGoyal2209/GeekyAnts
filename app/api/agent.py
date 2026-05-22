from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from app.api.dependencies import verify_credentials

router = APIRouter(prefix="/agent", tags=["LangChain Agents"], dependencies=[Depends(verify_credentials)])

class AgentRequest(BaseModel):
    question: str

class AgentResponse(BaseModel):
    answer: str

@router.post("/chat", response_model=AgentResponse)
async def chat_with_agent(request: AgentRequest):
    """
    Interact with the ReAct LangChain agent.
    The agent has access to a DuckDuckGo Search tool and a Calculator tool.
    It will autonomously decide which tool to use to answer the question.
    """
    try:
        from app.services.agent_service import agent_service
        result = agent_service.run_agent(request.question)
        return AgentResponse(answer=result["output"])
    except ImportError as e:
        raise HTTPException(status_code=503, detail=f"Agent dependencies are not installed: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Agent failed to execute: {str(e)}")
