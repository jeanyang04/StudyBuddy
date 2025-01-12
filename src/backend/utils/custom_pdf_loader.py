from io import BytesIO
from typing import List, Optional, Union
from langchain_community.document_loaders import PyPDFLoader
from langchain.schema import Document

class CustomPDFLoader(PyPDFLoader):
    def __init__(self, stream: BytesIO, password: Optional[Union[str, bytes]] = None):
        self.stream = stream
        self.password = password

    def load(self) -> List[Document]:
        # Create a temporary file-like object from the BytesIO stream
        return PyPDFLoader.load(self)