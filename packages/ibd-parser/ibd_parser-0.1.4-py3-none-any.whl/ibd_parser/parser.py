import os
import struct
from typing import List, Dict, Any, Optional
from .constants import PAGE_SIZE, PageType
from .page.fil import FilHeader, FilTrailer
from .page.index import IndexHeader
from .record.record_parser import RecordParser
from .utils import hex_dump

class IBDFileParser(object):
    def __init__(self, file_path: str, schema: Optional[Dict[str, Any]] = None):
        self.file_path = file_path
        self.file_size = os.path.getsize(file_path)
        self.schema = schema

    def parse_page_directory(self, page_data: bytes, n_dir_slots: int) -> List[int]:
        directory = []
        page_end = PAGE_SIZE - 8
        for i in range(n_dir_slots):
            slot_offset = page_end - (i + 1) * 2
            slot = struct.unpack('>H', page_data[slot_offset:slot_offset+2])[0]
            directory.append(slot)
        return directory

    def page_dump(self, page_no: int) -> Dict[str, Any]:
        with open(self.file_path, 'rb') as f:
            f.seek(page_no * PAGE_SIZE)
            page_data = f.read(PAGE_SIZE)

            page_header = FilHeader.parse(page_data)
            page_trailer = FilTrailer.parse(page_data)
            result = {
                'page_no': page_no,
                'header': page_header,
                'trailer': page_trailer
            }

            if page_header.page_type == PageType.FIL_PAGE_INDEX:
                index_header = IndexHeader.parse(page_data)
                result['page_header'] = index_header

                directory = self.parse_page_directory(
                    page_data,
                    index_header.n_dir_slots
                )
                result['page_directory'] = directory
                if self.schema:
                    record_parser = RecordParser(page_data, index_header, directory, self.schema)
                    result['records'] = record_parser.parse_records()

            return result
