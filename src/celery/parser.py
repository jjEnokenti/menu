import uuid
from typing import Any

import openpyxl
from _decimal import Decimal

from src.celery.google_cloud_connect import get_data_from_cloud
from src.config import settings


class Parser:

    def __init__(self, mode):
        if mode == 'CLOUD':
            self.data = get_data_from_cloud()
            self.get_data = self._parse_cloud_data(self.data)
        else:
            self.data = openpyxl.load_workbook(settings.ADMIN_FILE_PATH).active
            self.get_data = self._parse_local_data(self.data)

    def _parse_local_data(self, data) -> list:
        """Local file parser."""

        res_data = []

        for row in data.iter_rows():
            if row[0].value and self._is_valid_uuid(row[0].value):
                res_data.append(self._to_dict(*[item.value for item in row[:3]]))
            elif row[1].value and self._is_valid_uuid(row[1].value):
                res_data[-1]['submenus'] = res_data[-1].get('submenus', []) + [
                    self._to_dict(
                        *[item.value for item in row[1:4]])
                ]
            elif row[2].value and self._is_valid_uuid(row[2].value):
                res_data[-1]['submenus'][-1]['dishes'] = res_data[-1]['submenus'][-1].get('dishes', []) + [
                    self._to_dict(
                        *[item.value for item in row[2:7]]
                    )
                ]

        return res_data

    def _parse_cloud_data(self, data):
        """Cloud api sheet parser."""

        res_data = []

        for row in data:
            if row[0] and self._is_valid_uuid(row[0]):
                res_data.append(self._to_dict(*row[:3]))
            elif row[1] and self._is_valid_uuid(row[1]):
                res_data[-1]['submenus'] = res_data[-1].get('submenus', []) + [self._to_dict(*row[1:4])]
            elif row[2] and self._is_valid_uuid(row[2]):
                res_data[-1]['submenus'][-1]['dishes'] = res_data[-1]['submenus'][-1].get('dishes', []) + [
                    self._to_dict(*row[2:7])
                ]

        return res_data

    @staticmethod
    def _to_dict(uid=None, title=None, description=None, price=None, discount=None, *args, **kwargs) -> dict:
        """Dict maker serializer."""

        result = {
            'id': uuid.UUID(uid),
            'title': title,
            'description': description,
        }

        if price:
            result['price'] = Decimal(price).quantize(Decimal('0.00'))
        if discount:
            if isinstance(discount, (int, float)):
                if discount < 100:
                    result['discount'] = Decimal(price - price * discount / 100).quantize(Decimal('0.00'))
                else:
                    result['discount'] = Decimal(0.00).quantize(Decimal('0.00'))
        return result

    @staticmethod
    def _is_valid_uuid(uuid_str: Any) -> bool:
        """Uuid validator."""
        try:
            uuid_obj = uuid.UUID(uuid_str)
            return str(uuid_obj) == uuid_str
        except ValueError:
            return False
