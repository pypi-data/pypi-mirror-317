# adaptyper

Старается конвертировать один тип данных в другой.

Обработка пользовательских данных из не строго типизированных значений.

```py
from adaptyper import convert, ValueType

# to
convert('FaLsE').to(ValueType.BOOL)  # False
convert('any_str_value').to('bool')  # True
convert(0).to('bool')  # False
convert(1.0).to('bool')  # True

convert(True).to(ValueType.STR)  # "TRUE"
convert(-1).to('str')  # "-1"

convert(True).to(ValueType.FLOAT)  # 1.0
convert('FaLsE').to('float')  # 0.0
convert('.5').to('float')  # 0.5
convert(-1).to('float')  # -1.0

convert(True).to(ValueType.INT)  # 1
convert('1.5').to('int')  # 1
convert('1.5').to('int', True)  # 2

convert('2011-11-04').to(ValueType.DATETIME)  # datetime(2011, 11, 4, 0, 0)
convert('4.11.2011').to('datetime', '%d.%m.%Y')  # datetime(2011, 11, 4, 0, 0)

convert('2011-11-04').to(ValueType.DATE)  # date(2011, 11, 4)
convert('4.11.2011').to('date', '%d.%m.%Y')  # date(2011, 11, 4)

convert('.00').to(ValueType.DECIMAL)  # Decimal('0.00')
convert('.5').to('decimal')  # Decimal('0.5')
convert(-1).to('decimal')  # Decimal('-1')
convert("- 123 \xa0 456").to('decimal')  # Decimal('-123456')

# bool
convert('').to_bool()  # False
convert('0').to_bool()  # False
convert('FaLsE').to_bool()  # False
convert('any_str_value').to_bool()  # True

# str
convert(True).to_str()  # "TRUE"
convert('any_str_value').to_str()  # "any_str_value"
convert(1).to_str()  # "1"
convert(-1).to_str()  # "-1"
convert(123.456).to_str()  # "123.456"
convert(-123.456).to_str()  # "-123.456"

# float
convert(None).to_float()  # None
convert('').to_float()  # None
convert('123,456').to_float()  # 123.456
convert(' 123\xa0456\xa0').to_float()  # 123456.0
convert('tRuE').to_float()  # 1.0
convert(True).to_float()  # 1.0
convert(1).to_float()  # 1.0
convert('.3').to_float()  # 0.3

# int
# работает через float,
# банковское округление (по-умолчанию False)
convert('.6').to_int()  # 0
convert('.6').to_int(bankers_rounding=True)  # 1
convert('1.5').to_int(False)  # 1
convert('1.5').to_int(True)  # 2

# datetime
convert(None).to_datetime()  # None
convert('').to_datetime()  # None
convert('2011-11-04').to_datetime()  # datetime(2011, 11, 4, 0, 0)
convert('4.11.2011').to_datetime('%d.%m.%Y')  # datetime(2011, 11, 4, 0, 0)

# date
# работает через datetime
convert(None).to_date()  # None
convert('').to_date()  # None
convert('2011-11-04').to_date()  # date(2011, 11, 4)
convert('4.11.2011').to_date('%d.%m.%Y')  # date(2011, 11, 4)

# decimal
convert('.00').to(ValueType.DECIMAL)  # Decimal('0.00')
convert('.5').to('decimal')  # Decimal('0.5')
convert(-1).to('decimal')  # Decimal('-1')
convert(123456).to('decimal')  # Decimal('123456')
convert("- 123 456").to('decimal')  # Decimal('-123456')
convert("123\xa0456").to('decimal')  # Decimal('123456')
```

[![PyPI Downloads](https://static.pepy.tech/badge/adaptyper/week)](https://pepy.tech/projects/adaptyper)
[![PyPI Downloads](https://static.pepy.tech/badge/adaptyper/month)](https://pepy.tech/projects/adaptyper)
[![PyPI Downloads](https://static.pepy.tech/badge/adaptyper)](https://pepy.tech/projects/adaptyper)