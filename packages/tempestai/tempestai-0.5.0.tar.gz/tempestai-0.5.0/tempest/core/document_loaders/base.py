from abc import ABC, abstractmethod
from typing import List, Optional

from pydantic.v1 import BaseModel

from tempest.core.document import Document


class BaseLoader(ABC, BaseModel):
    """An interface for document loader."""

    @classmethod
    def class_name(cls) -> str:
        return "BaseLoader"

    @abstractmethod
    def load_data(self, extra_info: Optional[dict] = None) -> List[Document]:
        """Loads data."""

    def load(self) -> List[Document]:
        return self.load_data()

    def lazy_load(self) -> List[Document]:
        return self.load_data()
