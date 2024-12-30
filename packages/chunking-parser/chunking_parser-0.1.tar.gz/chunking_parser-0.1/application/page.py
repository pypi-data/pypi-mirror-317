import typing as tp
import json
import fitz
import math
from dataclasses import dataclass
from .file import Files


class PDFPageTextInfo:
    def __init__(
        self,
        page_no: int,
        font: int = None,
        text: str = "",
        ocr_text = False,
        block_start = False,
        size: int = None,
        bbox: tp.List = None,
    ):
        self.page_no = page_no
        self.font = font
        self.text = text
        self.ocr_text = ocr_text
        self.block_start = block_start
        self.size = size
        self.bbox = bbox

    def get_text(self):
        return self.text

    def get_page_text_info(self):
        return self

    def is_valid(self):
        return True if self.text.strip() else False

    def is_ocr(self):
        return self.ocr_text

    def is_bold(self):
        return ("Bold" in self.font)

    def startswith(self, keywords: list):
        for prefix in keywords:
            if self.text.lower().startswith(prefix.lower()):
                return True
        return False

    def is_next_page(self, other):
        return True if self.page_no == other.page_no + 1 else False

    def __str__(self):
        return(self.text
               + '#<o>#' + str(self.ocr_text)
               + '#<b>#' + str(self.block_start)
               + '#<p>#' + str(self.page_no)
               + '#<f>#' + str(self.font)
               + '#<s>#' + str(self.size)
               + '#<b>#' + str(self.bbox))


class PDFProcessor:
    async def get_doc(self, file: Files):
        # blob = await file.to_BytesIO_format()
        file._file.seek(0)
        doc = fitz.open("pdf", stream=file._file)
        return doc

    async def get_page(self, file: Files):
        doc = await self.get_doc(file)
        for page_no in range(len(doc)):
            page = doc.load_page(page_no)
            yield (page, page_no)

@dataclass
class PDFPageClauseProperties:
    id: int
    identifier_regex: str
    identifier_value: str
    content: str
    block_start: bool
    bbox: any
    page_no: int
    colon: bool
    start_char_x_coord: float

    def get_page_clause_properties(self):
        return dict(
            self.id,
            self.identifier_regex,
            self.identifier_value,
            self.content,
            self.block_start,
            self.bbox,
            self.page_no,
            self.colon,
            self.start_char_x_coord,
        )

    def get_bbox(self):
        return self.bbox

    def is_valid(self):
        return True if self.content.strip() else False

    def is_block_start(self):
        return self.block_start

    def __str__(self):
        dobj = {'id': self.id, \
                'id_regex': self.identifier_regex, \
                'id_value': self.identifier_value, \
                'content_len': len(self.content), \
                'content': self.content, \
                'block_start': self.block_start, \
                'bbox': self.bbox, \
                'page_no': self.page_no, \
                'colon': self.colon, \
                'start': self.start_char_x_coord}
        return str(dobj)
