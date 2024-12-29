import os, logging, traceback
from typing import Iterator, AsyncIterator, Optional
from langchain_core.document_loaders import BaseLoader
from langchain_core.documents import Document
from langchain_core.runnables import run_in_executor
from docling.document_converter import DocumentConverter, ConversionResult, ConversionStatus

class DoclingLoader(BaseLoader):
  def __init__(self, file_path: str | list[str]) -> None:
      self._file_paths = file_path if isinstance(file_path, list) else [file_path]
      self._converter = DocumentConverter()
  def load(self) -> list[Document]:
      """Load data into Document objects."""
      return list(self.lazy_load())
  async def aload(self) -> list[Document]:
      """Load data into Document objects."""
      return [document async for document in self.alazy_load()]
  async def alazy_load(self) -> AsyncIterator[Document]:
      """A lazy loader for Documents."""
      iterator = await run_in_executor(None, self.lazy_load)
      done = object()
      while True:
          doc = await run_in_executor(None, next, iterator, done)  # type: ignore[call-arg, arg-type]
          if doc is done:
              break
          yield doc  # type: ignore[misc]
  def lazy_load(self) -> Iterator[Document]:
      for source in self._file_paths:
          try:
            _result = self._converter.convert(
               os.path.abspath(source),
               raises_on_error=True)
            doc = _result.document
            text = doc.export_to_markdown(image_placeholder="")
            yield Document(page_content=text, metadata={"source": source})
          except Exception as e:
            logging.warning(f"Failed to load document from {source}: {e} | {traceback.format_exc()}")
