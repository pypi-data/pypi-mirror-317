from dataclasses import dataclass
import struct
from typing import Dict, Any

from ibd_parser.constants import RecordType, PAGE_SIZE

@dataclass
class RecordHeader:
    delete_mark: bool
    min_rec_flag: bool
    n_owned: int
    record_type: RecordType
    heap_no: int
    next: int

    @classmethod
    def parse(cls, page_data: bytes, offset: int) -> 'RecordHeader':
        """Parse the record header information (5 bytes)"""
        # Unpack the first 3 bytes and the next pointer
        byte1, byte2, byte3, next_ptr = struct.unpack('>3BH', page_data[offset-5:offset])

        # Parse the first byte (8 bits)
        delete_mark = (byte1 >> 7) & 0x01        # Highest bit
        min_rec_flag = (byte1 >> 6) & 0x01       # Second highest bit
        n_owned = byte1 & 0x0F                   # Last 4 bits

        # Heap number spans the 2nd and 3rd bytes (13 bits)
        heap_no = (byte2 << 5) | (byte3 >> 3)

        # Record type is the lowest 3 bits of the 3rd byte
        record_type = RecordType.CONVENTIONAL
        if offset == 99:  # Infimum record
            record_type = RecordType.INFIMUM
        elif offset == 112:  # Supremum record
            record_type = RecordType.SUPREMUM

        return cls(
            delete_mark=delete_mark,
            min_rec_flag=min_rec_flag,
            n_owned=n_owned,
            record_type=record_type,
            heap_no=heap_no,
            next=(offset + next_ptr) % 65536
        )

    def format_as_string(self) -> str:
        return (
            "#<RecordHeader\n"
            f" delete_mark={self.delete_mark},\n"
            f" min_rec_flag={self.min_rec_flag},\n"
            f" n_owned={self.n_owned},\n"
            f" record_type={self.record_type.name},\n"
            f" heap_no={self.heap_no},\n"
            f" next={self.next}\n"
            ">"
        )
