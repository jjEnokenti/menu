import uuid
from typing import Any

import openpyxl
from _decimal import Decimal


class Parser:

    def __init__(self, file_path):
        self.path = file_path
        self.wb = openpyxl.load_workbook(self.path)
        self.active_sheet = self.wb.active

    def parse_obj(self) -> list:
        """File parser."""

        data = []

        for row in self.active_sheet.iter_rows():
            if row[0].value and self.is_valid_uuid(row[0].value):
                data.append(self.to_dict(*row[:3]))
            elif row[1].value and self.is_valid_uuid(row[1].value):
                data[-1]['submenus'] = data[-1].get('submenus', []) + [self.to_dict(*row[1:4])]
            elif row[2].value and self.is_valid_uuid(row[2].value):
                data[-1]['submenus'][-1]['dishes'] = data[-1]['submenus'][-1].get('dishes', []) + [
                    self.to_dict(*row[2:6])
                ]

        return data

    @staticmethod
    def to_dict(uid=None, title=None, description=None, price=None, *args, **kwargs) -> dict:
        """Openpyxl object to dict serializer."""

        result = {
            'id': uuid.UUID(uid.value),
            'title': title.value,
            'description': description.value,
        }

        if price:
            result['price'] = Decimal(price.value).quantize(Decimal('0.00'))

        return result

    @staticmethod
    def is_valid_uuid(uuid_str: Any) -> bool:
        """Uuid validator."""
        try:
            uuid_obj = uuid.UUID(uuid_str)
            return str(uuid_obj) == uuid_str
        except ValueError:
            return False
