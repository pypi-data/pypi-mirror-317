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
from abc import ABCMeta as InterfaceMetaClass
from xpl import Interface, abstractmethod, BaseMetaClass
from .nodetype import NodeType

#--------------------------------------------------------------------------------
# 클래스 생성을 막는 메타 클래스.
#--------------------------------------------------------------------------------
class NodeMetaClass(BaseMetaClass, InterfaceMetaClass):
	#--------------------------------------------------------------------------------
	# 객체를 함수로 호출 해주는 오퍼레이터.
	#--------------------------------------------------------------------------------
	def __call__(classType, *argumentList, **argumentDictionary) -> None:
		raise ValueError("Node Instantiate Failed. (Try to NodeManager)")


#--------------------------------------------------------------------------------
# 인터페이스.
#--------------------------------------------------------------------------------
class INode(Interface, metaclass = NodeMetaClass):
	#--------------------------------------------------------------------------------
	# 멤버 변수 목록.
	#--------------------------------------------------------------------------------
	__parent: INode
	__isDirty: bool


	#--------------------------------------------------------------------------------
	# 생성 오퍼레이터.
	#--------------------------------------------------------------------------------
	def __new__(classType, *argumentList, **argumentDictionary) -> Any:
		if classType is INode:
			raise TypeError("Node Instantiate Failed. (INode is Interface)")
		if not argumentDictionary.get("_from_manager", False):
			raise ValueError("Node Instantiate Failed. (Try to NodeManager)")
		base = super()
		return base.__new__(classType)


	#--------------------------------------------------------------------------------
	# 생성됨 오퍼레이터.
	#--------------------------------------------------------------------------------
	def __init__(self, targetPath: str) -> None:
		self.__parent = None
		self.__isDirty = False


	#--------------------------------------------------------------------------------
	# 동일 여부 비교 오퍼레이터.
	#--------------------------------------------------------------------------------
	def __eq__(self, targetPath: Union[INode, str]) -> bool:
		from .nodemanager import NodeManager
		return NodeManager.Equals(self, targetPath)


	#--------------------------------------------------------------------------------
	# 문자열 변환 오퍼레이터.
	#--------------------------------------------------------------------------------
	def __str__(self) -> str:
		return self.Value
	

	#--------------------------------------------------------------------------------
	# 부모 디렉토리 프로퍼티.
	#--------------------------------------------------------------------------------
	@property
	def Parent(self) -> INode:
		if not self.Path:
			return None
		if self.__parent:
			return self.__parent
		
		from .nodemanager import NodeManager
		nodeManager = NodeManager.GetSharedInstance()
		self.__parent = nodeManager.CreateNode(self.Path)
		return self.__parent


	#--------------------------------------------------------------------------------
	# 캐시 갱신.
	#--------------------------------------------------------------------------------
	def Dirty(self) -> None:
		if self.__isDirty:
			return

		self.OnDirty()
		self.__isDirty = True


	#--------------------------------------------------------------------------------
	# 캐시 갱신 여부.
	#--------------------------------------------------------------------------------
	def IsDirty(self) -> bool:
		return self.__isDirty


	#--------------------------------------------------------------------------------
	# 파일/디렉토리 이름 프로퍼티. (파일의 경우 확장자 제외)
	#--------------------------------------------------------------------------------
	@property
	@abstractmethod
	def Name(self) -> str: pass


	#--------------------------------------------------------------------------------
	# 노드 타입 프로퍼티.
	#--------------------------------------------------------------------------------
	@property
	@abstractmethod
	def NodeType(self) -> NodeType: pass


	#--------------------------------------------------------------------------------
	# 현재 파일/디렉토리 이름을 제외한 경로 프로퍼티.
	#--------------------------------------------------------------------------------
	@property
	@abstractmethod
	def Path(self) -> str: pass


	#--------------------------------------------------------------------------------
	# 생성시 입력받았던 파일/디렉토리 전체 경로 프로퍼티.
	#--------------------------------------------------------------------------------
	@property
	@abstractmethod
	def Value(self) -> str: pass


	#--------------------------------------------------------------------------------
	# 생성됨.
	#--------------------------------------------------------------------------------
	@abstractmethod
	def OnCreate(self, targetPath: str) -> None: pass


	#--------------------------------------------------------------------------------
	# 파괴됨.
	#--------------------------------------------------------------------------------
	@abstractmethod
	def OnDestroy(self) -> None: pass


	#--------------------------------------------------------------------------------
	# 캐시 갱신됨.
	#--------------------------------------------------------------------------------
	@abstractmethod
	def OnDirty(self) -> None: pass