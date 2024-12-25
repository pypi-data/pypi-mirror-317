"""
# GW core

`gw-sys-core.gwis`

`gwis` - gw identification system

`created by KeyisB`

gw sys version -  [`0.0.0.0.4`]
"""


import typing as _typing

from .Exceptions import Exceptions

__ALPHABET = "0GWFromKeyisBI69XSRdpLTnN1UgHqVtK5EcCAhfwvD7jzb2ZQxPJua83MY4"
__BASE = len(__ALPHABET)

TYPES = {
    'g': {'id': 0, 'canAuth': True}, # global id
    's': {'id': 1, 'canAuth': True}, # server
    'u': {'id': 2, 'canAuth': True}, # user
    'c': {'id': 3, 'canAuth': False}, # company
    'p': {'id': 4, 'canAuth': False} # project
}

_TYPES_BY_ID = {value['id']: key for key, value in TYPES.items()}


class IDTypes():
    def getTypeFromID(self, id_: _typing.Union[int, str]):
        if isinstance(id_, int): # if id is globally
            return 'g'
        
        if '-' in id_: # if id correct
            id_type, id_value = id_.split('-')
            return id_type
        
        raise Exceptions.IncorrectIdType()
    
    def isCanAuth(self, id_: _typing.Union[int, str]) -> bool:

        if isinstance(id_, int):
            id__ = self.convertIDFromIntToString(id_)
        else:
            id__ = id_

        return TYPES[id__]['canAuth'] # type: ignore
    
    def convertIDFromStringToInt(self, id_: str) -> _typing.Optional[int]:
        return TYPES.get(id_, {}).get('id', None)
    
    def convertIDFromIntToString(self, id_: int):
        return _TYPES_BY_ID.get(id_, None)
            




def _int_to_base(num: int) -> str:
    if num == 0:
        return __ALPHABET[0]
    result = []
    while num > 0:
        result.append(__ALPHABET[num % __BASE])
        num //= __BASE
    return ''.join(reversed(result))

def _base_to_int(base_str: str) -> int:
    num = 0
    for char in base_str:
        num = num * __BASE + __ALPHABET.index(char)
    return num

class IDConverter:
    def __init__(self):
        self.__cache_to_int: _typing.Dict[str, int] = {}
        self.__cache_to_short: _typing.Dict[int, str] = {}
        self.__useCache = False

    def type(self, id_: _typing.Union[str, int]):
        if isinstance(id_, int):
            return 'n'
        elif '-' in id_:
            return 'f'
        else:
            return's'

    def convert(self, id_value: _typing.Union[str, int], target_format: str, prefix: _typing.Optional[str] = None) -> _typing.Union[str, int]:
        """
        Конвертирует ID в указанный формат.

        :param id_value: ID (полный, короткий или числовой).

        :param target_format: Формат для преобразования ('f', 's', 'n').

        :return: Конвертированный ID.
        
        """
        if isinstance(id_value, int):
            # Числовой формат
            if target_format == 's':
                return self.int_to_short(id_value)
            elif target_format == 'f':
                if prefix is None:
                    raise ValueError("Для полного ID необходим префикс типа объекта.")
                return f"{prefix}-{self.int_to_short(id_value)}"
            elif target_format == 'n':
                return id_value

        elif '-' in id_value:
            # Полный формат (например, u-4c92)
            prefix, short_id = id_value.split('-')
            if target_format == 's':
                return short_id
            elif target_format == 'n':
                return self.short_to_int(short_id)
            elif target_format == 'f':
                return id_value

        else:
            # Короткий формат (например, 4c92)
            if target_format == 'n':
                return self.short_to_int(id_value)
            elif target_format == 's':
                return id_value
            elif target_format == 'f':
                if prefix is None:
                    raise ValueError("Для полного ID необходим префикс типа объекта.")
                return f"{prefix}-{id_value}"

        raise ValueError("Неверный формат ID или целевой формат.")

    def full_to_short(self, full_id: str) -> str:
        """Конвертирует ID вида u-4c92 в короткий формат 4c92."""
        prefix, short_id = full_id.split('-')
        return short_id

    def short_to_int(self, short_id: str) -> int:
        """Конвертирует короткий ID 4c92 в числовой формат 1000000."""
        if self.__useCache:
            if short_id not in self.__cache_to_int:
                self.__cache_to_int[short_id] = _base_to_int(short_id)
            return self.__cache_to_int[short_id]
        else:
            return _base_to_int(short_id)

    def int_to_short(self, num: int) -> str:
        """Конвертирует числовой ID 1000000 в короткий формат 4c92."""
        if self.__useCache:
            if num not in self.__cache_to_short:
                short_id = _int_to_base(num)
                self.__cache_to_short[num] = short_id
            return self.__cache_to_short[num]
        else:
            return _int_to_base(num)

    def full_identify(self, full_id: str) -> str:
        """Определяет тип объекта по префиксу (u, o, p и т.д.)."""
        return full_id.split('-')[0]

    def clearCache(self):
        """Очищает кэшированные данные."""
        self.__cache_to_int.clear()
        self.__cache_to_short.clear()

    def enabledCache(self):
        """Включает кэширование."""
        self.__useCache = True

    def disabledCache(self):
        """Выключает кэширование."""
        self.__useCache = False















