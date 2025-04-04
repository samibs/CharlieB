from llama_index.core.base.embeddings.base import BaseEmbedding
from typing import List, Optional
import requests
from pydantic import Field
import time
import logging

logging.basicConfig(level=logging.INFO)

class LMStudioEmbedding(BaseEmbedding):
    endpoint: str = Field(default="http://127.0.0.1:1234/v1/embeddings")
    model: str = Field(default="text-embedding-nomic-embed-text-v1.5@q8_0")
    max_retries: int = Field(default=3)
    retry_delay: int = Field(default=1)

    def _get_query_embedding(self, query: str) -> List[float]:
        return self._get_text_embedding(query)

    async def _aget_query_embedding(self, query: str) -> List[float]:
        return self._get_text_embedding(query)

    def _get_text_embedding(self, text: str) -> List[float]:
        return self._get_text_embedding_batch([text])[0]

    def _get_text_embedding_batch(self, texts: List[str]) -> List[List[float]]:
        retries = 0
        while retries < self.max_retries:
            try:
                response = requests.post(
                    self.endpoint,
                    headers={"Content-Type": "application/json", "Authorization": "Bearer lm-studio"},
                    json={"model": self.model, "input": texts},
                )
                response.raise_for_status()
                result = response.json()
                if "data" not in result:
                    logging.error(f"Unexpected response format: {result}")
                    return [[] for _ in texts]
                return [r["embedding"] for r in result["data"]]
            except requests.exceptions.ConnectionError as e:
                logging.warning(f"Connection error: {e}. Retrying in {self.retry_delay} seconds...")
                time.sleep(self.retry_delay)
                retries += 1
            except requests.exceptions.RequestException as e:
                logging.error(f"Request error: {e}", exc_info=True)
                return [[] for _ in texts]

        logging.error(f"Failed to fetch embeddings after {self.max_retries} retries.")
        return [[] for _ in texts]