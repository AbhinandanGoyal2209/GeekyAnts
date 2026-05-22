from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from app.api.dependencies import verify_credentials
from app.core.config import settings

router = APIRouter(prefix="/llm", tags=["LLM Crash Course"], dependencies=[Depends(verify_credentials)])

class GenerateRequest(BaseModel):
    prompt: str
    system_prompt: str = "You are a helpful assistant."
    temperature: float = 0.7
    max_tokens: int = 500

class GenerateResponse(BaseModel):
    text: str
    input_tokens: int
    output_tokens: int
    total_tokens: int

def get_anthropic_client():
    try:
        import anthropic
    except ImportError as exc:
        raise HTTPException(
            status_code=503,
            detail="Anthropic SDK is not installed in the current Python environment.",
        ) from exc
    return anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)

@router.post("/generate", response_model=GenerateResponse)
async def generate_text(request: GenerateRequest):
    """
    Call the Anthropic API directly to generate text using Claude.
    Demonstrates system prompts, temperature, and tracking token usage.
    """
    try:
        client = get_anthropic_client()
        response = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=request.max_tokens,
            temperature=request.temperature,
            system=request.system_prompt,
            messages=[
                {"role": "user", "content": request.prompt}
            ]
        )
        
        return GenerateResponse(
            text=response.content[0].text,
            input_tokens=response.usage.input_tokens,
            output_tokens=response.usage.output_tokens,
            total_tokens=response.usage.input_tokens + response.usage.output_tokens
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/stream")
async def stream_text(request: GenerateRequest):
    """
    Call the OpenAI API to stream text token by token.
    Demonstrates Server-Sent Events (SSE) for better perceived latency.
    """
    async def event_generator():
        try:
            client = get_anthropic_client()
            with client.messages.stream(
                model="claude-3-5-sonnet-20241022",
                max_tokens=request.max_tokens,
                temperature=request.temperature,
                system=request.system_prompt,
                messages=[{"role": "user", "content": request.prompt}]
            ) as stream:
                for text in stream.text_stream:
                    yield text
        except Exception as e:
            yield f"Error: {str(e)}"

    return StreamingResponse(event_generator(), media_type="text/plain")
