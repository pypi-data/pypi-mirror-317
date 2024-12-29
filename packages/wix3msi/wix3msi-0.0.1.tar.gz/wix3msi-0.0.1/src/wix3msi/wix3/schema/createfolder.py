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
import os
import re
import uuid
from xml.dom import minidom as Minidom
from xml.dom.minidom import Document as MinidomDocument
from xml.etree import ElementTree
from xml.etree.ElementTree import Element
from .idattribute import IdAttribute


#--------------------------------------------------------------------------------
# 폴더생성 요소.
# - Component의 자식으로 들어갈 수 있으며, 지정한 디렉토리 요소의 경로에 디렉토리가 없으면 생성해준다.
#--------------------------------------------------------------------------------
class CreateFolder:
	#--------------------------------------------------------------------------------
	# 멤버 변수 목록.
	#--------------------------------------------------------------------------------
	Directory: IdAttribute # 디렉토리 요소의 고유식별자.