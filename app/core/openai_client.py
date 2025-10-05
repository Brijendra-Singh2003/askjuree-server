import os
from openai import AzureOpenAI
from app.schemas.chat import ChatRequest
# from app.crud.chat import get_chat_message, add_chat_message, ChatMessageCreate
from dotenv import load_dotenv
load_dotenv()

MODEL_NAME = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")

client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version="2024-02-15-preview",
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
)

async def stream_openai_chat(body: ChatRequest):
    json_chats = [message.model_dump() for message in body.messages]
    
    #TODO: get all messages of a conversation from database
    # json_chats = [{
    #     "role": chat.role,
    #     "content": chat.content,
    # } for chat in get_chat_message()]
    
    # new_message = body.messages[-1]
    # json_chats.append(new_message.model_dump())

    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=json_chats,
            stream=True,
            max_tokens=300,
        )

        content = ""

        for chunk in response:
            if not chunk.choices or len(chunk.choices) <= 0 or not chunk.choices[0].delta:
                continue

            delta = chunk.choices[0].delta.content

            if delta:
                content += delta
                yield delta

        # add_chat_message(ChatMessageCreate(
        #     role=new_message.role,
        #     content=new_message.content,
        # ))

        # add_chat_message(ChatMessageCreate(
        #     role="assistant",
        #     content=content,
        # ))
    except Exception as e:
        yield f"Error: {str(e)}"

