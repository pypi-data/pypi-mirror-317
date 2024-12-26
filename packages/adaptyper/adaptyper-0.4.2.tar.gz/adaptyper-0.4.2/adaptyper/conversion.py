import re
from datetime import datetime, date
from decimal import Decimal
from enum import Enum, auto
from typing import Union


class ConvertValueException(Exception): ...


class PreConvertFuncException(Exception): ...


class ConvertToBoolException(Exception): ...


class ConvertToStrException(Exception): ...


class ConvertToIntException(Exception): ...


class ConvertToFloatException(Exception): ...


class ConvertToDatetimeException(Exception): ...


class ConvertToDateException(Exception): ...


class ConvertToDecimalException(Exception): ...


class NotSupportedValueType(Exception): ...


class NotSupportedTargetType(Exception): ...


class ValueType(Enum):
    BOOL = auto()
    STR = auto()
    INT = auto()
    FLOAT = auto()
    DATETIME = auto()
    DATE = auto()
    DECIMAL = auto()


class Convert:
    def __init__(self, value: Union[str, int, float, bool, None]):
        self.value = value

    def to_float(
        self,
        additional_info=None,
        pre_convert_func=None,
        *args,
        **kwargs,
    ) -> float | None:
        return _to_float(self.value, additional_info, pre_convert_func, *args, **kwargs)

    def to_int(
        self,
        bankers_rounding: bool = False,
        pre_convert_func=None,
        *args,
        **kwargs,
    ) -> int | None:
        return _to_int(
            value=self.value,
            bankers_rounding=bankers_rounding,
            pre_convert_func=pre_convert_func,
            *args,
            **kwargs,
        )

    def to_str(
        self,
        additional_info=None,
        pre_convert_func=None,
        *args,
        **kwargs,
    ) -> str | None:
        return _to_str(
            value=self.value,
            additional_info=additional_info,
            pre_convert_func=pre_convert_func,
            *args,
            **kwargs,
        )

    def to_bool(
        self,
        additional_info=None,
        pre_convert_func=None,
        *args,
        **kwargs,
    ) -> bool | None:
        return _to_bool(
            value=self.value,
            additional_info=additional_info,
            pre_convert_func=pre_convert_func,
            *args,
            **kwargs,
        )

    def to_datetime(
        self,
        datetime_format=None,
    ) -> datetime | None:
        return _to_datetime(
            value=self.value,
            datetime_format=datetime_format,
        )

    def to_date(
        self,
        date_format=None,
    ) -> date | None:
        return _to_date(
            value=self.value,
            date_format=date_format,
        )

    def to_decimal(
        self,
        pre_convert_func=None,
        additional_info=None,
    ) -> Decimal | None:
        return _to_decimal(
            value=self.value,
            additional_info=additional_info,
            pre_convert_func=pre_convert_func,
        )

    def to(
        self,
        target_type: Union[ValueType, str],
        additional_info=None,
    ):
        return _to(
            target_type=target_type,
            value=self.value,
            additional_info=additional_info,
        )


def __pre_action(value, func, *args, **kwargs):
    """
    Выполнение пользовательской функции перед конвертацией

    :param value: данные
    :param func: пользовательская функция
    :return: обработанные пользовательской функцией данные
    """
    try:
        return func(value, *args, **kwargs)
    except Exception as e:
        raise PreConvertFuncException(e)


def _to_float(
    value: None | bool | str | int | float,
    additional_info=None,
    pre_convert_func=None,
    *args,
    **kwargs,
) -> float | None:
    """
    Конвертация значения в тип float.

    :param pre_convert_func: Пользовательская функция, вызываемая до конвертации
    :param value: строковое значение
    :return: float
    """

    if pre_convert_func:
        value = __pre_action(value, pre_convert_func, *args, **kwargs)

    try:
        if value is None:
            return None

        elif isinstance(value, bool):
            return 1.0 if value else 0.0

        elif isinstance(value, str):
            if value == "":
                return None

            if value.upper() == "TRUE":
                return 1.0
            elif value.upper() == "FALSE":
                return 0.0

            # Удаляем все пробелы и неразрывные пробелы
            value = re.sub(r"[\s\xa0\x20]+", "", value)

            # Заменяем первую запятую на точку
            value = re.sub(",", ".", value, 1)

            return float(value)

        elif isinstance(value, int):
            return float(value)

        elif isinstance(value, float):
            return value

        else:
            raise NotSupportedValueType((type(value), value))

    except Exception as e:
        raise ConvertToFloatException(e)


def _to_int(
    value: None | bool | str | int | float,
    bankers_rounding: bool = False,
    pre_convert_func=None,
    *args,
    **kwargs,
) -> int | None:
    """
    Конвертация значения в тип int. Банковское округление.

    Значения с плавающей точкой нужно сначала перевести во float формат.


    :param value:
    :param pre_convert_func:
    :param bankers_rounding: Алгоритм банковского округления
    :param args:
    :param kwargs:
    :return: int
    """
    if pre_convert_func:
        value = __pre_action(value, pre_convert_func, *args, **kwargs)

    try:
        if value is None:
            return None

        if not isinstance(value, (type(None), bool, str, int, float)):
            raise NotSupportedValueType((type(value), value))

        elif isinstance(value, str):
            if value == "":
                return None

        if bankers_rounding:
            return round(_to_float(value, pre_convert_func, *args, **kwargs))
        else:
            return int(_to_float(value, pre_convert_func, *args, **kwargs))

    except Exception as e:
        raise ConvertToIntException(e)


def _to_str(
    value: None | bool | str | int | float,
    additional_info=None,
    pre_convert_func=None,
    *args,
    **kwargs,
) -> str | None:
    """
    Конвертация значения в тип str.

     :param value: Значение
     :param additional_info: дополнительная информация к типу данных
     :param pre_convert_func: пользовательская функция обработки значения до конвертации
     :param args:
     :param kwargs:
     :return:
    """

    if pre_convert_func:
        value = __pre_action(value, pre_convert_func, *args, **kwargs)

    try:
        if value is None:
            return None

        elif isinstance(value, bool):
            return "TRUE" if value else "FALSE"

        elif isinstance(value, str):
            return value

        elif isinstance(value, int):
            return str(value)

        elif isinstance(value, float):
            return str(value)

        else:
            raise NotSupportedValueType((type(value), value))

    except Exception as e:
        raise ConvertToStrException(e)


def _to_bool(
    value: None | bool | str | int | float,
    additional_info=None,
    pre_convert_func=None,
    *args,
    **kwargs,
) -> bool | None:
    """
    Конвертация значения в тип bool.

    :param value: Значение
    :param additional_info: дополнительная информация
    :param pre_convert_func: пользовательская функция перед конвертацией
    :param args: *
    :param kwargs: **
    :return:
    """
    if pre_convert_func:
        value = __pre_action(value, pre_convert_func, *args, **kwargs)

    try:
        if value is None:
            return None

        elif isinstance(value, bool):
            return value

        elif isinstance(value, str):
            if value.upper() == "FALSE" or value == "0" or value == "":
                return False
            else:
                return True

        elif isinstance(value, int):
            return True if value != 0 else False

        elif isinstance(value, float):
            return True if value != 0.0 else False

        else:
            raise NotSupportedValueType((type(value), value))

    except Exception as e:
        raise ConvertToBoolException(e)


def _to_datetime(
    value: ValueType.STR,
    datetime_format=None,
) -> datetime | None:
    """
    Конвертация значения в тип datetime.

    Коды формата https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes

    :param value: значение
    :param datetime_format: формат даты в значении
    :return: datetime
    """
    try:
        if value is None:
            return None

        elif isinstance(value, str):
            if value == "":
                return None
            if datetime_format:
                return datetime.strptime(value, datetime_format)
            else:
                return datetime.fromisoformat(value)

        else:
            raise NotSupportedValueType((type(value), value))

    except Exception as e:
        raise ConvertToDatetimeException(e)


def _to_date(
    value: ValueType.STR,
    date_format: str = None,
) -> date | None:
    """
    Конвертация значения в тип date.

    Коды формата https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes

    :param value: значение
    :param date_format: формат даты в значении
    :return: date
    """

    try:
        if value is None:
            return None

        elif isinstance(value, str):
            if value == "":
                return None

        return _to_datetime(value, date_format).date()

    except Exception as e:
        raise ConvertToDateException(e)


def _to_decimal(
    value: None | str | int,
    additional_info=None,
    pre_convert_func=None,
    *args,
    **kwargs,
) -> Decimal | None:
    """
    Конвертация значения в тип Decimal.

    :param pre_convert_func: Пользовательская функция, вызываемая до конвертации
    :param value: обрабатываемое значение
    :return: Decimal
    """
    if pre_convert_func:
        value = __pre_action(value, pre_convert_func, *args, **kwargs)

    try:
        if value is None:
            return None

        elif isinstance(value, int):
            return Decimal(value)

        elif isinstance(value, str):
            if value == "":
                return None

            # Удаляем все пробелы и неразрывные пробелы
            value = re.sub(r"[\s\xa0\x20]+", "", value)

            # Заменяем первую запятую на точку
            value = re.sub(",", ".", value, 1)

            return Decimal(value)

        else:
            raise NotSupportedValueType((type(value), value))

    except Exception as e:
        raise ConvertToDecimalException(e)


def _to(
    target_type: Union[ValueType, str],
    value,
    additional_info=None,
):
    """
    Конвертация значения в нужный тип

    :param value: значение
    :param target_type: конвертировать в этот тип (может быть строкой или элементом ValueType)
    :param additional_info: дополнительная информация к типу
    :return:
    """
    try:
        if isinstance(target_type, str):
            to_type = {
                "bool": _to_bool,
                "str": _to_str,
                "int": _to_int,
                "float": _to_float,
                "datetime": _to_datetime,
                "date": _to_date,
                "decimal": _to_decimal,
            }

            if target_type not in to_type:
                raise NotSupportedTargetType(f"{target_type=}")

            return to_type[target_type](value, additional_info)

        else:
            to_type = {
                ValueType.BOOL: _to_bool,
                ValueType.STR: _to_str,
                ValueType.INT: _to_int,
                ValueType.FLOAT: _to_float,
                ValueType.DATETIME: _to_datetime,
                ValueType.DATE: _to_date,
                ValueType.DECIMAL: _to_decimal,
            }

            return to_type[target_type](value, additional_info)

    except Exception as e:
        raise ConvertValueException(e)
