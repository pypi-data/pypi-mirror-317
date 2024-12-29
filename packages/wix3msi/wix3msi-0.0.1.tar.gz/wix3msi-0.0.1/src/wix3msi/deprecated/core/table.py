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
from .core import ITable, IDatabase, IQuery, IRecord, Installer


#--------------------------------------------------------------------------------
# 테이블.
#--------------------------------------------------------------------------------
class Table(ITable):
	#--------------------------------------------------------------------------------
	# 컬럼 정보 반환.
	#--------------------------------------------------------------------------------
	def GetColumns(self) -> list:
		tableName: str = self.GetTableName()
		database: IDatabase = self.GetDatabase()
		try:
			query: IQuery = Installer.CreateQuery(database, f"SELECT Name FROM _Columns WHERE Table = {tableName}")
			query.Execute()
		except Exception as exception:
			raise

		record: IRecord = query.Fetch()
		columns = list()
		while record:
			fieldName: str = record.GetFieldValueAsString(0)
			fieldTypeCode: int = record.GetFieldValueAsInteger(1)
			fieldType: str = "Other"
			if fieldTypeCode == 0:
				fieldType = "String"
			elif fieldTypeCode == 1:
				fieldType = "Integer"
			columns.append((fieldName, fieldType))
			record = query.Fetch()
		query.Close()
		return columns


	#--------------------------------------------------------------------------------
	# 모든 레코드 반환.
	#--------------------------------------------------------------------------------
	def GetAllRecords(self) -> list:
		tableName: str = self.GetTableName()
		database: IDatabase = self.GetDatabase()
		records = list()
		query: IQuery = Installer.CreateQuery(database, f"SELECT * FROM {tableName}")
		query.Execute(None)
		data = query.Fetch()
		while data:
			records.append(data)
			data = query.Fetch()
		query.Close()
		return records

	#--------------------------------------------------------------------------------
	# 레코드 추가.
	#--------------------------------------------------------------------------------
	def Insert(self, record: IRecord) -> None:
		tableName: str = self.GetTableName()
		database: IDatabase = self.GetDatabase()
		columns: list = self.GetColumns()
		columnFieldsString: str = str()
		inputFieldsString: str = str()
		count: int = len(columns)

		for index in range(count):
			column = columns[index]
			if index + 1 < count:
				columnFieldsString += f"{column}, "
				inputFieldsString += f"?, "
			else:
				columnFieldsString += column
				inputFieldsString += f"?"

		query: IQuery = Installer.CreateQuery(database, f"INSERT INTO {self.__tableName} ({columnFieldsString}) VALUES ({inputFieldsString})")
		query.Execute(record)
		query.Close()



	#--------------------------------------------------------------------------------
	# 레코드 제거.
	#--------------------------------------------------------------------------------
	def Remove(self, record: IRecord) -> None:
		pass


	#--------------------------------------------------------------------------------
	# 레코드 갱신.
	#--------------------------------------------------------------------------------
	def Update(self, record: IRecord) -> None:
		pass


	#--------------------------------------------------------------------------------
	# 레코드 업데이트.
	#--------------------------------------------------------------------------------
	def UpdateRecords(self, whereFieldName: str, whereFieldValue: Union[int, str, None], updateFieldName: str, updateFieldValue: Union[int, str, None])  -> None:
		tableName: str = self.GetTableName()
		database: IDatabase = self.GetDatabase()
		record: IRecord = Installer.CreateRecordFromFieldValues((updateFieldValue, whereFieldValue))
		view = Installer.CreateQuery(database, f"UPDATE {tableName} SET {updateFieldName} = ? WHERE {whereFieldName} = ?")
		view.Execute(record)
		view.Close()