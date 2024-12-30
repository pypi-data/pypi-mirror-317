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
import os
from .inode import INode
from .nodetype import NodeType


#--------------------------------------------------------------------------------
# 파일 노드.
#--------------------------------------------------------------------------------
class FileNode(INode):
	#--------------------------------------------------------------------------------
	# 멤버 변수 목록.
	#--------------------------------------------------------------------------------
	__path: str # 대상 이름을 제외한 경로.
	__name: str # 대상 파일 이름.
	__extension: str # 대상 파일 확장자.


	#--------------------------------------------------------------------------------
	# 이름 프로퍼티. (인터페이스 구현)
	#--------------------------------------------------------------------------------
	@property
	def Name(self) -> str:
		return self.__name


	#--------------------------------------------------------------------------------
	# 노드 타입 프로퍼티. (인터페이스 구현)
	#--------------------------------------------------------------------------------
	@property
	def NodeType(self) -> NodeType:
		return NodeType.FILE
	
	
	#--------------------------------------------------------------------------------
	# 현재 파일 이름을 제외한 경로 프로퍼티. (인터페이스 구현)
	#--------------------------------------------------------------------------------
	@property
	def Path(self) -> str:
		return self.__path


	#--------------------------------------------------------------------------------
	# 생성시 입력받았던 파일 전체 경로 프로퍼티. (인터페이스 구현)
	#--------------------------------------------------------------------------------
	@property
	def Value(self) -> str:
		return os.path.join(self.Path, self.Name, self.Extension)


	#--------------------------------------------------------------------------------
	# 파일 이름 프로퍼티.
	#--------------------------------------------------------------------------------
	@property
	def FileName(self) -> str:
		return f"{self.Name}{self.Extension}"


	#--------------------------------------------------------------------------------
	# 확장자 프로퍼티.
	#--------------------------------------------------------------------------------
	@property
	def Extension(self) -> str:
		return self.__extension


	#--------------------------------------------------------------------------------
	# 생성됨. (인터페이스 구현)
	#--------------------------------------------------------------------------------
	def OnCreate(self, targetPath: str) -> None:
		from .nodemanager import NodeManager
		if not NodeManager.ExistsFile(targetPath):
			raise FileNotFoundError(targetPath)
		self.__name, self.__extension = os.path.splitext(os.path.basename(targetPath))
		self.__path: str = os.path.dirname(targetPath)


	#--------------------------------------------------------------------------------
	# 캐시 갱신. (오버라이드)
	#--------------------------------------------------------------------------------
	def Dirty(self) -> None:
		base = super()
		if not base.IsDirty():
			return		
		base.Dirty()