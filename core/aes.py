import json
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from core.utils import *
from core.exeptions import Error


def AES_genkey(nbits: int):
	return get_random_bytes(nbits // 8)


def AES_encrypt(data: bytes, key: bytes):
	cipher = AES.new(key, AES.MODE_EAX)
	nonce: bytes = cipher.nonce
	data_encrypted, tag = cipher.encrypt_and_digest(data)
	return data_encrypted, nonce, tag


def AES_decrypt(data_encrypted: bytes, key: bytes, nonce: bytes, tag: bytes):
	uncipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
	data_decrypted = uncipher.decrypt(data_encrypted)
	try:
		uncipher.verify(tag)
	except ValueError:
		raise Error(f"authentification failed, tag: \"{b64encode(tag)}\"")
	return data_decrypted


def AES_test():
	data = b"some data"
	key = AES_genkey(256)
	data_encrypted, nonce, tag = AES_encrypt(data, key)
	data_decrypted = AES_decrypt(data_encrypted, key, nonce, tag)
	return data_decrypted == b"some data"


def aes_encrypt(
	data: str = None,
	source: str = None,
	key: str = None,
	keyb64: str = None,
	output: str = None
):
	if data:
		d = strtobytes(data)
	elif source:
		d = readfileb(source)
	
	if key:
		k = strtobytes(key)
	elif keyb64:
		k = b64decode(key)
	
	data_encrypted, new_nonce, new_tag = AES_encrypt(d, k)
	nstr = b64encode(new_nonce)
	tstr = b64encode(new_tag)
	destr = b64encode(data_encrypted)

	if output:
		# keys_dict = {"key": b64encode(key), "nonce": b64encode(nonce), "tag": b64encode(tag)}
		keys_dict = {"nonce": nstr, "tag": tstr, "data": destr}
		writefile(output, json.dumps(keys_dict, indent=4))
	
	return nstr, tstr, destr


def aes_decrypt(
	data: str = None,
	source: str = None,
	key: str = None,
	keyb64: str = None,
	nonce: str = None,
	tag: str = None,
	output: str = None
):
	if data:
		data_encrypted = b64decode(data)
		n = b64decode(nonce)
		t = b64decode(tag)
	elif source:
		try:
			keys_dict: dict = json.loads(readfile(source))
		except:
			raise Error(f"can't decode JSON data: \"{source}\"")
		n = b64decode(keys_dict["nonce"])
		t = b64decode(keys_dict["tag"])
		data_encrypted = b64decode(keys_dict["data"])
	
	if key:
		k = strtobytes(key)
	elif keyb64:
		k = b64decode(keyb64)

	data_decrypted = AES_decrypt(data_encrypted, k, n, t)

	if not data_encrypted:
		raise Error("can't decrypt: key incorrect or data corrupted")

	if output:
		writefileb(output, data_decrypted)

	return bytestostr(data_decrypted)