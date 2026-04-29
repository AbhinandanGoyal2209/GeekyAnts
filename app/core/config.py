import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    ANTHROPIC_API_KEY: str = os.getenv("ANTHROPIC_API_KEY", "")
    API_USERNAME: str = os.getenv("API_USERNAME", "admin")
    API_PASSWORD: str = os.getenv("API_PASSWORD", "secretpassword")

settings = Settings()
