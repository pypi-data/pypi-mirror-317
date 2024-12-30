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
# # import cx_Freeze # type: ignore
# # from cx_Freeze import Executable # type: ignore
# import win32com.client # type: ignore


# #--------------------------------------------------------------------------------
# # 전역 상수 목록.
# #--------------------------------------------------------------------------------
# NAME: str = "이름"
# VERSION: str = "버전"
# CREATOR: str = "공급업체"
# DESCRIPTION: str = "설명"
# BDIST_MSI: str = "bdist_msi"
# BUILD_EXE: str = "build_exe"
# CURRENTFILEPATH: str = os.path.abspath(__file__)
# ROOTPATH: str = os.path.dirname(CURRENTFILEPATH)


# #--------------------------------------------------------------------------------
# # 파일 진입점.
# #--------------------------------------------------------------------------------
# if __name__ == "__main__":
# 	msi_path = "example.msi"  # 수정할 MSI 파일 경로
# 	file_id = "UpdateBatFile"  # File 테이블의 File ID
# 	component_id = "MainComponent"  # Component 테이블의 Component ID
# 	directory_id = "TARGETDIR"  # Component 테이블의 Directory ID
# 	sequence = 1  # 설치 순서	
# 	msiFilePath: str = os.path.join(ROOTPATH, msi_path)

# 	installer = win32com.client.Dispatch("WindowsInstaller.Installer")
# 	database = installer.OpenDatabase(msiFilePath, 3)

# 	tables_query = "SELECT * FROM `_Tables` WHERE Name = 'Component'"
# 	view = database.OpenView(tables_query)
# 	view.Execute(None)
# 	record = view.Fetch()
# 	if record:
# 		print("Component 테이블이 존재합니다.")
# 	else:
# 		print("Component 테이블이 없습니다.")

# 	tables_query = "SELECT * FROM `_Tables` WHERE Name = 'File'"
# 	view = database.OpenView(tables_query)
# 	view.Execute(None)
# 	record = view.Fetch()
# 	if record:
# 		print("File 테이블이 존재합니다.")
# 	else:
# 		print("File 테이블이 없습니다.")
# 		create_table_query = """
# 			CREATE TABLE File (
# 				File TEXT PRIMARY KEY,
# 				Component_ TEXT NOT NULL,
# 				FileName TEXT NOT NULL,
# 				FileSize INTEGER,
# 				Version TEXT,
# 				Language TEXT,
# 				Attributes INTEGER,
# 				Sequence INTEGER
# 			)
# 		"""
# 		view = database.OpenView(create_table_query)
# 		view.Execute(None)
# 		view.Close()

# 	try:
# 		sourceFilePath: str = os.path.join(ROOTPATH, "res", "msi", "update.bat")
# 		sourceFileSize = os.path.getsize(sourceFilePath)
# 		view = database.OpenView("INSERT INTO File (File, Component_, FileName, FileSize, Version, Language, Attributes, Sequence) VALUES (?, ?, ?, ?, ?, ?, ?, ?)")
# 		record = installer.CreateRecord(8)
# 		record.SetString(1, file_id)  # File ID
# 		record.SetString(2, component_id)  # Component ID
# 		record.SetString(3, "update.bat")  # File Name
# 		record.SetInteger(4, sourceFileSize)  # File Size
# 		record.SetString(5, None)  # Version
# 		record.SetString(6, None)  # Language
# 		record.SetInteger(7, 0)  # Attributes
# 		record.SetInteger(8, sequence)  # Sequence	
# 		view.Execute(record)
# 		view.Close()
# 		view = database.OpenView("INSERT INTO Component (Component, ComponentId, Directory_, Attributes, Condition, KeyPath) VALUES (?, ?, ?, ?, ?, ?)")
# 		record = installer.CreateRecord(6)
# 		record.SetString(1, component_id)  # Component ID
# 		record.SetString(2, "{12345678-1234-1234-1234-123456789ABC}")  # Component GUID
# 		record.SetString(3, directory_id)  # Directory ID
# 		record.SetInteger(4, 0)  # Attributes
# 		record.SetString(5, None)  # Condition
# 		record.SetString(6, file_id)  # KeyPath
# 		view.Execute(record)	
# 		view.Close()

# 		with open(sourceFilePath, "rb") as file:
# 			bytes = file.read()

# 		database.Streams(file_id).Write(bytes)
# 		database.Commit()
# 	except Exception as exception:
# 		builtins.print(exception)
#	# finally:
#	# 	database.Close()