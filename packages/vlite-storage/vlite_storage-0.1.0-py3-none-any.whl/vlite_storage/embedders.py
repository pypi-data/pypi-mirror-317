from typing import List
import numpy as np
from ollama import EmbedResponse, Client


class OllamaEmbedder:
    """Class to embed texts using the Ollama model.

    This class provides methods to check and load the model,
    retrieve the dimensions of the embeddings, and generate
    embeddings for a list of texts.
    """

    def __init__(
        self,
        base_url: str = "http://localhost:11434",
        model_name: str = "bge-m3:latest",
    ):
        """Initializes the OllamaEmbedder with the specified base URL and model name.

        Args:
            base_url (str): The base URL for the Ollama client.
            model_name (str): The name of the model to use.
        """
        self.client = Client(base_url)
        self.model_name = model_name
        self._check_and_load_model()
        self.dim = None

    def dimensions(self) -> int:
        """Retrieves the dimensions of the embeddings.

        If the dimensions have not been previously calculated,
        it sends a test request to get the dimensions.

        Returns:
            int: The dimensions of the embeddings.

        Example:
            >>> embedder = OllamaEmbedder()
            >>> dim = embedder.dimensions()
            >>> print(dim)
        """
        if self.dim is not None:
            return self.dim
        test_request = self.client.embed(
            model=self.model_name, input="hello", keep_alive=True
        )
        self.dim = len(test_request.embeddings[0])
        return self.dim

    def __call__(self, texts: List[str]) -> np.ndarray:
        """Generates embeddings for a list of texts.

        Args:
            texts (List[str]): A list of texts to embed.

        Returns:
            np.ndarray: An array of embeddings for the input texts.

        Example:
            >>> embedder = OllamaEmbedder()
            >>> embeddings = embedder(["Hello world", "How are you?"])
            >>> print(embeddings)
        """
        response: EmbedResponse = self.client.embed(
            model=self.model_name, input=texts, keep_alive=True
        )
        embeddings = np.array(response.embeddings, dtype=np.float32)
        return embeddings

    def _check_and_load_model(self) -> bool:
        """Checks if the specified model is available and loads it if not.

        Returns:
            bool: True if the model is available or successfully loaded, False otherwise.
        """
        models = {model.model for model in self.client.list().models}
        if self.model_name not in models:
            print(f"Model {self.model_name} not found, loading...")
            try:
                self.client.pull(model=self.model_name, stream=True)
            except Exception as e:
                print(f"Error loading model: {e}")
                raise e
        return True
