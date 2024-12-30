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
from builtins import object as Object
import os
from xpl import SharedClass
from .directorynode import DirectoryNode
from .filenode import FileNode
from .inode import INode
from .nodetype import NodeType


#--------------------------------------------------------------------------------
# 노드 매니저.
#--------------------------------------------------------------------------------
class NodeManager(SharedClass):
	#--------------------------------------------------------------------------------
	# 멤버 변수 목록.
	#--------------------------------------------------------------------------------
	__nodes: dict[str, INode] = dict()


	#--------------------------------------------------------------------------------
	# 노드 목록 프로퍼티. (읽기 전용으로 수정해도 영향 없음)
	#--------------------------------------------------------------------------------
	@property
	def Nodes(self) -> List[INode]:
		values: ValuesView = self.__nodes.values()
		valueList = list(values)
		return valueList
	

	#--------------------------------------------------------------------------------
	# 생성됨.
	#--------------------------------------------------------------------------------
	def __init__(self) -> None:
		self.__nodes = dict()


	#--------------------------------------------------------------------------------
	# 노드 전체 파괴.
	#--------------------------------------------------------------------------------
	def DestroyAllNodes(self) -> None:
		if not self.__nodes:
			return	
		for node in self.Nodes:
			self.DestroyNode(node)
		self.__nodes.clear()


	#--------------------------------------------------------------------------------
	# 노드 추가.
	# - useUpdate: 이미 있을 경우 갱신처리 여부.
	#--------------------------------------------------------------------------------
	def AddNode(self, node: INode, useUpdate: bool = True) -> bool:
		if not node:
			return False
		if not useUpdate and self.ContainsNode(node.Value):
			return
		self.__nodes[node.Value] = node


	#--------------------------------------------------------------------------------
	# 노드 파괴. (함부로 삭제하면 캐싱이 꼬여서 곤란하므로 진짜 필요할 때 외에는 사용 금지)
	#--------------------------------------------------------------------------------
	def DestroyNode(self, target: Union[INode, str]) -> bool:
		if not target:
			return False
		targetNormalizedPath: str = NodeManager.GetNormalizedPath(target)
		if not targetNormalizedPath:
			return False	
		if targetNormalizedPath in self.__nodes:
			return False	
		target: INode = self.__nodes[targetNormalizedPath]
		target.OnDestroy()
		del self.__nodes[targetNormalizedPath]
		return True


	#--------------------------------------------------------------------------------
	# 노드 포함 여부 확인.
	#--------------------------------------------------------------------------------
	def ContainsNode(self, target: Union[INode, str]) -> bool:
		if not target:
			return False
		if not self.__nodes:
			return False
		targetNormalizedPath: str = NodeManager.GetNormalizedPath(target)
		if not targetNormalizedPath:
			return False
		if targetNormalizedPath not in self.__nodes:
			return False
		return True


	#--------------------------------------------------------------------------------
	# 노드 존재여부 및 노드 반환.
	#--------------------------------------------------------------------------------
	def TryGetNode(self, targetPath: str) -> Union[bool, Optional[INode]]:
		node: INode = self.GetNode(targetPath)
		if not node:
			return (False, None)
		return (True, node)


	#--------------------------------------------------------------------------------
	# 노드 반환.
	#--------------------------------------------------------------------------------
	def GetNode(self, target: Union[INode, str]) -> Optional[INode]:
		if not target:
			return None
		if not self.__nodes:
			return None
		targetNormalizedPath: str = NodeManager.GetNormalizedPath(target)
		if not targetNormalizedPath:
			return None
		if targetNormalizedPath not in self.__nodes:
			return None
		node: INode = self.__nodes[targetNormalizedPath]
		return node


	#--------------------------------------------------------------------------------
	# 노드 생성.
	# - 경로에서 디렉토리/파일의 실존 여부를 검사하지 않으므로 주의.
	#--------------------------------------------------------------------------------
	@staticmethod
	def CreateNode(targetPath: str) -> Optional[INode]:
		targetNormalizedPath = NodeManager.GetNormalizedPath(targetPath)
		if not targetNormalizedPath:
			return None
		nodeManager: NodeManager = NodeManager.GetSharedInstance()
		isContains, node = nodeManager.TryGetNode(targetNormalizedPath)
		if isContains:
			return node
		else:
			if NodeManager.IsDirectoryPath(targetNormalizedPath):
				node: INode = Object.__new__(DirectoryNode)
				nodeManager.AddNode(node)
				node.__init__(targetNormalizedPath)
				node.OnCreate(targetNormalizedPath)
				return node
			elif NodeManager.IsFilePath(targetNormalizedPath):
				node: INode = Object.__new__(FileNode)
				nodeManager.AddNode(node)
				node.__init__(targetNormalizedPath)
				node.OnCreate(targetNormalizedPath)
				return node
			else:
				return None


	#--------------------------------------------------------------------------------
	# 디렉토리 여부 반환.
	#--------------------------------------------------------------------------------
	@staticmethod
	def IsDirectoryPath(targetPath: str) -> bool:
		path, name, extension = NodeManager.GetPathAndNameAndExtension(targetPath)
		if extension:
			return False
		return True


	#--------------------------------------------------------------------------------
	# 파일 여부 반환.
	#--------------------------------------------------------------------------------
	@staticmethod
	def IsFilePath(targetPath: str) -> bool:
		path, name, extension = NodeManager.GetPathAndNameAndExtension(targetPath)
		if not extension:
			return False
		return True
	
	#--------------------------------------------------------------------------------
	# 디렉토리 존재 여부 반환.
	#--------------------------------------------------------------------------------
	@staticmethod
	def ExistsDirectory(targetDirectoryPath: str) -> bool:
		if not os.path.isdir(targetDirectoryPath):
			return False
		return True


	#--------------------------------------------------------------------------------
	# 파일 존재 여부 반환.
	#--------------------------------------------------------------------------------
	@staticmethod
	def ExistsFile(targetFilePath: str) -> bool:
		if not os.path.isfile(targetFilePath):
			return False
		return True


	#--------------------------------------------------------------------------------
	# 경로의 정규화된 경로 반환.
	#--------------------------------------------------------------------------------
	@staticmethod
	def GetNormalizedPath(target: Union[INode, str]) -> Optional[str]:
		if not target:
			return None
		if builtins.isinstance(target, INode):
			targetNormalizedPath = os.path.normpath(target.Value)
			return targetNormalizedPath
		elif builtins.isinstance(target, str):
			targetNormalizedPath = os.path.normpath(target)
			return targetNormalizedPath
		else:
			return None


	#--------------------------------------------------------------------------------
	# 노드/절대경로를 경로, 이름, 확장자로 변환하여 반환.
	#--------------------------------------------------------------------------------
	@staticmethod
	def GetPathAndNameAndExtension(targetPath: Union[INode, str]) -> tuple[str, str, str]:
		targetNormalizedPath: str = NodeManager.GetNormalizedPath(targetPath)
		if not targetNormalizedPath:
			return ("", "", "")
		path, fileName = os.path.split(targetNormalizedPath)
		name, extension = os.path.splitext(fileName)
		return (path, name, extension)


	#--------------------------------------------------------------------------------
	# 노드/경로 두개의 경로가 동일한지 여부 비교.
	#--------------------------------------------------------------------------------
	@staticmethod
	def Equals(leftTarget: Union[INode, str], rightTarget: Union[INode, str]) -> bool:
		if not leftTarget or not rightTarget:
			return False
		
		leftValue: str = NodeManager.GetNormalizedPath(leftTarget)
		rightValue: str = NodeManager.GetNormalizedPath(rightTarget)	
		if leftValue == rightValue:
			return True
		return False