from enum import Enum
from datetime import datetime
from pathlib import PureWindowsPath
import pathlib

class IOObjectType(Enum):
	Unknown = 0
	File = 1
	Directory = 2

class TypedPath(type(pathlib.Path())):
	ObjectType:IOObjectType = IOObjectType.Unknown
	SystemSeparator:str = "/"

	def __init__(self, path:pathlib.Path|str, objectType:IOObjectType = IOObjectType.Unknown):
		if (isinstance(path, PureWindowsPath)):
			self.SystemSeparator = "\\"
		if (isinstance(path, str)):
			super().__init__(pathlib.Path(path))
		else:
			super().__init__(path)
		self.Type = objectType

	def __str__(self):
		return str(super().__str__()).replace("\\", self.SystemSeparator)

__all__ = ["IOObjectType", "TypedPath"]
