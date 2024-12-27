import os
import fitz
import logging
import requests
import tempfile

from pathlib import Path
from urllib.parse import urlparse
from fitz import Page
from PIL import Image

from typing import Union, List, Dict, Iterator, Any, Optional

from langchain_core.documents import Document
from langchain_community.document_loaders.pdf import BasePDFLoader
from langchain_community.document_loaders.blob_loaders import Blob
from langchain_community.document_loaders.parsers.pdf import PyMuPDFParser

PROXIES = {
    "http": os.environ["PROXY"],
    "https": os.environ["PROXY"],
}
HEADERS = {
    "User-Agent": os.environ["USER_AGENT"],
}

logger = logging.getLogger(__file__)


class BasePDFProxyLoader(BasePDFLoader):
    def __init__(self, file_path: Union[str, Path], *, headers: Optional[Dict] = None):
        self.file_path = str(file_path)
        self.web_path = None
        self.headers = headers or {}
        # update self.headers
        self.headers = {**self.headers, **HEADERS}
        if "~" in self.file_path:
            self.file_path = os.path.expanduser(self.file_path)

        # If the file is a web path or S3, download it to a temporary file, and use that
        if not os.path.isfile(self.file_path) and self._is_valid_url(self.file_path):
            self.temp_dir = tempfile.TemporaryDirectory()
            _, suffix = os.path.splitext(self.file_path)
            if self._is_s3_presigned_url(self.file_path):
                suffix = urlparse(self.file_path).path.split("/")[-1]
            temp_pdf = os.path.join(self.temp_dir.name, f"tmp{suffix}")
            self.web_path = self.file_path
            if not self._is_s3_url(self.file_path):
                r = requests.get(self.file_path, headers=self.headers, proxies=PROXIES)
                if r.status_code != 200:
                    raise ValueError("Check the url of your file; returned status code %s" % r.status_code)

                with open(temp_pdf, mode="wb") as f:
                    f.write(r.content)
                self.file_path = str(temp_pdf)
        elif not os.path.isfile(self.file_path):
            raise ValueError("File path %s is not a valid file or url" % self.file_path)


class PyMuPDFProxyLoader(BasePDFProxyLoader):
    def __init__(
        self,
        file_path: str,
        *,
        headers: Optional[Dict] = None,
        extract_images: bool = False,
        **kwargs: Any,
    ) -> None:
        super().__init__(file_path, headers=headers)
        self.extract_images = extract_images
        self.text_kwargs = kwargs

    def _lazy_load(self, **kwargs: Any) -> Iterator[Document]:
        if kwargs:
            logger.warning(
                f"Received runtime arguments {kwargs}. Passing runtime args to `load`"
                f" is deprecated. Please pass arguments during initialization instead."
            )

        text_kwargs = {**self.text_kwargs, **kwargs}
        parser = PyMuPDFParser(text_kwargs=text_kwargs, extract_images=self.extract_images)
        if self.web_path:
            blob = Blob.from_data(open(self.file_path, "rb").read(), path=self.web_path)  # type: ignore[attr-defined]
        else:
            blob = Blob.from_path(self.file_path)  # type: ignore[attr-defined]
        yield from parser.lazy_parse(blob)

    def load(self, **kwargs: Any) -> List[Document]:
        return list(self._lazy_load(**kwargs))

    def lazy_load(self) -> Iterator[Document]:
        yield from self._lazy_load()


class ImagePDFProxyLoader(BasePDFProxyLoader):
    def __init__(
        self,
        file_path: str,
        *,
        headers: Optional[Dict] = None,
    ) -> None:
        super().__init__(file_path, headers=headers)

    def load_pdf_page(self, page: Page, dpi: int) -> Image.Image:
        pix = page.get_pixmap(matrix=fitz.Matrix(dpi / 72, dpi / 72))
        image = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

        if pix.width > 3000 or pix.height > 3000:
            pix = page.get_pixmap(matrix=fitz.Matrix(1, 1), alpha=False)
            image = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

        return image

    def load(self) -> List[Image.Image]:
        images = []

        doc = fitz.open(self.file_path)
        for i in range(len(doc)):
            page = doc[i]
            image = self.load_pdf_page(page, dpi=250)
            images.append(image)

        return images

    def lazy_load(self) -> Iterator[Image.Image]:
        raise NotImplementedError("Lazy loading is not supported for ImagePDFProxyLoader")
