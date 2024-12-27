from dotenv import load_dotenv
import nest_asyncio
from typing import List
from langchain_text_splitters import (
    RecursiveCharacterTextSplitter,
)

from sarthakai.doc_parsing.parse_doc_llamaparse import llamaparse_file_to_md
from sarthakai.models import Chunk

load_dotenv()
nest_asyncio.apply()
CHUNK_SIZE_LIMIT = 1000


def chunk_local_file(filename):
    """First converts any locally saved doc to markdown and then chunks it."""
    print("Processing", filename)
    status, all_documents_md = llamaparse_file_to_md(filename=filename, by_page=True)
    chunks = chunk_text(all_documents_md, CHUNK_SIZE_LIMIT)
    return status, chunks


def chunk_text(document: str, text_size_limit: int) -> List[Chunk]:
    text_splitter = RecursiveCharacterTextSplitter(
        # custom separators can be defined here using `separators=[...]`
        chunk_size=text_size_limit,
        chunk_overlap=50,
        length_function=len,
    )
    texts = text_splitter.split_text(document)
    chunks = [Chunk(text=text) for text in texts]
    return chunks
