from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage
import numexpr as ne
from GeekyAnts.app.core.config import settings

def calculate(expression: str) -> str:
    """Evaluate a mathematical expression using numexpr."""
    try:
        # numexpr evaluates mathematical strings safely and quickly
        return str(ne.evaluate(expression).item())
    except Exception as e:
        return f"Error evaluating expression: {str(e)}"

class AgentService:
    def __init__(self):
        self.llm = ChatAnthropic(
            model="claude-3-5-sonnet-20241022", 
            anthropic_api_key=settings.ANTHROPIC_API_KEY, 
            temperature=0
        )

    def run_agent(self, question: str) -> dict:
        """
        Run the agent with the provided question using LLM.
        Returns the response from the LLM.
        """
        try:
            # Create a prompt that tells the LLM about available tools
            system_prompt = """You are a helpful assistant with access to tools for mathematical calculations and web searches.

For math questions:
- If the question asks for calculation, solve it directly or describe how to solve it
- Examples: "What is 2+2?", "Calculate 15 * 3"

For factual questions:
- Provide accurate information based on your training data
- Be helpful and informative

Always be clear and concise in your responses."""
            
            messages = [
                HumanMessage(content=system_prompt + "\n\nUser question: " + question)
            ]
            
            response = self.llm.invoke(messages)
            
            return {
                "input": question,
                "output": response.content
            }
        except Exception as e:
            return {
                "input": question,
                "output": f"Error: {str(e)}"
            }

agent_service = AgentService()
