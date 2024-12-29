#--------------------------------------------------------------------------------
# 참조 모듈 목록.
#--------------------------------------------------------------------------------
from __future__ import annotations
from typing import Awaitable, Callable, Final, Generic, Iterable, Iterator, Optional, Sequence, Type, TypeVar, Tuple, Union
from typing import ItemsView, KeysView, ValuesView
from typing import IO, TextIO, BinaryIO
from typing import Any, List, Dict, Set
from typing import cast, overload
from .content import Content


#--------------------------------------------------------------------------------
# 조건 요소.
# - 체크가 실패할 경우 Message가 메시지박스로 생성되면서 이후 설치가 중단된다. 조건 자체는 Content에 Text Value를 통해 설정할 수 있다.
# - 논리적인 조건: 인스톨되어있거나 삭제가 아니면서 맥스와 심플리곤이 다 설치되어 있는 경우.
# - 조건컨텐트 설정: <![CDATA[Installed OR (NOT REMOVE AND (CHECK_INSTALLED_AUTODESK3DSMAX2023 AND CHECK_INSTALLED_SIMPLYGON10))]]>
#--------------------------------------------------------------------------------
class Condition(Content):
	#--------------------------------------------------------------------------------
	# 멤버 변수 목록.
	#--------------------------------------------------------------------------------
	Message: str