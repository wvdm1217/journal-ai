import numpy as np
import faiss
from typing import List, Dict, Tuple
from openai import OpenAI
from journal_ai.models import JournalEntry
from journal_ai.config import Config


class RAGQuerier:
    def __init__(self, config: Config):
        self.config = config
        self.client = OpenAI(api_key=config.openai_api_key)
        self.index = None
        self.entries: List[JournalEntry] = []

    def _get_embedding(self, text: str) -> np.ndarray:
        response = self.client.embeddings.create(
            input=text,
            model=self.config.embedding_model
        )
        return np.array(response.data[0].embedding, dtype=np.float32)

    def index_entries(self, entries: Dict[str, JournalEntry]):
        self.entries = list(entries.values())
        embeddings = [self._get_embedding(entry.content)
                      for entry in self.entries]

        dimension = len(embeddings[0])
        self.index = faiss.IndexFlatL2(dimension)
        self.index.add(np.array(embeddings))

    def query(self, question: str, k: int = 3) -> str:
        question_embedding = self._get_embedding(question)
        D, I = self.index.search(question_embedding.reshape(1, -1), k)

        context = "\n\n".join([
            f"Entry {self.entries[i].id} ({self.entries[i].title}):\n{
                self.entries[i].content}"
            for i in I[0]
        ])

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
