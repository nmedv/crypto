from Crypto.Random import get_random_bytes
from core.utils import b64encode, b64decode
from core.utils import strtobytes, bytestostr
from core.utils import readfile, writefile, readfileb, writefileb
from core.exeptions import Error


def gamma(__data: bytes, __gamma: bytes):
	res = bytearray(__data)
	g_len = len(__gamma)
	j = 0
	for i in range(len(res)):
		res[i] ^= __gamma[j]
		if j == g_len - 1:
			j = 0
		else:
			j += 1
	
	return bytes(res)


def gammer(
	data: str = None,
	source: str = None,
	decrypt = False,
	gm: str = None,
	gmb64 : str = None,
	gmn = 64,
	gmsource : str = None,
	gmsourceb64: str = None,
	output: str = None,
	encoding = "utf-8"
):
	if data:
		if decrypt:
			d = b64decode(data)
		else:
			d = strtobytes(data, encoding)
	elif source:
		if decrypt:
			# d = b64decode(readfile(source, encoding))
			d = b64decode(readfileb(source))
		else:
			# d = bytes(readfile(source, encoding), encoding)
			d = readfileb(source)
	else:
		raise Error("no input data")

	if gm:
		g = strtobytes(gm, encoding)
		gstr = gm
	elif gmb64:
		g = b64decode(gmb64)
		gstr = gm
	elif gmn:
		g = get_random_bytes(gmn)
		gstr = b64encode(g, encoding)
	elif gmsource:
		gstr = readfile(gmsource, encoding)
		g = strtobytes(gstr, encoding)
	elif gmsourceb64:
		gstr = readfile(gmsourceb64, encoding)
		g = strtobytes(gstr, encoding)
	else:
		raise Error("no gamma")

	if decrypt:
		try:
			res = gamma(d, g).decode(encoding)
		except:
			raise Error(f"can't decode data decrypted with gamma \"{gstr}\" in \"{encoding}\" encoding")
	else:
		res = b64encode(gamma(d, g), encoding)
	
	if output: writefile(output, res)

	return (gstr, res)

# def gammer(
# 	data: str = None,
# 	source: str = None,
# 	decrypt = False,
# 	gm: str = None,
# 	gmb64 : str = None,
# 	gmn = 64,
# 	gmsource : str = None,
# 	gmsourceb64: str = None,
# 	output: str = None,
# 	encoding = "utf-8"):

# 	if data:
# 		if decrypt:
# 			d = b64decode(data)
# 		else:
# 			d = strtobytes(data, encoding)
# 	elif source:
# 		if decrypt:
# 			#d = b64decode(readfile(source, encoding))
# 			d = b64decode(readfileb(source))
# 		else:
# 			#d = bytes(readfile(source, encoding), encoding)
# 			d = readfileb(source)
# 	else:
# 		raise Error("no input data")

# 	if gm:
# 		g = strtobytes(gm, encoding)
# 		gstr = gm
# 	elif gmb64:
# 		g = b64decode(gmb64)
# 		gstr = gm
# 	elif gmn:
# 		g = get_random_bytes(gmn)
# 		gstr = b64encode(g, encoding)
# 	elif gmsource:
# 		gstr = readfile(gmsource, encoding)
# 		g = strtobytes(gstr, encoding)
# 	elif gmsourceb64:
# 		gstr = readfile(gmsourceb64, encoding)
# 		g = strtobytes(gstr, encoding)
# 	else:
# 		raise Error("no gamma")

# 	if decrypt:
# 		try:
# 			res = gamma(d, g).decode(encoding)
# 		except:
# 			raise Error(f"can't decode data decrypted with gamma \"{gstr}\" in \"{encoding}\" encoding")
# 	else:
# 		res = b64encode(gamma(d, g), encoding)
	
# 	if output: writefile(output, res)

# 	return (gstr, res)