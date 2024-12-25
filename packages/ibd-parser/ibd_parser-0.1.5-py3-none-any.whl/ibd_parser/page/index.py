from dataclasses import dataclass
import struct
from typing import Dict, Any, List
from ibd_parser.constants import PageType, PAGE_SIZE, FIL_PAGE_DATA

@dataclass
class IndexHeader:
    n_dir_slots: int
    heap_top: int
    n_heap_format: int
    n_heap: int
    format: str
    garbage_offset: int
    garbage_size: int
    last_insert_offset: int
    direction: str
    n_direction: int
    n_recs: int
    max_trx_id: int
    level: int
    index_id: int

    @classmethod
    def parse(cls, page_data: bytes) -> 'IndexHeader':
        offset = FIL_PAGE_DATA
        header = struct.unpack('>HHHHHHHHHQHQ', page_data[offset:offset+36])

        n_heap_format = header[2]
        format_flag = (n_heap_format & 0x8000) >> 15
        n_heap = n_heap_format & 0x7fff

        direction = "no_direction"
        if header[6] == 1:
            direction = "right"
        elif header[6] == 2:
            direction = "left"
        return cls(
            n_dir_slots=header[0],
            heap_top=header[1],
            n_heap_format=n_heap_format,
            n_heap=n_heap,
            format="compact" if format_flag == 1 else "redundant",
            garbage_offset=header[3],
            garbage_size=header[4],
            last_insert_offset=header[5],
            direction=direction,
            n_direction=header[7],
            n_recs=header[8],
            max_trx_id=header[9],
            level=header[10],
            index_id=header[11]
        )

    def format_as_string(self) -> str:
        return (
            "#<IndexHeader\n"
            f" n_dir_slots={self.n_dir_slots},\n"
            f" heap_top={self.heap_top},\n"
            f" n_heap_format={self.n_heap_format},\n"
            f" n_heap={self.n_heap},\n"
            f" format={self.format},\n"
            f" garbage_offset={self.garbage_offset},\n"
            f" garbage_size={self.garbage_size},\n"
            f" last_insert_offset={self.last_insert_offset},\n"
            f" direction={self.direction},\n"
            f" n_direction={self.n_direction},\n"
            f" n_recs={self.n_recs},\n"
            f" max_trx_id={self.max_trx_id},\n"
            f" level={self.level},\n"
            f" index_id={self.index_id}\n"
            ">"
        )
