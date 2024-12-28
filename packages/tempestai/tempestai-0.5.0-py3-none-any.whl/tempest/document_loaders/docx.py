import os
from pathlib import Path
from typing import List, Optional

from tempest.core.document import Document
from tempest.core.document_loaders import BaseLoader


class DocxLoader(BaseLoader):
    """Microsoft Word (Docx) loader."""

    def load_data(self, input_file: str, extra_info: Optional[dict] = None) -> List[Document]:
        """Loads data from the specified directory.
        
        Args:
            input_file (str): File path to load.
        """
        try:
            import docx2txt  # noqa: F401
        except ImportError:
            raise ImportError("docx2txt package not found, please install it with `pip install docx2txt`")
        
        if not os.path.isfile(input_file):
            raise ValueError(f"File `{input_file}` does not exist")
        
        input_file = str(Path(input_file).resolve())

        text = docx2txt.process(input_file)
        metadata = {"source": input_file}

        return [Document(text=text, metadata=metadata)]
