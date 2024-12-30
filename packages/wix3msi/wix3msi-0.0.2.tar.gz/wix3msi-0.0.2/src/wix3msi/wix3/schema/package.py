#--------------------------------------------------------------------------------
# 참조 모듈 목록.
#--------------------------------------------------------------------------------
from __future__ import annotations
from typing import Awaitable, Callable, Final, Generic, Iterable, Iterator, Optional, Sequence, Type, TypeVar, Tuple, Union
from typing import ItemsView, KeysView, ValuesView
from typing import IO, TextIO, BinaryIO
from typing import Any, List, Dict, Set
from typing import cast, overload
from .booleanattribute import BooleanAttribute


#--------------------------------------------------------------------------------
# 패키지 요소.
#--------------------------------------------------------------------------------
class Package:
	#--------------------------------------------------------------------------------
	# 멤버 변수 목록.
	#--------------------------------------------------------------------------------
	InstallVersion: str
	InstallPrivileges: str
	Compressed: BooleanAttribute
	InstallScope: str
	Platform: str