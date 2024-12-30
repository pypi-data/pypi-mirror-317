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


#--------------------------------------------------------------------------------
# 패키지 포함 목록.
#--------------------------------------------------------------------------------
from .schema import BooleanAttribute, Component, ComponentGroup, ComponentGroupRef, ComponentRef, Condition, Content, CreateFolder, Custom, CustomAction,\
Directory, DirectoryRef, DirectorySearch, Feature, File, FileSearch, Fragment, GuidAttribute, IdAttribute, InstallExecuteSequence, Package, Product, Property,\
UI, UIRef, Wix, WixVariable
from .basebuildprocess import BaseBuildProcess
from .languagecode import LanguageCode
from .wxs import WXS
from .xml import XML, Minidom, MinidomDocument, ElementTree, Element