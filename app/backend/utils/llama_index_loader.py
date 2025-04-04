import os
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
from app.backend.llm.lmstudio_wrapper import LMStudioEmbedding
import logging
from app.backend.utils.llm_studio_llm import LMStudioLLM # Import from the new module

logging.basicConfig(level=logging.INFO)

class DocumentIndex:
    def __init__(self, directory_path: str = None):
        embed_model = LMStudioEmbedding()
        Settings.embed_model = embed_model

        if directory_path is None:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            directory_path = os.path.join(current_dir, "../../data")
            directory_path = os.path.normpath(directory_path)

        self.directory_path = directory_path
        if not os.path.exists(self.directory_path):
            logging.warning(f"Directory path does not exist: {self.directory_path}")
            self.index = None
        else:
            try:
                self.index = self._create_index()
            except Exception as e:
                logging.error(f"Error creating index: {e}", exc_info=True)
                self.index = None

    def _create_index(self):
        documents = SimpleDirectoryReader(self.directory_path).load_data()
        index = VectorStoreIndex.from_documents(documents)
        return index

    def get_engine(self, **kwargs):
        if self.index is None:
            raise RuntimeError("Index not properly initialized.")

        llm = LMStudioLLM()
        Settings.llm = llm

        return self.index.as_chat_engine(chat_mode="context", verbose=True, **kwargs)