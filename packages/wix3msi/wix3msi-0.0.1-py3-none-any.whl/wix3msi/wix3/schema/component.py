#--------------------------------------------------------------------------------
# 참조 모듈 목록.
#--------------------------------------------------------------------------------
from __future__ import annotations
from typing import Awaitable, Callable, Final, Generic, Iterable, Iterator, Optional, Sequence, Type, TypeVar, Tuple, Union
from typing import ItemsView, KeysView, ValuesView
from typing import IO, TextIO, BinaryIO
from typing import Any, List, Dict, Set
from typing import cast, overload
from .createfolder import CreateFolder
from .file import File
from .guidattribute import GuidAttribute
from .idattribute import IdAttribute


#--------------------------------------------------------------------------------
# 컴포넌트 요소.
#--------------------------------------------------------------------------------
class Component:
	#--------------------------------------------------------------------------------
	# 멤버 변수 목록.
	#--------------------------------------------------------------------------------
	Id: IdAttribute
	Guid: GuidAttribute
	Directory: str
	Win64: bool
	Children: Optional[List[Union[CreateFolder, File]]]