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
from .core import IRecord


#--------------------------------------------------------------------------------
# Microsoft Installer Database의 레코드.
#--------------------------------------------------------------------------------
class Record(IRecord):
	#--------------------------------------------------------------------------------
	# 필드 갯수 반환.
	#--------------------------------------------------------------------------------
	def GetFieldCount(self) -> int:
		rawdata = self.GetRawData()
		return rawdata.GetFieldCount()


	#--------------------------------------------------------------------------------
	# 값 반환.
	#--------------------------------------------------------------------------------
	def GetFieldValueAsInteger(self, fieldIndex: int) -> int:
		if fieldIndex < 0 or fieldIndex >= self.GetFieldCount():
			raise IndexError(f"invalid field index: {fieldIndex}")
		rawdata = self.GetRawData()
		return rawdata.GetInteger(fieldIndex + 1)


	#--------------------------------------------------------------------------------
	# 값 반환.
	#--------------------------------------------------------------------------------
	def GetFieldValueAsString(self, fieldIndex: int) -> str:
		if fieldIndex < 0 or fieldIndex >= self.GetFieldCount():
			raise IndexError(f"invalid field index: {fieldIndex}")
		rawdata = self.GetRawData()
		return rawdata.GetString(fieldIndex + 1)


	#--------------------------------------------------------------------------------
	# 값 설정.
	#--------------------------------------------------------------------------------
	def GetFieldValue(self, fieldIndex: int) -> Union[int, str, None]:
		if fieldIndex < 0 or fieldIndex >= self.GetFieldCount():
			raise IndexError(f"invalid field index: {fieldIndex}")
		try:
			return self.GetFieldValueAsInteger(fieldIndex)
		except Exception as exception:
			try:
				return self.GetFieldValueAsString(fieldIndex)
			except Exception as exception:
				raise


	#--------------------------------------------------------------------------------
	# 값 설정.
	#--------------------------------------------------------------------------------
	def SetFieldValueAsInteger(self, fieldIndex: int, value: int) -> None:
		if fieldIndex < 0 or fieldIndex >= self.GetFieldCount():
			raise IndexError(f"invalid field index: {fieldIndex}")
		elif value == None:
			rawdata = self.GetRawData()
			rawdata.SetString(fieldIndex + 1, 0)
		elif not builtins.isinstance(value, int):
			raise ValueError(f"filePath is Not Integer.")
		else:
			rawdata = self.GetRawData()
			rawdata.SetInteger(fieldIndex + 1, value)


	#--------------------------------------------------------------------------------
	# 값 설정.
	#--------------------------------------------------------------------------------
	def SetFieldValueAsString(self, fieldIndex: int, value: str) -> None:
		if fieldIndex < 0 or fieldIndex >= self.GetFieldCount():
			raise IndexError(f"invalid field index: {fieldIndex}")
		elif value == None:
			rawdata = self.GetRawData()
			rawdata.SetString(fieldIndex + 1, "")
		elif builtins.isinstance(value, str):
			rawdata = self.GetRawData()
			rawdata.SetString(fieldIndex + 1, value)
		else:
			raise ValueError(f"{value} is Not String.")


	#--------------------------------------------------------------------------------
	# 값 설정.
	#--------------------------------------------------------------------------------
	def SetFieldValueAsStream(self, fieldIndex: int, filePath: str) -> None:
		if fieldIndex < 0 or fieldIndex >= self.GetFieldCount():
			raise IndexError(f"invalid field index: {fieldIndex}")
		elif not builtins.isinstance(filePath, str):
			raise ValueError(f"not String.")
		elif not os.path.exists(filePath):
			raise FileNotFoundError(f"not exist file: {filePath}")
		rawdata = self.GetRawData()
		rawdata.SetStream(fieldIndex + 1, filePath)


	#--------------------------------------------------------------------------------
	# 값 설정.
	#--------------------------------------------------------------------------------
	def SetFieldValue(self, fieldIndex: int, value: Union[int, str, None]) -> None:
		if fieldIndex < 0 or fieldIndex >= self.GetFieldCount():
			raise IndexError(f"invalid field index: {fieldIndex}")
		elif value == None:
			self.SetFieldValueAsString(fieldIndex, None)
		elif builtins.isinstance(value, int):
			self.SetFieldValueAsInteger(fieldIndex, value)
		elif builtins.isinstance(value, str):
			if os.path.exists(value):
				self.SetFieldValueAsStream(fieldIndex, value)
			else:
				self.SetFieldValueAsString(fieldIndex, value)
		else:
			raise ValueError(f"connot be a field value: {value}")


	#--------------------------------------------------------------------------------
	# 값 설정.
	#--------------------------------------------------------------------------------
	def SetFieldValues(self, fieldValues: Tuple) -> None:
		fieldIndex: int = 0
		for fieldValue in fieldValues:
			self.SetFieldValue(fieldIndex, fieldValue)
			fieldIndex += 1