from typing import Sequence, Optional

from llama_index import Document, OpenAIEmbedding
from llama_index.embeddings.base import BaseEmbedding


def make_embedded_docs_from_pages(pages: Sequence[str],
                                  embedding_model: Optional[BaseEmbedding] = None) -> Sequence[Document]:
    embedding_model = embedding_model or OpenAIEmbedding()
    return [Document(page, embedding=embedding_model.get_text_embedding(page)) for page in pages]
