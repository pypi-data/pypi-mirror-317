import logging
import os
from pathlib import Path
from typing import List, Optional

from tempest.core.document import Document
from tempest.core.document_loaders import BaseLoader

logger = logging.getLogger("pypdf")
logger.setLevel(logging.ERROR)

class PDFLoader(BaseLoader):
    """PDF loader using PyPDF."""

    def load_data(self, input_file: str, extra_info: Optional[dict] = None) -> List[Document]:
        """Loads data from the specified directory.
        
        Args:
            input_file (str): File path to load.
        """
        try:
            import pypdf  # noqa: F401

        except ImportError:
            raise ImportError("pypdf package not found, please install it with `pip install pypdf`")
        
        if not os.path.isfile(input_file):
            raise ValueError(f"File `{input_file}` does not exist")
        
        input_file = str(Path(input_file).resolve())
        pdf_loader = pypdf.PdfReader(input_file)

        return [
            Document(
                text=page.extract_text().strip(),
                metadata={"source": input_file, "page": page_number}
            )
            for page_number, page in enumerate(pdf_loader.pages)
        ]
