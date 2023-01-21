from base64 import b64encode as _b64encode
from base64 import b64decode as _b64decode
from core.exeptions import Error


def b64encode(data: bytes, encoding = "utf-8"):
	return _b64encode(data).decode(encoding)


def b64decode(data: str):
	try:
		return _b64decode(data)
	except:
		raise Error(f"invalid base64: \"{data}\"")


def strtobytes(data: str, encoding = "utf-8"):
	try:
		return bytes(data, encoding)
	except:
		raise Error(f"can't read \"{data[:16]}...\" with encoding \"{encoding}\"")


def bytestostr(data: bytes, encoding = "utf-8"):
	try:
		return data.decode(encoding)
	except:
		raise Error(f"can't read data in \"{encoding}\" encoding")


def readfile(file: str, encoding: str = "utf-8"):
	try:
		with open(file, "r", encoding=encoding) as f:
			if f.readable():
				return f.read()
			else:
				raise Error(f"can't read file: \"{file}\"")
	except FileNotFoundError:
		raise Error(f"file not found: \"{file}\"")
	except OSError:
		raise Error(f"invalid path: \"{file}\"")


def readfileb(file: str):
	try:
		with open(file, "rb") as f:
			if f.readable():
				return f.read()
			else:
				raise Error(f"can't read file: \"{file}\"")
	except FileNotFoundError:
		raise Error(f"file not found: \"{file}\"")
	except OSError:
		raise Error(f"invalid path: \"{file}\"")


def writefile(file: str, data: str):
	with open(file, "w") as f:
		if f.writable():
			return f.write(data)
		else:
			raise Error(f"can't write to file: \"{file}\"")


def writefileb(file: str, data: str):
	with open(file, "wb") as f:
		if f.writable():
			return f.write(data)
		else:
			raise Error(f"can't write to file: \"{file}\"")