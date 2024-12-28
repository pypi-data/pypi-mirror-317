from pathlib import Path
from .TypedPath import TypedPath
from .TimestampedPath import TimestampedPath

class IClearIO:
	"""
	Interface class for all classes that wish to represent themselves as ClearIO compliant classes.
	"""

	def CreateDirectory(self, fullDirectoryPath:Path|str, createParents:bool = True) -> None:
		"""
		Creates a directory

		Parameters
		----------
		fullDirectoryPath : Path or str
			The full path to the directory to create.

		createParents : bool
			Indicates whether to create the parent directories. If False and parent directories are missing, an IOError is raised.
		"""
		raise NotImplementedError()

	def RemoveDirectory(self, fullDirectoryPath:Path|str) -> None:
		"""
		Removes the specified directory and all child objects within the directory.

		Parameters
		----------
		fullDirectoryPath : Path or str
			The full path to the directory to remove.
		"""
		raise NotImplementedError()

	def EmptyDirectory(self, fullDirectoryPath:Path|str) -> None:
		"""
		Removes all child objects within the directory, but does not remove the directory.

		Parameters
		----------
		fullDirectoryPath : Path or str
			The full path to the directory to clean.
		"""
		raise NotImplementedError()

	def ListAllDirectories(self, fullDirectoryPath:Path|str) -> list[TypedPath]:
		"""
		Retrieves all directory paths within a directory. This method is not recursive.

		Parameters
		----------
		fullDirectoryPath : Path or str
			The full path to the directory to retrieve.

		Returns
		-------
		list[Path or str]
			A list of directories within the directory.
			Return type is determined by the type of fullDirectoryPath.
		"""
		raise NotImplementedError()

	def ListAllDirectoriesRecursively(self, fullDirectoryPath:Path|str) -> list[TypedPath]:
		"""
		Recursively retrieves all directory paths within a directory.

		Parameters
		----------
		fullDirectoryPath : Path or str
			The full path to the directory to retrieve.

		Returns
		-------
		list[Path or str]
			A list of directories within the directory.
			Return type is determined by the type of fullDirectoryPath.
		"""
		raise NotImplementedError()

	def ListDirectories(self, fullDirectoryPath:Path|str, pattern:str|None = None) -> list[TypedPath]:
		"""
		Retrieves directory paths within a directory where the directory name matches a regex pattern. This method is not recursive.

		Parameters
		----------
		fullDirectoryPath : Path or str
			The full path to the directory to retrieve.

		pattern : str
			The pattern to use when selecting which files to include in the results.
			Note: This is regex based. Not based on typical file name wildcards.
			Cf. https://medium.com/@jamestjw/parsing-file-names-using-regular-expressions-3e85d64deb69

		Returns
		-------
		list[Path or str]
			A list of directories within the directory.
			Return type is determined by the type of fullDirectoryPath.
		"""
		raise NotImplementedError()

	def ListDirectoriesRecursively(self, fullDirectoryPath:Path|str, pattern:str|None = None) -> list[TypedPath]:
		"""
		Recursively retrieves directory paths within a directory where the directory name matches a regex pattern.

		Parameters
		----------
		fullDirectoryPath : Path or str
			The full path to the directory to retrieve.

		pattern : str
			The pattern to use when selecting which files to include in the results.
			Note: This is regex based. Not based on typical file name wildcards.
			Cf. https://medium.com/@jamestjw/parsing-file-names-using-regular-expressions-3e85d64deb69

		Returns
		-------
		list[Path or str]
			A list of directories within the directory.
			Return type is determined by the type of fullDirectoryPath.
		"""
		raise NotImplementedError()

	def ListAllFiles(self, fullDirectoryPath:Path|str) -> list[TypedPath]:
		"""
		Retrieves all file paths within a directory. This method is not recursive.

		Parameters
		----------
		fullDirectoryPath : Path or str
			The full path to the directory to retrieve.

		Returns
		-------
		list[Path or str]
			A list of files within the directory.
			Return type is determined by the type of fullDirectoryPath.
		"""
		raise NotImplementedError()

	def ListAllFilesRecursively(self, fullDirectoryPath:Path|str) -> list[TypedPath]:
		"""
		Recursively retrieves all file paths within a directory.

		Parameters
		----------
		fullDirectoryPath : Path or str
			The full path to the directory to retrieve.

		Returns
		-------
		list[Path or str]
			A list of files within the directory.
			Return type is determined by the type of fullDirectoryPath.
		"""
		raise NotImplementedError()

	def ListFiles(self, fullDirectoryPath:Path|str, pattern:str|None = None) -> list[TypedPath]:
		"""
		Retrieves file paths within a directory where the file name matches a regex pattern. This method is not recursive.

		Parameters
		----------
		fullDirectoryPath : Path or str
			The full path to the directory to retrieve.

		pattern : str
			The pattern to use when selecting which files to include in the results.
			Note: This is regex based. Not based on typical file name wildcards.
			Cf. https://medium.com/@jamestjw/parsing-file-names-using-regular-expressions-3e85d64deb69

		Returns
		-------
		list[Path or str]
			A list of files within the directory.
			Return type is determined by the type of fullDirectoryPath.
		"""
		raise NotImplementedError()

	def ListFilesRecursively(self, fullDirectoryPath:TypedPath|Path|str, pattern:str|None = None) -> list[TypedPath]:
		"""
		Recursively retrieves file paths within a directory where the file name matches a regex pattern.

		Parameters
		----------
		fullDirectoryPath : Path or str
			The full path to the directory to retrieve.

		pattern : str
			The pattern to use when selecting which files to include in the results.
			Note: This is regex based. Not based on typical file name wildcards.
			Cf. https://medium.com/@jamestjw/parsing-file-names-using-regular-expressions-3e85d64deb69

		Returns
		-------
		list[Path or str]
			A list of files within the directory.
			Return type is determined by the type of fullDirectoryPath.
		"""
		raise NotImplementedError()

	def List(self, fullDirectoryPath:Path|str) -> list[TypedPath]:
		"""
		Retrieves all files and directories paths within a directory.

		Parameters
		----------
		fullDirectoryPath : Path or str
			The full path to the directory to retrieve.

		Returns
		-------
		list[Path or str]
			A list of files and directories within the directory.
			Return type is determined by the type of fullDirectoryPath.
		"""
		raise NotImplementedError()

	def ListRecursively(self, fullDirectoryPath:TypedPath|Path|str) -> list[TypedPath]:
		"""
		Recursively retrieves all files and directories paths within a directory.

		Parameters
		----------
		fullDirectoryPath : Path or str
			The full path to the directory to retrieve.

		Returns
		-------
		list[Path or str]
			A list of files and directories within the directory.
			Return type is determined by the type of fullDirectoryPath.
		"""
		raise NotImplementedError()

	def GetFile(self, fullPath:Path|str) -> bytes:
		"""
		Retrieves the bytes of a file.
		Note: These bytes can be used in PutFile to perform a copy style of operation.

		Parameters
		----------
		fullPath : Path or str
			The full path to the file to retrieve.
			
		Returns
		-------
		bytes
			A byte array of the contents of the file.
		"""
		raise NotImplementedError()

	def PutFile(self, fullPath:Path|str, content:bytes):
		"""
		Writes a byte array to a file.
		Note: contents may be the output of GetFile to perform a copy style of operation.

		Parameters
		----------
		fullPath : Path or str
			The full path to the file to write.

		contents : bytes
			The array of bytes to write to the file.
		"""
		raise NotImplementedError()

	def RemoveFile(self, fullFilePath:Path|str) -> None:
		"""
		Removes the specified file.

		Parameters
		----------
		fullFilePath : Path or str
			The full path to the file to remove.
		"""
		raise NotImplementedError()

	def ParseTimestamps(self, paths:list[TypedPath], prefixesBeforeTimestamp:list[str] | None = None, timestampFormat:str | None = None) -> list[TimestampedPath]:
		"""
		Attempts to parse timestamps from the file/directory names in the list provided.

		Parameters
		----------
		paths : list[Path or str]
			A list of paths to attempt to parse timestamps from. Can be directories, file, or a combination of both.
		
		prefixesBeforeTimestamp : list[str]
			A list of prefixes to check before the timestamp. If the list contains "" or is None, if will attempt to treat the stem, file name without extension, as the timestamp.
		
		timestampFormat : str
			The format the timestamp is expected to be in.
			Cf. https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes

		Returns
		-------
		list[TimestampedPath]
			A list containing TimestampedPaths. If a timestamp cannot be parsed, the TimestampedPath.HasTimestamp will be False.
		"""
		raise NotImplementedError()

__all__ = ["IClearIO"]
