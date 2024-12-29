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


#--------------------------------------------------------------------------------
# Microsoft Installer Custom Action Type.
#--------------------------------------------------------------------------------
class CustomActionType(Enum):
	EXECUTE_EXE_PATH_PROVIDED = 1      # 실행 파일 호출. (경로 제공)
	EXECUTE_FILE_AFTER_INSTALL = 2     # 파일 설치 후 실행.
	CALL_DLL = 8                       # DLL 호출.
	EXECUTE_EXE_PROPERTY_BASED = 16    # EXE 호출. (Property 기반)
	EXECUTE_INSTALLED_FILE = 32        # 설치된 파일 실행. (경로 제공)
	EXECUTE_FILE_ID_BASED = 34         # 파일 실행. (File ID 기반)
	EXECUTE_PATH_PROPERTY_BASED = 50   # Property 기반 경로로 실행.
	RUN_INTERNAL_SCRIPT = 64           # 내부 코드 호출.
	CALL_DLL_PROPERTY_BASED = 128      # DLL 호출. (Property 기반)
	RUN_PROCESS_WITH_ADMIN = 256       # 보조 관리자 프로세스 실행.
	WAIT_PROCESS_AND_CONTINUE = 512    # 보조 관리자 프로세스 실행 후 종료.
	EXECUTE_OUTSIDE_UI = 1024          # UI 외부에서 실행.
	IGNORE_FAILURE = 2048              # 실패 시 무시.