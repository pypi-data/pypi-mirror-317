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
from .core import IQuery, IRecord, Installer


#--------------------------------------------------------------------------------
# Microsoft Installer Database의 SQL 처리자. (View)
#--------------------------------------------------------------------------------
class Query(IQuery):
	#--------------------------------------------------------------------------------
	# 실행.
	#--------------------------------------------------------------------------------
	def Execute(self, value: Union[IRecord, Tuple, None] = None) -> None:
		try:
			if value == None:
				rawdata = self.GetRawData()
				rawdata.Execute(None)
			elif builtins.isinstance(value, IRecord):
				rawdata = self.GetRawData()
				rawdata.Execute(value.GetRawData())
			elif builtins.isinstance(value, Tuple):
				record: IRecord = Installer.CreateRecordFromFieldValues(value)
				rawdata = self.GetRawData()
				rawdata.Execute(record.GetRawData())
			else:
				raise ValueError(f"invalid value: {value}")
		except Exception as exception:
			builtins.print(exception)
			raise


	#--------------------------------------------------------------------------------
	# 가져오기.
	#--------------------------------------------------------------------------------
	def Fetch(self) -> Optional[IRecord]:
		try:
			rawdata = self.GetRawData()
			record = rawdata.Fetch()
			if not record:
				return None
			if not record.GetFieldCount():
				return None
		except Exception as exception:
			builtins.print(exception)
			raise
			
		from .record import Record
		return Record(record)


	#--------------------------------------------------------------------------------
	# 닫기.
	#--------------------------------------------------------------------------------
	def Close(self) -> None:
		rawdata = self.GetRawData()
		rawdata.Close()