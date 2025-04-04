from fastapi import APIRouter, Request, HTTPException
from pydantic import BaseModel
from app.backend.utils.llama_index_loader import DocumentIndex
from app.backend.utils.llm_studio_llm import LMStudioLLM
from llama_index.core.chat_engine.types import AgentChatResponse
from llama_index.core.base.llms.types import ChatResponse
import logging
import asyncio

logging.basicConfig(level=logging.INFO)
ask_router = APIRouter()

# Health check endpoint
@ask_router.get("/health")
async def health_check():
    logging.info("✅ Health check requested.")
    return {"status": "ok"}

# Init document index and LLM
index = DocumentIndex()
llm = LMStudioLLM()
chat_engine = index.get_engine(llm=llm)
logging.info(f"✅ Chat engine initialized: {chat_engine}")

class AskRequest(BaseModel):
    question: str

@ask_router.post("/ask")
async def ask_question(request: Request):
    data = await request.json()
    question = data.get("question")

    if not question:
        logging.warning("⚠️ Missing question in request.")
        raise HTTPException(status_code=400, detail="Missing question in request.")

    try:
        logging.info(f"💬 Processing question: {question}")
        # Ensure the sync method is safely called in async context
        response = await asyncio.to_thread(chat_engine.chat, question)

        logging.info(f"📦 Chat engine response type: {type(response)}")
        logging.debug(f"📦 Response dir: {dir(response)}")

        if isinstance(response, ChatResponse):
            raw_response = response.message.content
        elif isinstance(response, AgentChatResponse):
            raw_response = response.response
        else:
            logging.error(f"❌ Unexpected response type: {type(response)}")
            raise ValueError(f"Unexpected response type: {type(response)}")

        if not raw_response:
            return {"answer": "⚠️ No response generated."}

        cleaned_response = clean_llm_response(raw_response)
        logging.info(f"🧼 Cleaned response: {cleaned_response}")
        return {"answer": cleaned_response}

    except Exception as e:
        logging.error(f"❌ Error processing question: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")


@ask_router.post("/test_llm_complete")
async def test_llm_complete(request: Request):
    data = await request.json()
    question = data.get("question")

    if not question:
        logging.warning("⚠️ Missing question in test request.")
        raise HTTPException(status_code=400, detail="Missing question in request.")

    try:
        logging.info(f"🧪 Testing LMStudioLLM.complete with: {question}")
        result = await asyncio.to_thread(llm.complete, question)
        logging.info(f"🧪 Complete result type: {type(result)}")
        logging.info(f"🧪 Complete result: {result}")
        return {"result": str(result), "type": str(type(result))}
    except Exception as e:
        logging.error(f"❌ Error testing LMStudioLLM.complete: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")


def clean_llm_response(raw_response: str) -> str:
    logging.info(f"🧼 Cleaning raw response: {raw_response}")
    parts = raw_response.split("--------------------")
    if len(parts) > 1:
        return parts[-1].strip()
    return raw_response.strip()
