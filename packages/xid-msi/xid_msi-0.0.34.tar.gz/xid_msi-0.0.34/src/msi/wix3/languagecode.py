#--------------------------------------------------------------------------------
# 참조 모듈 목록.
#--------------------------------------------------------------------------------
from __future__ import annotations
from typing import Awaitable, Callable, Final, Generic, Iterable, Iterator, Optional, Sequence, Type, TypeVar, Tuple, Union
from typing import ItemsView, KeysView, ValuesView
from typing import IO, TextIO, BinaryIO
from typing import Any, List, Dict, Set
from typing import cast, overload
from enum import Enum


#--------------------------------------------------------------------------------
# 국가별 언어 코드.
#--------------------------------------------------------------------------------
class LanguageCode(Enum):
    KOREAN = 1042
    ENGLISH = 1033
    JAPANESE = 1041
    GERMAN = 1031
    SPANISH = 1034
    FRENCH = 1036