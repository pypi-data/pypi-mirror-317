#--------------------------------------------------------------------------------
# 참조 모듈 목록.
#--------------------------------------------------------------------------------
from __future__ import annotations
from typing import Awaitable, Callable, Final, Generic, Iterable, Iterator, Optional, Sequence, Type, TypeVar, Tuple, Union
from typing import ItemsView, KeysView, ValuesView
from typing import IO, TextIO, BinaryIO
from typing import Any, List, Dict, Set
from typing import cast, overload
from .directorysearch import DirectorySearch
from .filesearch import FileSearch
from .idattribute import IdAttribute


#--------------------------------------------------------------------------------
# 프로퍼티 요소.
#--------------------------------------------------------------------------------
class Property:
	#--------------------------------------------------------------------------------
	# 멤버 변수 목록.
	#--------------------------------------------------------------------------------
	Id: IdAttribute
	Value: str
	Children: Optional[List[DirectorySearch, FileSearch]]