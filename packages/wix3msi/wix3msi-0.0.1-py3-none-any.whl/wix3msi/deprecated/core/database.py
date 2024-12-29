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
from .core import IDatabase, IQuery, IRecord, ITable, Installer


#--------------------------------------------------------------------------------
# 전역 상수 목록.
#--------------------------------------------------------------------------------
SQL_EXISTS_TABLE: str = "SELECT Name FROM _Tables WHERE Name = ?"


#--------------------------------------------------------------------------------
# Microsoft Installer Database.
# - cmd: msiexec /?
#--------------------------------------------------------------------------------
class Database(IDatabase):
	#--------------------------------------------------------------------------------
	# 테이블 반환.
	#--------------------------------------------------------------------------------
	def GetTable(self, tableName: str) -> ITable:
		if not Installer.ExistsTable(self, tableName):
			return None
		
		from .table import Table
		return Table(self, tableName)


	#--------------------------------------------------------------------------------
	# 적용.
	#--------------------------------------------------------------------------------
	def Commit(self) -> None:
		rawdata = self.GetRawData()
		rawdata.Commit()


	#--------------------------------------------------------------------------------
	# 닫기.
	#--------------------------------------------------------------------------------
	def Close(self) -> None:
		rawdata = self.GetRawData()
		rawdata.Close()