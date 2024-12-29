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
import os
import re
import uuid
from xml.dom import minidom as Minidom
from xml.dom.minidom import Document as MinidomDocument
from xml.etree import ElementTree
from xml.etree.ElementTree import Element
from .condition import Condition
from .customaction import CustomAction
from .feature import Feature
from .guidattribute import GuidAttribute
from .idattribute import IdAttribute
from .installexecutesequence import InstallExecuteSequence
from .mediatemplate import MediaTemplate
from .package import Package
from .property import Property
from .ui import UI
from .wixvariable import WixVariable


#--------------------------------------------------------------------------------
# 프로덕트 요소.
#--------------------------------------------------------------------------------
class Product:
	#--------------------------------------------------------------------------------
	# 멤버 변수 목록.
	#--------------------------------------------------------------------------------
	Id: IdAttribute
	Name: str
	Manufacturer: str
	UpgradeCode: GuidAttribute
	Version: str
	Language: str
	Children: Optional[List[Condition, CustomAction, Feature, InstallExecuteSequence, MediaTemplate, Package, Property, UI, WixVariable]]