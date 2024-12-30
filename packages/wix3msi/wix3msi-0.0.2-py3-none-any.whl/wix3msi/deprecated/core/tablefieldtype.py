#--------------------------------------------------------------------------------
# 참조 모듈 목록.
#--------------------------------------------------------------------------------
from __future__ import annotations
from typing import Awaitable, Callable, Final, Generic, Iterable, Iterator, Optional, Sequence, Type, TypeVar, Tuple, Union
from typing import ItemsView, KeysView, ValuesView
from typing import IO, TextIO, BinaryIO
from typing import Any, List, Dict, Set
from typing import cast, overload
import builtins
from enum import Enum


#--------------------------------------------------------------------------------
# Microsoft Installer Table Field Type.
#--------------------------------------------------------------------------------
class TableFieldType(Enum):
	TEXT = "TEXT"		# 가변 길이의 문자열. (MSI 내부에서 필드마다 각각 다른 고정값 존재)
	INTEGER = "INTEGER"	# 32비트 정수 값.
	LONG = "LONG"		# 64비트 정수 값.
	OBJECT = "OBJECT"	# 바이너리데이터. (BLOB)