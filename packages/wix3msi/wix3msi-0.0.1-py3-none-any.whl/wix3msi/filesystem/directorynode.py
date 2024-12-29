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
# 디렉토리 노드.
#--------------------------------------------------------------------------------
class DirectoryNode:
	#--------------------------------------------------------------------------------
	# 멤버 변수 목록.
	#--------------------------------------------------------------------------------
	__path: str # 대상 이름을 제외한 경로.
	__name: str # 대상 디렉토리 이름.
	__directories: List[INode] # 자식 디렉토리 목록.
	__files: List[INode] # 자식 파일 목록.


	#--------------------------------------------------------------------------------
	# 디렉토리 이름 프로퍼티. (인터페이스 구현)
	#--------------------------------------------------------------------------------
	@property
	def Name(self) -> str:
		return self.__name


	#--------------------------------------------------------------------------------
	# 노드 타입 프로퍼티. (인터페이스 구현)
	#--------------------------------------------------------------------------------
	@property
	def NodeType(self) -> NodeType:
		return NodeType.DIRECTORY
	

	#--------------------------------------------------------------------------------
	# 현재 디렉토리 이름을 제외한 경로 프로퍼티. (인터페이스 구현)
	#--------------------------------------------------------------------------------
	@property
	def Path(self) -> str:
		return self.__path
	

	#--------------------------------------------------------------------------------
	# 생성시 입력받았던 디렉토리 전체 경로 프로퍼티. (인터페이스 구현)
	#--------------------------------------------------------------------------------
	@property
	def Value(self) -> str:
		return os.path.join("{self.Path}", {self.Name})


	#--------------------------------------------------------------------------------
	# 자식 디렉토리 목록 프로퍼티.
	#--------------------------------------------------------------------------------
	@property
	def Directories(self) -> List[INode]:
		from .nodemanager import NodeManager
		nodeManager = NodeManager.GetSharedInstance()
		self.__directories.clear()
		for directory in os.listdir(self.Value):
			targetPath: str = os.path.join(self.Value, directory)
			if not os.path.isdir(targetPath):
				continue
			node: INode = nodeManager.CreateNode(targetPath)
			if not node:
				continue
			self.__directories.append(node)
		return self.__directories


	#--------------------------------------------------------------------------------
	# 자식 파일 목록 프로퍼티.
	#--------------------------------------------------------------------------------
	@property
	def Files(self) -> List[INode]:
		from .nodemanager import NodeManager
		nodeManager = NodeManager.GetSharedInstance()
		self.__files.clear()
		for directory in os.listdir(self.Value):
			targetPath: str = os.path.join(self.Value, directory)
			if not os.path.isfile(targetPath):
				continue
			node: INode = nodeManager.CreateNode(targetPath)
			if not node:
				continue
			self.__files.append(node)
		return self.__files
	

	#--------------------------------------------------------------------------------
	# 생성됨. (인터페이스 구현)
	#--------------------------------------------------------------------------------
	def OnCreate(self, targetPath: str) -> None:
		from .nodemanager import NodeManager
		if not NodeManager.ExistsDirectory(targetPath):
			raise FileNotFoundError(targetPath)

		self.__path: str = os.path.dirname(targetPath)
		self.__name: str = os.path.basename(targetPath)
		self.__directories = list()
		self.__files = list()


	#--------------------------------------------------------------------------------
	# 캐시 갱신. (오버라이드)
	#--------------------------------------------------------------------------------
	def Dirty(self) -> None:
		base = super()
		if not base.IsDirty():
			return		
		base.Dirty()