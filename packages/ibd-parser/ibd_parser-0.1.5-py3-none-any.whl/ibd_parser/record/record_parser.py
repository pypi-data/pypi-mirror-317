from dataclasses import dataclass
from typing import List, Dict, Any, Optional
import struct

from flask import json
from ibd_parser.page.index import IndexHeader
from ibd_parser.record.record_header import RecordHeader
from ibd_parser.utils import parse_datetime

@dataclass
class Record:
    header: RecordHeader
    trx_id: int
    rollback_pointer: int
    data: Dict[str, Any]
    error: str = ""


class RecordParser(object):
    def __init__(
        self,
        page_data: bytes,
        page_header: IndexHeader,
        page_directory: List[int],
        schema: Optional[Dict[str, Any]] = None
    ):
        self.page_data = page_data
        self.page_header = page_header
        self.page_directory = page_directory
        self.schema = schema

    def parse_records(self) -> List[Record]:
        """Parse all records"""
        if not self.schema:
            print(":(records not dumped due to missing record describer or data dictionary)")
            return []

        records = []

        # Parse system records
        infimum = RecordHeader.parse(self.page_data, self.page_directory[0])
        supremum = RecordHeader.parse(self.page_data, self.page_directory[-1])
        # Traverse the record list starting from Infimum
        next_offset = infimum.next
        while next_offset != supremum.next:
            record = self.parse_record(self.page_data, next_offset)
            records.append(record)
            next_offset = record.header.next

        return records

    def parse_record(self, page_data: bytes, offset: int) -> Record:
        """Parse a record using the provided schema"""
        data_offset = offset
        header = RecordHeader.parse(page_data, data_offset)
        header_offset = data_offset - 5
        assert self.schema is not None, "Schema is not loaded"

        try:
            # Initialize parsed data
            parsed_data = Record(header=header, trx_id=0, rollback_pointer=0, data={})
            # 解析固定长度字段
            id_value = struct.unpack('>I', page_data[data_offset:data_offset+4])[0]
            id_value = id_value & ~0x80000000
            data_offset += 4
            parsed_data.data['id'] = id_value

            # Parse fixed fields (trx_id and rollback_pointer)
            trx_id_bytes = page_data[data_offset:data_offset+6]
            trx_id_bytes = b'\x00\x00' + trx_id_bytes
            trx_id_value = struct.unpack('>Q', trx_id_bytes)[0]
            data_offset += 6

            rollback_pointer_bytes = page_data[data_offset:data_offset+7]
            rollback_pointer_bytes = b'\x00' + rollback_pointer_bytes
            rollback_pointer_value = struct.unpack('>Q', rollback_pointer_bytes)[0]
            data_offset += 7

            parsed_data.trx_id = trx_id_value
            parsed_data.rollback_pointer = rollback_pointer_value

            # Parse null flags and variable-length field lengths
            null_flags_offset = header_offset - 1
            null_flags = page_data[null_flags_offset]
            var_lens = []
            null_flags_offset -= 1

            for field in self.schema['fields']:
                if field['type'] == 'varchar':
                    if page_data[null_flags_offset] < 128:  # 1-byte length
                        var_lens.append(page_data[null_flags_offset])
                        null_flags_offset -= 1
                    else:  # 2-byte length
                        var_lens.append(((page_data[null_flags_offset] & 0x3F) << 8) | page_data[null_flags_offset + 1])
                        null_flags_offset -= 2

            # Parse user-defined fields based on schema
            var_len_index = 0
            for field in self.schema['fields']:
                field_name = field['name']
                field_type = field['type']
                field_length = field['length']
                if field.get('primary_key', False):
                    continue

                if field_type == 'int':
                    value = struct.unpack('>I', page_data[data_offset:data_offset+field_length])[0]
                    value = value & ~0x80000000
                    data_offset += field_length
                elif field_type == 'varchar':
                    var_len = var_lens[var_len_index]
                    value = page_data[data_offset:data_offset+var_len].decode('utf8')
                    data_offset += var_len
                    if page_data[data_offset] == 0x99:
                        data_offset += 1
                    var_len_index += 1
                elif field_type == 'tinyint':
                    value = page_data[data_offset] - 128
                    data_offset += field_length
                elif field_type == 'datetime':
                    datetime_bytes = page_data[data_offset:data_offset+field_length]
                    value = parse_datetime(struct.unpack('>I', datetime_bytes)[0])
                    data_offset += field_length
                else:
                    raise ValueError(f"Unsupported field type: {field_type}")

                parsed_data.data[field_name] = value

            return parsed_data

        except Exception as e:
            return Record(header=header, trx_id=0, rollback_pointer=0, data={}, error=str(e))
