from typing import Dict, List

import faiss
import numpy as np
from openai import OpenAI

from journal_ai.config import Config
from journal_ai.models import JournalEntry
from journal_ai.storage import JsonStorage


class RAGQuerier:
    def __init__(self, config: Config):
        self.config = config
        self.client = OpenAI(api_key=config.openai_api_key)
        self.storage = JsonStorage(config=config)
        self.index = None
        self.entries: List[JournalEntry] = []

    def _load_or_create_index(self, dimension: int) -> faiss.IndexFlatL2:
        index_path = self.storage.get_vector_db_path()
        if index_path.exists():
            try:
                return faiss.read_index(str(index_path))
            except:
                return faiss.IndexFlatL2(dimension)
        return faiss.IndexFlatL2(dimension)

    def _save_index(self):
        if self.index is not None:
            faiss.write_index(self.index, str(
                self.storage.get_vector_db_path()))

    def _get_embedding(self, text: str) -> np.ndarray:
        response = self.client.embeddings.create(
            input=text, model=self.config.embedding_model
        )
        return np.array(response.data[0].embedding, dtype=np.float32)

    def index_entries(self, entries: Dict[str, JournalEntry]):
        self.entries = list(entries.values())
        embeddings = [self._get_embedding(entry.content)
                      for entry in self.entries]

        dimension = len(embeddings[0])
        self.index = self._load_or_create_index(dimension)
        self.index.reset()  # Clear existing vectors
        self.index.add(np.array(embeddings))
        self._save_index()

    def query(self, question: str, k: int = 3) -> str:
        if self.index is None:
            index_path = self.storage.get_vector_db_path()
            if not index_path.exists():
                return "No indexed entries found. Please add some entries first."
            self.index = faiss.read_index(str(index_path))
            self.entries = list(self.storage.load_all().values())

        question_embedding = self._get_embedding(question)
        D, I = self.index.search(question_embedding.reshape(1, -1), k)

        context = "\n\n".join(
            [
                f"Entry {self.entries[i].id} ({self.entries[i].title}):\n{
                    self.entries[i].content
                }"
                for i in I[0]
            ]
        )

        prompt = f"""Based on the following journal entries, answer this question: {question}

Context entries:
{context}

Please provide a thoughtful answer based only on the information in these journal entries."""

        response = self.client.chat.completions.create(
            model=self.config.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
        )

        return response.choices[0].message.content
