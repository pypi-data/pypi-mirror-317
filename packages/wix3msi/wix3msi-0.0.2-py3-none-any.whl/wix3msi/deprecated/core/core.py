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
import msilib # type: ignore
from xpl import Interface, BaseClass, abstractmethod


#--------------------------------------------------------------------------------
# 전역 상수 목록.
#--------------------------------------------------------------------------------
SQL_CREATE_PROPERTYTABLE: str = "CREATE TABLE Property (Property TEXT NOT NULL PRIMARY KEY, Value TEXT)"
SQL_EXISTS_TABLE: str = "SELECT Name FROM _Tables WHERE Name = ?"
UNDEFINED: str = "undefined"


#--------------------------------------------------------------------------------
# 데이터베이스 인터페이스.
#--------------------------------------------------------------------------------
class IDatabase(Interface):
	#--------------------------------------------------------------------------------
	# 멤버 변수 목록.
	#--------------------------------------------------------------------------------
	__database: msilib.Database	


	#--------------------------------------------------------------------------------
	# 생성됨.
	#--------------------------------------------------------------------------------
	def __init__(self, database: msilib.Database) -> None:
		self.__database = database


	#--------------------------------------------------------------------------------
	# 문자열 변환.
	#--------------------------------------------------------------------------------
	def __str__(self) -> str:
		return str(self.__database)
	

	#--------------------------------------------------------------------------------
	# 래핑한 원래 객체.
	#--------------------------------------------------------------------------------
	def GetRawData(self) -> msilib.Database:
		return self.__database


	#--------------------------------------------------------------------------------
	# 테이블 반환.
	#--------------------------------------------------------------------------------
	@abstractmethod
	def GetTable(self, tableName: str) -> ITable: pass


	#--------------------------------------------------------------------------------
	# 적용.
	#--------------------------------------------------------------------------------
	@abstractmethod
	def Commit(self) -> None: pass


	#--------------------------------------------------------------------------------
	# 닫기.
	#--------------------------------------------------------------------------------
	@abstractmethod
	def Close(self) -> None: pass


#--------------------------------------------------------------------------------
# 테이블 인터페이스.
#--------------------------------------------------------------------------------
class ITable(Interface):
	#--------------------------------------------------------------------------------
	# 멤버 변수 목록.
	#--------------------------------------------------------------------------------
	__database: IDatabase
	__tableName: str
	# __columnNames: list
	# __columnTypes: list

	#--------------------------------------------------------------------------------
	# 생성됨.
	#--------------------------------------------------------------------------------
	def __init__(self, database: IDatabase, tableName: str) -> None:
		self.__database = database
		self.__tableName = tableName
		self.__columnNames = list()
		self.__columnTypes = list()
		# for column in self.GetColumns():
		# 	self.__columnNames.append(column[0])
		# 	self.__columnTypes.append(column[1])


	#--------------------------------------------------------------------------------
	# 래핑한 원래 객체.
	#--------------------------------------------------------------------------------
	def GetDatabase(self) -> msilib.Database:
		return self.__database
	

	#--------------------------------------------------------------------------------
	# 테이블 이름.
	#--------------------------------------------------------------------------------
	def GetTableName(self) -> str:
		return self.__tableName
	

	#--------------------------------------------------------------------------------
	# 컬럼 정보 반환.
	#--------------------------------------------------------------------------------
	def GetColumns(self) -> list: pass


	#--------------------------------------------------------------------------------
	# 모든 레코드 반환.
	#--------------------------------------------------------------------------------		
	def GetAllRecords(self) -> list: pass


	#--------------------------------------------------------------------------------
	# 레코드 추가.
	#--------------------------------------------------------------------------------	
	def Insert(self, record: IRecord) -> None: pass


	#--------------------------------------------------------------------------------
	# 레코드 제거.
	#--------------------------------------------------------------------------------
	def Remove(self, record: IRecord) -> None: pass


	#--------------------------------------------------------------------------------
	# 레코드 갱신.
	#--------------------------------------------------------------------------------
	def Update(self, record: IRecord) -> None: pass


	#--------------------------------------------------------------------------------
	# 레코드 업데이트.
	#--------------------------------------------------------------------------------
	def UpdateRecords(self, whereFieldName: str, whereFieldValue: Union[int, str, None], updateFieldName: str, updateFieldValue: Union[int, str, None]) -> None: pass


#--------------------------------------------------------------------------------
# 쿼리 인터페이스.
#--------------------------------------------------------------------------------
class IQuery(Interface):
	#--------------------------------------------------------------------------------
	# 멤버 변수 목록.
	#--------------------------------------------------------------------------------
	__view: msilib.View


	#--------------------------------------------------------------------------------
	# 생성됨.
	#--------------------------------------------------------------------------------
	def __init__(self, view: msilib.View) -> None:
		self.__view = view


	#--------------------------------------------------------------------------------
	# 문자열 변환.
	#--------------------------------------------------------------------------------
	def __str__(self) -> str:
		return str(self.__view)
	

	#--------------------------------------------------------------------------------
	# 래핑한 원래 객체.
	#--------------------------------------------------------------------------------
	def GetRawData(self) -> msilib.View:
		return self.__view


	#--------------------------------------------------------------------------------
	# 실행.
	#--------------------------------------------------------------------------------
	@abstractmethod
	def Execute(self, value: Union[IRecord, Tuple, None] = None) -> None: pass


	#--------------------------------------------------------------------------------
	# 가져오기.
	#--------------------------------------------------------------------------------
	@abstractmethod
	def Fetch(self) -> Optional[IRecord]: pass


	#--------------------------------------------------------------------------------
	# 닫기.
	#--------------------------------------------------------------------------------
	@abstractmethod
	def Close(self) -> None: pass


#--------------------------------------------------------------------------------
# 레코드 인터페이스.
#--------------------------------------------------------------------------------
class IRecord(Interface):
	#--------------------------------------------------------------------------------
	# 멤버 변수 목록.
	#--------------------------------------------------------------------------------
	__record: msilib.Record


	#--------------------------------------------------------------------------------
	# 생성됨.
	#--------------------------------------------------------------------------------
	def __init__(self, record: msilib.Record) -> None:
		self.__record = record


	#--------------------------------------------------------------------------------
	# 문자열 변환.
	#--------------------------------------------------------------------------------
	def __str__(self) -> str:
		return str(self.__record)
	

	#--------------------------------------------------------------------------------
	# 래핑한 원래 객체.
	#--------------------------------------------------------------------------------
	def GetRawData(self) -> msilib.Record:
		return self.__record


	#--------------------------------------------------------------------------------
	# 필드 갯수 반환.
	#--------------------------------------------------------------------------------
	@abstractmethod
	def GetFieldCount(self) -> int: pass


	#--------------------------------------------------------------------------------
	# 값 반환.
	#--------------------------------------------------------------------------------
	@abstractmethod
	def GetFieldValueAsInteger(self, fieldIndex: int) -> int: pass


	#--------------------------------------------------------------------------------
	# 값 반환.
	#--------------------------------------------------------------------------------
	@abstractmethod
	def GetFieldValueAsString(self, fieldIndex: int) -> str: pass


	#--------------------------------------------------------------------------------
	# 값 반환.
	#--------------------------------------------------------------------------------
	@abstractmethod
	def GetFieldValue(self, fieldIndex: int) -> Union[int, str, None]: pass


	#--------------------------------------------------------------------------------
	# 값 설정.
	#--------------------------------------------------------------------------------
	@abstractmethod
	def SetFieldValueAsInteger(self, fieldIndex: int, value: int) -> None: pass


	#--------------------------------------------------------------------------------
	# 값 설정.
	#--------------------------------------------------------------------------------
	@abstractmethod
	def SetFieldValueAsString(self, fieldIndex: int, value: str) -> None: pass


	#--------------------------------------------------------------------------------
	# 값 설정.
	#--------------------------------------------------------------------------------
	@abstractmethod
	def SetFieldValueAsStream(self, fieldIndex: int, filePath: str) -> None: pass


	#--------------------------------------------------------------------------------
	# 값 설정.
	#--------------------------------------------------------------------------------
	@abstractmethod
	def SetFieldValue(self, fieldIndex: int, value: Union[int, str, None]) -> None: pass


	#--------------------------------------------------------------------------------
	# 값 설정.
	#--------------------------------------------------------------------------------
	@abstractmethod
	def SetFieldValues(self, fieldValues: Tuple) -> None: pass


#--------------------------------------------------------------------------------
# 인스톨러.
#--------------------------------------------------------------------------------
class Installer(BaseClass):
	#--------------------------------------------------------------------------------
	# GUID 생성.
	# - 생성된 값: "{12345678-1234-1234-1234-123456789ABC}"
	# - uuid4로 대체 가능.
	#--------------------------------------------------------------------------------
	@staticmethod
	def CreateGUID() -> str:
		try:
			return msilib.gen_uuid()
		except Exception as exception:
			builtins.print(exception)
			raise
	

	#--------------------------------------------------------------------------------
	# 생성.
	#--------------------------------------------------------------------------------
	@staticmethod
	def CreateDatabase(msiFilePath: str) -> IDatabase:
		try:
			msilib.init_database(msiFilePath, msilib.schema, UNDEFINED, UNDEFINED, UNDEFINED, UNDEFINED)
		except Exception as exception:
			builtins.print(exception)
			raise
		
		database: IDatabase = Installer.OpenDatabase(msiFilePath)
		return database


	#--------------------------------------------------------------------------------
	# 불러오기.
	#--------------------------------------------------------------------------------
	@staticmethod
	def OpenDatabase(msiFilePath: str) -> IDatabase:
		try:
			database: msilib.Database = msilib.OpenDatabase(msiFilePath, msilib.MSIDBOPEN_TRANSACT)
		except Exception as exception:
			builtins.print(exception)
			raise

		from .database import Database
		return Database(database)


	#--------------------------------------------------------------------------------
	# 불러오기. (읽기전용)
	#--------------------------------------------------------------------------------
	@staticmethod
	def OpenDatabaseAsReadonly(msiFilePath: str) -> IDatabase:
		try:
			database: msilib.Database = msilib.OpenDatabase(msiFilePath, msilib.MSIDBOPEN_READONLY)
		except Exception as exception:
			builtins.print(exception)
			raise

		from .database import Database
		return Database(database)
	

	#--------------------------------------------------------------------------------
	# 테이블 존재 유무.
	#--------------------------------------------------------------------------------
	@staticmethod
	def ExistsTable(database: IDatabase, tableName: str) -> bool:
		fieldValues: Tuple = (tableName,)
		record: IRecord = Installer.CreateRecordFromFieldValues(fieldValues)
		try:
			query: IQuery = Installer.CreateQuery(database, SQL_EXISTS_TABLE)
			query.Execute(record)
			data = query.Fetch()
			query.Close()
			if data == None:
				return False
			elif data.GetFieldCount() == 0:
				return False
			return True
		except Exception as exception:
			return False


	#--------------------------------------------------------------------------------
	# 테이블 생성.
	#--------------------------------------------------------------------------------
	@staticmethod
	def CreateTable(database: IDatabase, tableName: str, fields: list) -> ITable:
		if not Installer.ExistsTable(database, tableName):
			fieldsString: str = str() # Component TEXT PRIMARY KEY, Directory_ TEXT, Attributes INTEGER, Guid TEXT

			fieldCount: int = builtins.len(fields)
			for index in range(fieldCount):
				field: str = fields[index]
				if not field:
					raise ValueError()
				
				values = field.split(" ")
				name: str = values[0]
				type: str = "TEXT"
				isPrimaryKey: bool = False
				wordCount: int = builtins.len(values)

				# 문제가 있음.
				if wordCount == 0:
					raise IndexError()

				if wordCount > 0:
					name: str = values[0]
				if wordCount > 1:
					type = values[1]
				if wordCount > 2:
					isPrimaryKey = True

				if index + 1 < fieldCount:
					if isPrimaryKey:
						fieldsString += f"{name} {type} PRIMARY KEY, "
					else:
						fieldsString += f"{name} {type}, "
				else:
					if isPrimaryKey:
						fieldsString += f"{name} {type} PRIMARY KEY"
					else:
						fieldsString += f"{name} {type}"

		query: IQuery = Installer.CreateQuery(database, f"CREATE TABLE {tableName} ({fieldsString})")
		query.Execute()
		from .table import Table
		table = Table(database, tableName)
		query.Close()


	#--------------------------------------------------------------------------------
	# 쿼리 생성하기. (뷰)
	#--------------------------------------------------------------------------------
	@staticmethod
	def CreateQuery(database: IDatabase, sqlString: str) -> IQuery:
		try:
			builtins.print(sqlString)
			rawdata: msilib.Databse = database.GetRawData()
			view: msilib.View = rawdata.OpenView(sqlString)
		except Exception as exception:
			builtins.print(exception)
			raise
	
		from .query import Query
		return Query(view)
	

	#--------------------------------------------------------------------------------
	# 레코드 생성.
	#--------------------------------------------------------------------------------
	@staticmethod
	def CreateRecord(fieldCount: int) -> IRecord:
		try:
			record: msilib.Record = msilib.CreateRecord(fieldCount)
		except Exception as exception:
			builtins.print(exception)
			raise

		from .record import Record
		return Record(record)
	

	#--------------------------------------------------------------------------------
	# 필드값 목록으로부터 레코드 생성.
	#--------------------------------------------------------------------------------
	@staticmethod
	def CreateRecordFromFieldValues(fieldValues: Tuple) -> IRecord:
		try:
			fieldCount: int = builtins.len(fieldValues)
			if fieldCount == 0:
				raise ValueError(f"invalid field values: {fieldValues}")
			record: IRecord = Installer.CreateRecord(fieldCount)
			record.SetFieldValues(fieldValues)
			return record
		except Exception as exception:
			builtins.print(exception)
			raise
	

	#--------------------------------------------------------------------------------
	# 필드값 목록으로부터 레코드 생성.
	#--------------------------------------------------------------------------------
	@staticmethod
	def CreateFieldValuesFromRecord(record: IRecord) -> Optional[Tuple]:
		try:
			if not record:
				raise ValueError(f"invalid record.")
			if record.GetFieldCount() == 0:
				raise ValueError(f"invalid record.")
			return tuple(record.GetFieldValue(index) for index in range(record.GetFieldCount()))
		except Exception as exception:
			builtins.print(exception)
			raise