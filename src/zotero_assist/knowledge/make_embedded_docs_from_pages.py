from typing import Sequence, Optional

from llama_index import Document, OpenAIEmbedding
from llama_index.embeddings.base import BaseEmbedding

from zotero_assist.zot.read_pdf_pages import PdfPages


def make_embedded_docs_from_pages(pdf: PdfPages,
                                  embedding_model: Optional[BaseEmbedding] = None) -> Sequence[Document]:
    embedding_model = embedding_model or OpenAIEmbedding()
    return [Document(page, embedding=embedding_model.get_text_embedding(page), doc_id=f"{pdf.src.stem}_p{i}",
                     extra_info=dict(source_pdf=pdf.src.as_posix(), page_idx=i)) for i, page in enumerate(pdf.pages)]
