#--------------------------------------------------------------------------------
# 참조 모듈 목록.
#--------------------------------------------------------------------------------
from __future__ import annotations
from typing import Awaitable, Callable, Final, Generic, Iterable, Iterator, Optional, Sequence, Type, TypeVar, Tuple, Union
from typing import ItemsView, KeysView, ValuesView
from typing import IO, TextIO, BinaryIO
from typing import Any, List, Dict, Set
from typing import cast, overload


#--------------------------------------------------------------------------------
# 논리형 속성.
# - 일반적인 XML은 논리형에 대해서 문자열로 처리하며, True/False 대신 yes/no로 표현한다.
# - 또한 논리형 속성 자체는 선언했지만 값이 공백인 경우 및 속성 자체의 생략은 False로 처리한다.
#--------------------------------------------------------------------------------
class BooleanAttribute:
	#--------------------------------------------------------------------------------
	# 열거 요소 목록.
	#--------------------------------------------------------------------------------
	Value: bool


	#--------------------------------------------------------------------------------
	# 문자열 변환 오퍼레이터.
	#--------------------------------------------------------------------------------
	def __str__(self) -> str:
		if self.Value:
			return f"yes"
		else:
			return f"no"