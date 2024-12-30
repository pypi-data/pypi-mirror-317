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
import traceback
from. core import IDatabase, ITable, IQuery, IRecord, Installer


#--------------------------------------------------------------------------------
# Microsoft Installer Database Property Table.
#--------------------------------------------------------------------------------
class PropertyTable: # (ITable):
	#--------------------------------------------------------------------------------
	# 멤버 변수 목록.
	#--------------------------------------------------------------------------------
	__database: IDatabase


	#--------------------------------------------------------------------------------
	# 생성됨.
	#--------------------------------------------------------------------------------
	def __init__(self, database: IDatabase) -> None:
		self.__database = database


	#--------------------------------------------------------------------------------
	# 레코드 존재 유무.
	#--------------------------------------------------------------------------------
	def Exists(self, propertyName: str) -> IRecord:
		query: IQuery = Installer.CreateQuery(self.__database, f"SELECT Property FROM Property WHERE Property = '{propertyName}'")
		query.Execute()
		record: IRecord = query.Fetch()
		query.Close()
		if not record:
			return False
		return True

	
	#--------------------------------------------------------------------------------
	# 레코드 조회.
	#--------------------------------------------------------------------------------
	def Find(self, propertyName: str) -> IRecord:
		query: IQuery = Installer.CreateQuery(self.__database, f"SELECT * FROM Property WHERE Property = '{propertyName}'")
		query.Execute()
		record: IRecord = query.Fetch()
		query.Close()
		return record


	#--------------------------------------------------------------------------------
	# 레코드 추가.
	#--------------------------------------------------------------------------------
	def Add(self, propertyName: str, propertyValue: str) -> None:
		query: IQuery = Installer.CreateQuery(self.__database, "INSERT INTO Property (Property, Value) VALUES ('{propertyName}', '{propertyValue}')")
		query.Execute()
		query.Close()


	#--------------------------------------------------------------------------------
	# 레코드 변경.
	#--------------------------------------------------------------------------------
	def Set(self, propertyName: str, propertyValue: str) -> bool:
		if not self.Exists(propertyName):
			return False
		
		query: IQuery = Installer.CreateQuery(self.__database, f"UPDATE Property SET Value = '{propertyValue}' WHERE Property = '{propertyName}'")
		query.Execute()
		query.Close()
		return True