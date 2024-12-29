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
from ..filesystem import INode, DirectoryNode, FileNode, NodeManager
from .languagecode import LanguageCode


#--------------------------------------------------------------------------------
# 전역 상수 목록.
#--------------------------------------------------------------------------------
FILE_READTEXT: str = "rt"
FILE_WRITETEXT: str = "wt"
UTF8: str = "utf-8"
WIX: str = "wix"
WIX_NAMESPACE: str = "http://schemas.microsoft.com/wix/2006/wi"
EMPTY: str = ""
RE_REMOVE_NS0: str = "(ns0:|ns0|:ns0)"
LINEFEED: str = "\n"


#--------------------------------------------------------------------------------
# 기본 빌드 프로세스.
#--------------------------------------------------------------------------------
class BaseBuildProcess:
	#--------------------------------------------------------------------------------
	# 멤버 변수 목록.
	#--------------------------------------------------------------------------------
	__productCode: str
	__productVersion: str
	__productName: str
	__productManufacturer: str
	__productLanguague: LanguageCode


	#--------------------------------------------------------------------------------
	# 설치파일 코드 프로퍼티.
	#--------------------------------------------------------------------------------
	@property
	def ProductCode(self) -> str:
		return self.__productCode


	#--------------------------------------------------------------------------------
	# 설치파일 코드 프로퍼티.
	#--------------------------------------------------------------------------------
	@ProductCode.setter
	def ProductCode(self, value: str) -> None:
		self.__productCode = value


	#--------------------------------------------------------------------------------
	# 설치파일 버전 프로퍼티.
	#--------------------------------------------------------------------------------
	@property
	def ProductVersion(self) -> str:
		return self.__productVersion


	#--------------------------------------------------------------------------------
	# 설치파일 버전 프로퍼티.
	#--------------------------------------------------------------------------------
	@ProductVersion.setter
	def ProductVersion(self, value: str) -> None:
		self.__productVersion = value


	#--------------------------------------------------------------------------------
	# 설치파일 이름 프로퍼티.
	#--------------------------------------------------------------------------------
	@property
	def ProductName(self) -> str:
		return self.__productName


	#--------------------------------------------------------------------------------
	# 설치파일 이름 프로퍼티.
	#--------------------------------------------------------------------------------
	@ProductName.setter
	def ProductName(self, value: str) -> None:
		self.__productName = value


	#--------------------------------------------------------------------------------
	# 설치파일 제조업체 프로퍼티.
	#--------------------------------------------------------------------------------
	@property
	def ProductManufacturer(self) -> str:
		return self.__productManufacturer


	#--------------------------------------------------------------------------------
	# 설치파일 제조업체 프로퍼티.
	#--------------------------------------------------------------------------------
	@ProductManufacturer.setter
	def ProductManufacturer(self, value: str) -> None:
		self.__productManufacturer = value


	#--------------------------------------------------------------------------------
	# 설치파일 언어코드 프로퍼티.
	#--------------------------------------------------------------------------------
	@property
	def ProductLaunguage(self) -> LanguageCode:
		return self.__productLanguague


	#--------------------------------------------------------------------------------
	# 설치파일 언어코드 프로퍼티.
	#--------------------------------------------------------------------------------
	@ProductLaunguage.setter
	def ProductLaunguage(self, value: LanguageCode) -> None:
		self.__productLanguague = value


	#--------------------------------------------------------------------------------
	# 생성됨.
	#--------------------------------------------------------------------------------
	def __init__(self) -> None:
		self.__productCode = "{A1B2C3D4-5E6F-G7H8-IJKL-1M2N3O4P5Q6R}"
		self.__productVersion = "0.0.0"
		self.__productName = "ProductName"
		self.__productManufacturer = "ProductManufacturer"
		self.__productLanguague: LanguageCode = LanguageCode.ENGLISH