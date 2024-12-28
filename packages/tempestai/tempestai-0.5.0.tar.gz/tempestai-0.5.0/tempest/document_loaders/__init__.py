from tempest.document_loaders.directory import DirectoryLoader
from tempest.document_loaders.docx import DocxLoader
from tempest.document_loaders.html import HTMLLoader
from tempest.document_loaders.json import JSONLoader
from tempest.document_loaders.pdf import PDFLoader
from tempest.document_loaders.s3 import S3Loader
from tempest.document_loaders.watson_discovery import WatsonDiscoveryLoader

__all__ = [
    "DirectoryLoader",
    "DocxLoader",
    "HTMLLoader",
    "JSONLoader",
    "PDFLoader",
    "S3Loader",
    "WatsonDiscoveryLoader",
]
