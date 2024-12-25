from dataclasses import dataclass
import struct
from typing import Dict, Any, List
from ibd_parser.constants import PageType


@dataclass
class FilHeader:
    checksum: int
    page_no: int
    previous_page: int
    next_page: int
    lsn: int
    page_type: PageType
    flush_lsn: int
    space_id: int

    @classmethod
    def parse(cls, page_data: bytes) -> "FilHeader":
        header = struct.unpack(">IIIIQHQI", page_data[:38])
        return cls(
            checksum=header[0],
            page_no=header[1],
            previous_page=header[2],
            next_page=header[3],
            lsn=header[4],
            page_type=PageType(header[5]),
            flush_lsn=header[6],
            space_id=header[7],
        )

    def format(self) -> str:
        return (
            "#<FilHeader\n"
            f" checksum={self.checksum},\n"
            f" offset={self.page_no},\n"
            f" prev={self.previous_page if self.previous_page != 4294967295 else 'nil'},\n"
            f" next={self.next_page if self.next_page != 4294967295 else 'nil'},\n"
            f" lsn={self.lsn},\n"
            f" type={self.page_type.name},\n"
            f" flush_lsn={self.flush_lsn},\n"
            f" space_id={self.space_id}\n"
            ">"
        )

@dataclass
class FilTrailer:
    checksum: int
    lsn_low32: int

    @classmethod
    def parse(cls, page_data: bytes) -> 'FilTrailer':
        trailer = struct.unpack('>II', page_data[-8:])
        return cls(
            checksum=trailer[0],
            lsn_low32=trailer[1]
        )

    def format(self) -> str:
        return (
            "#<FilTrailer\n"
            f" checksum={self.checksum},\n"
            f" lsn_low32={self.lsn_low32}\n"
            ">"
        )
