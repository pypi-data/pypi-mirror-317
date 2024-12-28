from pathlib import Path, PurePosixPath
import re
import boto3
import botocore

from .IClearIO import IClearIO
from .TypedPath import TypedPath, IOObjectType
from .TimestampedPath import TimestampedPath

class S3ClearIO(IClearIO):
	"""
	Class for S3 access in a ClearIO compliant way.
	"""
	S3Resource = None
	S3Bucket = None
	Bucket:str|None = None
	AccessKey:str|None = None
	SecretAccessKey:str|None = None

	def __init__(self, bucket:str, accessKey:str, secretAccessKey:str) -> None:
		if (bucket is None):
			raise ValueError("bucket is required")
		if (accessKey is None):
			raise ValueError("accessKey is required")
		if (secretAccessKey is None):
			raise ValueError("secretAccessKey is required")
		self.Bucket = bucket
		self.AccessKey = accessKey
		self.SecretAccessKey = secretAccessKey
		self.S3Resource = boto3.resource(
			"s3",
			aws_access_key_id=self.AccessKey,
			aws_secret_access_key=self.SecretAccessKey)
		self.S3Bucket = self.S3Resource.Bucket(self.Bucket)

	def SplitPathToPaths(self, fullPath:Path|str) -> list[str]:
		returnValue:list[str] = list[str]()
		if (isinstance(fullPath, str) or isinstance(fullPath, Path)):
			fullPath = PurePosixPath(fullPath)
		fullPath = str(fullPath)
		if (fullPath.startswith("/")):
			fullPath = fullPath[1:]
		if (fullPath.endswith("/")):
			fullPath = fullPath[:1]
		path:str = None
		for element in fullPath.split("/"):
			if (path is not None):
				path += f"/{element}"
			else:
				path = element
			if (path not in returnValue):
				returnValue.append(path)
		return sorted(returnValue)

	def ExistsIndependent(self, fullPath:Path|str) -> bool:
		returnValue:bool = False
		if (isinstance(fullPath, str) or isinstance(fullPath, Path)):
			fullPath = PurePosixPath(fullPath)
		fullPath = str(fullPath)
		try:
			self.S3Resource.Object(self.Bucket, fullPath).load()
			returnValue = True
		except botocore.exceptions.ClientError as e:
			if e.response['Error']['Code'] == "404":
				returnValue = False
			else:
				raise
		return sorted(returnValue)

	def Exists(self, fullPath:Path|str) -> bool:
		returnValue:bool = False
		if (isinstance(fullPath, str) or isinstance(fullPath, Path)):
			fullPath = PurePosixPath(fullPath)
		fullPath = str(fullPath)
		for o in self.S3Bucket.objects.filter(Prefix=fullPath):
			if (o.key.startswith(str(fullPath))):
				returnValue = True
				break
		return sorted(returnValue)

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
		if (isinstance(fullDirectoryPath, str) or isinstance(fullDirectoryPath, Path)):
			fullDirectoryPath = PurePosixPath(fullDirectoryPath)
		if (not self.Exists(fullDirectoryPath.parent)
	  		and not createParents):
			raise ValueError("Parent does not exists")
		elif (not self.Exists(fullDirectoryPath.parent)
	  		and createParents):
			parentPathString:str = f"{str(fullDirectoryPath.parent)}/"
			self.S3Bucket.put_object(Key=parentPathString)
		pathString:str = str(fullDirectoryPath)
		if (not pathString.endswith("/")):
			pathString += "/"
		self.S3Bucket.put_object(Key=str(pathString))
		
	def RemoveDirectory(self, fullDirectoryPath:Path|str) -> None:
		"""
		Removes the specified directory and all child objects within the directory.

		Parameters
		----------
		fullDirectoryPath : Path or str
			The full path to the directory to remove.
		"""
		if (isinstance(fullDirectoryPath, str) or isinstance(fullDirectoryPath, Path)):
			fullDirectoryPath = PurePosixPath(fullDirectoryPath)
		fullDirectoryPath = str(fullDirectoryPath)
		for o in self.S3Bucket.objects.filter(Prefix=fullDirectoryPath):
			o.delete()

	def EmptyDirectory(self, fullDirectoryPath:Path|str) -> None:
		"""
		Removes all child objects within the directory, but does not remove the directory.

		Parameters
		----------
		fullDirectoryPath : Path or str
			The full path to the directory to clean.
		"""
		if (isinstance(fullDirectoryPath, str) or isinstance(fullDirectoryPath, Path)):
			fullDirectoryPath = PurePosixPath(fullDirectoryPath)
		fullDirectoryPath = str(fullDirectoryPath)
		if (not self.ExistsIndependent(fullDirectoryPath)):
			self.CreateDirectory(fullDirectoryPath, True)
		for o in self.S3Bucket.objects.filter(Prefix=fullDirectoryPath):
			if (f"{fullDirectoryPath}/" != o.key):
				o.delete()

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
		returnValue:list[TypedPath] = list[TypedPath]()
		if (isinstance(fullDirectoryPath, str) or isinstance(fullDirectoryPath, Path)):
			fullDirectoryPath = PurePosixPath(fullDirectoryPath)
		fullDirectoryPath = str(fullDirectoryPath)
		if (fullDirectoryPath == "." or fullDirectoryPath == "./"):
			fullDirectoryPath = ""
		asPath:PurePosixPath = PurePosixPath(fullDirectoryPath)
		foundObjects:any = None
		if (fullDirectoryPath is None or fullDirectoryPath == ""):
			foundObjects = self.S3Bucket.objects.all()
		else:
			foundObjects = self.S3Bucket.objects.filter(Prefix=fullDirectoryPath)
		for o in foundObjects:
			if (o.key != "./"
			and o.key != fullDirectoryPath
			and o.key != f"{fullDirectoryPath}/"):
				if (o.key.endswith("/")):
					relative:str = str(PurePosixPath(o.key).relative_to(asPath))
					root:str = ""
					if ("/" in relative):
						root = relative[:relative.index("/")]
					else:
						root = relative
					typedPath:TypedPath = TypedPath(asPath.joinpath(root), IOObjectType.Directory)
					if (not any(path.name == typedPath.name for path in returnValue)):
						returnValue.append(typedPath)
		return sorted(returnValue)

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
		returnValue:list[TypedPath] = list[TypedPath]()
		if (isinstance(fullDirectoryPath, str) or isinstance(fullDirectoryPath, Path)):
			fullDirectoryPath = PurePosixPath(fullDirectoryPath)
		fullDirectoryPath = str(fullDirectoryPath)
		if (fullDirectoryPath == "." or fullDirectoryPath == "./"):
			fullDirectoryPath = ""
		foundObjects:any = None
		if (fullDirectoryPath is None or fullDirectoryPath == ""):
			foundObjects = self.S3Bucket.objects.all()
		else:
			foundObjects = self.S3Bucket.objects.filter(Prefix=fullDirectoryPath)
		for o in foundObjects:
			if (o.key != "./"
			and o.key != fullDirectoryPath
			and o.key != f"{fullDirectoryPath}/"):
				if (o.key.endswith("/")):
					for path in self.SplitPathToPaths(o.key):
						typedPath:TypedPath = TypedPath(path, IOObjectType.Directory)
						if (not any(str(path) == str(typedPath) for path in returnValue)):
							returnValue.append(typedPath)
				else:
					for path in self.SplitPathToPaths(PurePosixPath(o.key).parent):
						typedPath:TypedPath = TypedPath(path, IOObjectType.Directory)
						if (not any(str(path) == str(typedPath) for path in returnValue)):
							returnValue.append(typedPath)
		return sorted(returnValue)

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
		returnValue:list[TypedPath] = list[TypedPath]()
		if (isinstance(fullDirectoryPath, str)):
			fullDirectoryPath = Path(fullDirectoryPath)
		allItems:list[Path] = self.ListAllDirectories(fullDirectoryPath)
		if (pattern == "*.*" or pattern == "*" or pattern == "" or pattern is None):
			for item in allItems:
				returnValue.append(item)
		else:
			for item in allItems:
				if (re.search(pattern, str(item.stem))):
					returnValue.append(item)
		return sorted(returnValue)

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
		returnValue:list[TypedPath] = list[TypedPath]()
		if (isinstance(fullDirectoryPath, str)):
			fullDirectoryPath = Path(fullDirectoryPath)
		allItems:list[Path] = self.ListAllDirectoriesRecursively(fullDirectoryPath)
		if (pattern == "*.*" or pattern == "*" or pattern == "" or pattern is None):
			for item in allItems:
				returnValue.append(item)
		else:
			for item in allItems:
				if (re.search(pattern, str(item.stem))):
					returnValue.append(item)
		return sorted(returnValue)

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
		returnValue:list[TypedPath] = list[TypedPath]()
		if (isinstance(fullDirectoryPath, str) or isinstance(fullDirectoryPath, Path)):
			fullDirectoryPath = PurePosixPath(fullDirectoryPath)
		fullDirectoryPath = str(fullDirectoryPath)
		if (fullDirectoryPath == "." or fullDirectoryPath == "./"):
			fullDirectoryPath = ""
		asPath:PurePosixPath = PurePosixPath(fullDirectoryPath)
		foundObjects:any = None
		if (fullDirectoryPath is None or fullDirectoryPath == ""):
			foundObjects = self.S3Bucket.objects.all()
		else:
			foundObjects = self.S3Bucket.objects.filter(Prefix=fullDirectoryPath)
		for o in foundObjects:
			if (o.key != "./"
			and o.key != fullDirectoryPath
			and o.key != f"{fullDirectoryPath}/"):
				if (not o.key.endswith("/")
					and "/" not in str(PurePosixPath(o.key).relative_to(asPath))):
					typedPath:TypedPath = TypedPath(o.key, IOObjectType.File)
					if (not any(str(path) == str(typedPath) for path in returnValue)):
						returnValue.append(typedPath)
		return sorted(returnValue)

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
		returnValue:list[TypedPath] = list[TypedPath]()
		fullDirectoryPath:Path = Path("asb")
		if (isinstance(fullDirectoryPath, str) or isinstance(fullDirectoryPath, Path)):
			fullDirectoryPath = PurePosixPath(fullDirectoryPath)
		fullDirectoryPath = str(fullDirectoryPath)
		if (fullDirectoryPath == "." or fullDirectoryPath == "./"):
			fullDirectoryPath = ""
		foundObjects:any = None
		if (fullDirectoryPath is None or fullDirectoryPath == ""):
			foundObjects = self.S3Bucket.objects.all()
		else:
			foundObjects = self.S3Bucket.objects.filter(Prefix=fullDirectoryPath)
		for o in foundObjects:
			if (o.key != "./"
			and o.key != fullDirectoryPath
			and o.key != f"{fullDirectoryPath}/"):
				if (not o.key.endswith("/")):
					typedPath:TypedPath = TypedPath(o.key, IOObjectType.File)
					if (not any(str(path) == str(typedPath) for path in returnValue)):
						returnValue.append(typedPath)
		return sorted(returnValue)

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
		returnValue:list[TypedPath] = list[TypedPath]()
		if (isinstance(fullDirectoryPath, str)):
			fullDirectoryPath = Path(fullDirectoryPath)
		allItems:list[Path] = self.ListAllFiles(fullDirectoryPath)
		if (pattern == "*.*" or pattern == "*" or pattern == "" or pattern is None):
			for item in allItems:
				returnValue.append(item)
		else:
			for item in allItems:
				if (re.search(pattern, str(item.stem))):
					returnValue.append(item)
		return sorted(returnValue)

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
		returnValue:list[TypedPath] = list[TypedPath]()
		if (isinstance(fullDirectoryPath, str)):
			fullDirectoryPath = Path(fullDirectoryPath)
		allItems:list[Path] = self.ListAllFilesRecursively(fullDirectoryPath)
		if (pattern == "*.*" or pattern == "*" or pattern == "" or pattern is None):
			for item in allItems:
				returnValue.append(item)
		else:
			for item in allItems:
				if (re.search(pattern, str(item.stem))):
					returnValue.append(item)
		return sorted(returnValue)

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
		returnValue:list[TypedPath] = list[TypedPath]()
		for typedPath in self.ListAllDirectories(fullDirectoryPath):
			if (not any(str(path) == str(typedPath) for path in returnValue)):
				returnValue.append(typedPath)
		for typedPath in self.ListAllFiles(fullDirectoryPath):
			if (not any(str(path) == str(typedPath) for path in returnValue)):
				returnValue.append(typedPath)
		return sorted(returnValue)

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
		returnValue:list[TypedPath] = list[TypedPath]()
		for typedPath in self.ListAllDirectoriesRecursively(fullDirectoryPath):
			if (not any(str(path) == str(typedPath) for path in returnValue)):
				returnValue.append(typedPath)
		for typedPath in self.ListAllFilesRecursively(fullDirectoryPath):
			if (not any(str(path) == str(typedPath) for path in returnValue)):
				returnValue.append(typedPath)
		return sorted(returnValue)

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
		if (isinstance(fullPath, str) or isinstance(fullPath, Path)):
			fullPath = PurePosixPath(fullPath)
		pathString:str = str(fullPath)
		if (not self.Exists(pathString)):
			raise ValueError("File does not exists")
		return self.S3Resource.Object(self.Bucket, pathString).get()["Body"].read()

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
		if (isinstance(fullPath, str) or isinstance(fullPath, Path)):
			fullPath = PurePosixPath(fullPath)
		parentPathString:str = f"{str(fullPath.parent)}/"
		if (not self.Exists(parentPathString)):
			raise ValueError("Parent does not exists")
		pathString:str = str(fullPath)
		self.S3Resource.Object(self.Bucket, pathString).put(Body=content)

	def RemoveFile(self, fullFilePath:Path|str) -> None:
		"""
		Removes the specified file.

		Parameters
		----------
		fullFilePath : Path or str
			The full path to the file to remove.
		"""
		if (isinstance(fullFilePath, str) or isinstance(fullFilePath, Path)):
			fullFilePath = PurePosixPath(fullFilePath)
		fullFilePath = str(fullFilePath)
		if (self.Exists(fullFilePath)):
			obj = self.S3Resource.Object(self.Bucket, fullFilePath).delete()

	def ParseTimestamps(self, paths:list[TypedPath], prefixesBeforeTimestamp:list[str] | None = None, timestampFormat:str | None = None) -> list[TimestampedPath]:
		returnValue:list[TimestampedPath] = list[TimestampedPath]()
		for item in paths:
			returnValue.append(TimestampedPath(item, prefixesBeforeTimestamp, timestampFormat))
		return returnValue

__all__ = ["S3ClearIO"]
