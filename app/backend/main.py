from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.backend.api.routes import ask_router
from app.backend.llm.lmstudio_wrapper import LMStudioEmbedding
import logging
import requests

logging.basicConfig(level=logging.INFO)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5173"],  # Allow your frontend origin
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

@app.on_event("startup")
async def startup_event():
    try:
        # Check LLM connection
        response = requests.get("http://127.0.0.1:1234/health")
        response.raise_for_status()
        logging.info("LLM connection verified.")
    except requests.exceptions.RequestException as e:
        logging.error(f"LLM connection failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="LLM connection failed.")

app.include_router(ask_router)