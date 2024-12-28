import json
import sqlite3
import apsw
import numpy as np
import vectorlite_py as vlite

from dataclasses import dataclass
from typing import Callable, List, Optional, Tuple
from vlite_storage.embedders import OllamaEmbedder


@dataclass
class Document:
    content: str
    metadata: dict


class Storage:
    def __init__(
        self,
        db_name: str,
        dim: int,
        embedding_fn: Optional[Callable[[str], np.ndarray]] = None,
    ):
        self.db_name = db_name
        self.dim = dim
        self.embedding_fn = (
            embedding_fn if embedding_fn else OllamaEmbedder(model_name="bge-m3:latest")
        )

        self.conn = apsw.Connection(self.db_name)
        self.conn.enable_load_extension(True)
        self.conn.load_extension(vlite.vectorlite_path())

        self._setup_tables()

    def add(self, content: str, metadata: dict):
        """Adds a document with its content and metadata to the database."""
        embedding_vector = self.embedding_fn(content).tobytes()

        with self.conn as db:
            cur = db.cursor()
            cur.execute(
                "INSERT INTO documents(content, metadata) VALUES (?, ?)",
                (content, json.dumps(metadata)),
            )

            rowid = db.last_insert_rowid()
            cur.execute(
                "INSERT INTO vectors(rowid, embedding) VALUES (?, ?)",
                (rowid, embedding_vector),
            )

    def remove(self, rowid: int):
        """Deletes a document by rowid."""
        with self.conn:
            cur = self.conn.cursor()
            cur.execute("DELETE FROM documents WHERE rowid = ?", (rowid,))
            cur.execute("DELETE FROM vectors WHERE rowid = ?", (rowid,))

    def update(self, rowid: int, content: Optional[str], metadata: Optional[dict]):
        """Updates the content and/or metadata of a document by rowid."""
        with self.conn:
            cur = self.conn.cursor()
            if content is not None:
                embedding_vector = self.embedding_fn(content).tobytes()
                cur.execute(
                    "UPDATE documents SET content = ? WHERE rowid = ?", (content, rowid)
                )
                cur.execute(
                    "UPDATE vectors SET embedding = ? WHERE rowid = ?",
                    (embedding_vector, rowid),
                )
            if metadata is not None:
                cur.execute(
                    "UPDATE documents SET metadata = ? WHERE rowid = ?",
                    (json.dumps(metadata), rowid),
                )

    def get(self, rowid: int) -> Document:
        """Retrieves a document's content and metadata by rowid."""
        with self.conn:
            cur = self.conn.cursor()
            cur.execute(
                "SELECT content, metadata FROM documents WHERE rowid = ?", (rowid,)
            )
            result = cur.fetchone()
            if result:
                content, metadata_json = result
                return Document(content, json.loads(metadata_json))
            return None

    def search(self, text: str, k: int) -> List[Tuple[Document, float]]:
        """Performs a vector search to find k nearest neighbors to the embedding of the given text."""
        query_embedding = self.embedding_fn(text).tobytes()
        with self.conn:
            cur = self.conn.cursor()
            cur.execute(
                "SELECT rowid, distance FROM vectors WHERE knn_search(embedding, knn_param(?, ?)) ORDER BY distance ASC",
                (query_embedding, k),
            )
            ids = cur.fetchall()
            documents = [(self.get(rowid), distance) for rowid, distance in ids]
            return documents

    def close(self):
        """Closes the database connection."""
        self.conn.close()

    def _setup_tables(self):
        """Initializes database tables and vector search virtual table."""
        with self.conn:
            cur = self.conn.cursor()
            cur.execute("""
            CREATE TABLE IF NOT EXISTS documents (
                rowid INTEGER PRIMARY KEY,
                content TEXT,
                metadata TEXT
            )""")

            # Create vector search virtual table
            max_elements = 2**20
            index_file_path = f"{self.db_name}_index.bin"
            cur.execute(f"""
            CREATE VIRTUAL TABLE IF NOT EXISTS vectors USING vectorlite(
                embedding float32[{self.dim}] cosine,
                hnsw(max_elements={max_elements}), 
                '{index_file_path}'
            )
            """)
