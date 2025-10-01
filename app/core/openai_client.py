import os
from openai import AzureOpenAI
from app.schemas.chat import ChatRequest
from dotenv import load_dotenv
load_dotenv()

client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version="2024-02-15-preview",
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
)


async def stream_openai_chat(body: ChatRequest):
    response = client.chat.completions.create(
        model=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
        messages=[m.dict() for m in body.messages],
        stream=True
    )

    for chunk in response:
        if not chunk.choices or not chunk.choices[0].delta:
            continue
        delta = chunk.choices[0].delta.content

        if delta:
            yield delta


