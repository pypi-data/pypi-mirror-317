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
from wix3msi import IDatabase, IQuery, IRecord, ITable, Installer, DatabaseScope, QueryScope, CustomActionType


#--------------------------------------------------------------------------------
# BuildProcess.
#--------------------------------------------------------------------------------
class BuildProcess:
	#--------------------------------------------------------------------------------
	# 출력.
	#--------------------------------------------------------------------------------
	@staticmethod
	def PrintTable(database: IDatabase, tableName: str) -> None:
		# 파일 테이블 출력.
		table: ITable = database.GetTable(tableName)
		for record in table.GetAllRecords():
			record: IRecord = cast(IRecord, record)
			fieldValues = Installer.CreateFieldValuesFromRecord(record)
			builtins.print(f"[{tableName}] {fieldValues}")


	#--------------------------------------------------------------------------------
	# 생성.
	#--------------------------------------------------------------------------------
	@staticmethod
	def CreateMSIToFile(msiFilePath: str, applicationGUID: str) -> None:
		# 생성.
		database: IDatabase = Installer.CreateDatabase(msiFilePath)

		# 프로퍼티 테이블.
		if Installer.ExistsTable(database, "Property"):
			propertyTable: ITable = database.GetTable("Property")
			propertyTable.UpdateRecords("Property", "ProductName", "Value", "ALTAVA Group 3ds Max 2023 Plugin")
			propertyTable.UpdateRecords("Property", "ProductCode", "Value", applicationGUID)
			propertyTable.UpdateRecords("Property", "ProductVersion", "Value", "0.0.10")
			propertyTable.UpdateRecords("Property", "Manufacturer", "Value", "ALTAVA Group")
			propertyTable.UpdateRecords("Property", "ProductLanguage", "Value", 1033)
		else:
			with QueryScope(database, "CREATE TABLE Property (Property TEXT NOT NULL PRIMARY KEY, Value TEXT)") as query:
				query.Execute()
			with QueryScope(database, "INSERT INTO Property (Property, Value) VALUES (?, ?)") as query:
				query.Execute(("ProductName", "ALTAVA Group 3ds Max 2023 Plugin"))
				query.Execute(("ProductCode", applicationGUID))
				query.Execute(("ProductVersion", "0.0.10"))
				query.Execute(("Manufacturer", "ALTAVA Group"))
				query.Execute(("ProductLanguage", 1033))
		BuildProcess.PrintTable(database, "Property")

		# 디렉토리 테이블.
		with QueryScope(database, "INSERT INTO Directory (Directory, Directory_Parent, DefaultDir) VALUES (?, ?, ?)") as query:
			query.Execute(("TARGETDIR", None, "SourceDir"))
			query.Execute(("PROGRAMFILES", "TARGETDIR", ".:Programe Files"))
			query.Execute(("AUTODESK_3DSMAX2023", "PROGRAMFILES", "Autodesk\\3ds Max 2023"))
			query.Execute(("AUTODESK_3DSMAX2023_BIN_ASSEMBLIES", "AUTODESK_3DSMAX2023", "bin\\assemblies"))
			query.Execute(("AUTODESK_3DSMAX2023_SCRIPTS_ALTAVAMAXPLUGIN", "AUTODESK_3DSMAX2023", "scirpts\\AltavaMaxPlugin"))
			query.Execute(("AUTODESK_3DSMAX2023_SCRIPTS_STARTUP", "AUTODESK_3DSMAX2023", "scirpts\\Startup"))
		BuildProcess.PrintTable(database, "Directory")

		# 컴포넌트 테이블.
		with QueryScope(database, "INSERT INTO Component (Component, ComponentId, Directory_, Attributes, Condition, KeyPath) VALUES (?, ?, ?, ?, ?, ?)") as query:
			query.Execute(("ALTAVA_MAX_PLUGIN", Installer.CreateGUID(), "AUTODESK_3DSMAX2023_SCRIPTS_ALTAVAMAXPLUGIN", 0, "VersionNT >= 1000", "AUTODESK_3DSMAX2023_SCRIPTS_ALTAVAMAXPLUGIN"))
			query.Execute(("BABYLON_JS_EXPORTER", Installer.CreateGUID(), "AUTODESK_3DSMAX2023", 0, "VersionNT >= 1000", None))

		# 파일 테이블.
		database.AddStream
		with QueryScope(database, "INSERT INTO File (File, Component_, FileName, FileSize, Version, Language, Attributes, Sequence) VALUES (?, ?, ?, ?, ?, ?, ?, ?)") as query:
			fileSize = os.path.getsize("update.bat")
			query.Execute(("update.bat", "ALTAVA_MAX_PLUGIN", "update.bat", fileSize, None, None, 0, 1))
			# query.Execute(("update.bat", "BABYLON_JS_EXPORTER", "update.bat", fileSize, None, None, 0, 1))
		BuildProcess.PrintTable(database, "File")

		# 커스텀 액션 테이블.
		with QueryScope(database, "INSERT INTO CustomAction (Action, Type, Source, Target) VALUES (?, ?, ?, ?)") as query:
			query.Execute(("UpdateBatchFile", CustomActionType.EXECUTE_FILE_ID_BASED.value, "update.bat", ""))

		# # 설치 실행 시퀀스 테이블.
		BuildProcess.PrintTable(database, "InstallExecuteSequence")
		# with QueryScope(database, "INSERT INTO InstallExecuteSequence (Action, Condition, Sequence) VALUES (?, ?, ?)") as query:
		# 	query.Execute(("UpdateBatchFile", "NOT Installed", 700))

		# 최종 반영.
		database.Commit()
		database.Close()