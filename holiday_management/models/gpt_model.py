import os
from dotenv import load_dotenv
from autogen_ext.models.openai import OpenAIChatCompletionClient

# Load .env before reading any environment variables
load_dotenv()

model_client = OpenAIChatCompletionClient(
    model=os.getenv("MODEL_NAME", "gpt-4o"),
    api_key=os.environ["OPENAI_API_KEY"],
)
