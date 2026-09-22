from pathlib import Path
import chromadb

from config import CHROMA_DIR, COLLECTION_NAME


class KnowledgeBase:
    def __init__(self):
        Path(CHROMA_DIR).mkdir(parents=True, exist_ok=True)

        self.db = chromadb.PersistentClient(path=CHROMA_DIR)
        self.collection = self.db.get_or_create_collection(
            COLLECTION_NAME
        )

    def add(self, client_id, texts):
        if not texts:
            return

        ids = [f"{client_id}_{i}" for i in range(len(texts))]

        self.collection.upsert(
            ids=ids,
            documents=texts,
            metadatas=[{"client_id": client_id} for _ in texts],
        )

    def search(self, client_id, query, k=4):
        result = self.collection.query(
            query_texts=[query],
            n_results=k,
            where={"client_id": client_id},
        )

        documents = result.get("documents", [[]])
        return documents[0] if documents else []


kb = KnowledgeBase()


def seed_demo_data():
    kb.add(
        "manufacturing_demo",
        [
            "ABC Industrial Systems provides industrial automation solutions.",
            "The company works with manufacturing operations and procurement teams.",
            "Key themes include predictive maintenance, production efficiency and operational visibility.",
        ],
    )

    kb.add(
        "fintech_demo",
        [
            "XYZ Financial Technologies builds software for digital payments and fraud prevention.",
            "The company focuses on secure payment infrastructure and financial operations.",
            "Key themes include digital payments, fraud prevention and financial technology.",
        ],
    )
