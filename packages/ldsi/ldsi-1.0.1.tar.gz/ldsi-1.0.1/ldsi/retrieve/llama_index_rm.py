import logging
from typing import Optional

import ldsi

try:
    from llama_index.core.base.base_retriever import BaseRetriever
except ImportError:
    err = "The 'llama_index' package is required to use LlamaIndexRM. Install it with 'pip install llama_index'."
    raise ImportError(err) from None

NO_TOP_K_WARNING = "The underlying LlamaIndex retriever does not support top k retrieval. Ignoring k value."


class LlamaIndexRM(ldsi.Retrieve):
    """Implements a retriever which wraps over a LlamaIndex retriever.

    This is done to bridge LlamaIndex and LDSI and allow the various retrieval
    abstractions in LlamaIndex to be used in LDSI.

    To-do (maybe):
        - Async support (LDSI lacks this entirely it seems, so not a priority until the rest of the repo catches on)
        - Text/video retrieval (Available in LI, not sure if this will be a priority in LDSI)

    Args:
        retriever (BaseRetriever): A LlamaIndex retriever object - text based only
        k (int): Optional; the number of examples to retrieve (similarity_top_k)

        If the underlying LI retriever does not have the property similarity_top_k, k will be ignored.

    Returns:
        LDSI RM Object - this is a retriever object that can be used in LDSI
    """

    retriever: BaseRetriever

    def __init__(
        self,
        retriever: BaseRetriever,
        k: Optional[int] = None,
    ):
        self.retriever = retriever

        if k:
            self.k = k

    @property
    def k(self) -> Optional[int]:
        """Get similarity top k of retriever."""
        if not hasattr(self.retriever, "similarity_top_k"):
            logging.warning(NO_TOP_K_WARNING)
            return None

        return self.retriever.similarity_top_k

    @k.setter
    def k(self, k: int) -> None:
        """Set similarity top k of retriever."""
        if hasattr(self.retriever, "similarity_top_k"):
            self.retriever.similarity_top_k = k
        else:
            logging.warning(NO_TOP_K_WARNING)

    def forward(self, query: str, k: Optional[int] = None) -> list[ldsi.Example]:
        """Forward function for the LI retriever.

        This is the function that is called to retrieve the top k examples for a given query.
        Top k is set via the setter similarity_top_k or at LI instantiation.

        Args:
            query (str): The query to retrieve examples for
            k (int): Optional; the number of examples to retrieve (similarity_top_k)

            If the underlying LI retriever does not have the property similarity_top_k, k will be ignored.

        Returns:
            List[ldsi.Example]: A list of examples retrieved by the retriever
        """
        if k:
            self.k = k

        raw = self.retriever.retrieve(query)

        return [
            ldsi.Example(
                text=result.text,
                score=result.score,
            )
            for result in raw
        ]
