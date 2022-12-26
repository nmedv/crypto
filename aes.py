from argparse import ArgumentParser
from base64 import b64encode, b64decode
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import json

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
		return
	return data_decrypted


def AES_test():
	data = b"some data"
	key = AES_genkey(256)
	data_encrypted, nonce, tag = AES_encrypt(data, key)
	data_decrypted = AES_decrypt(data_encrypted, key, nonce, tag)
	return data_decrypted == b"some data"


def _b64encode(data: bytes, encoding: str = "utf-8"):
	return b64encode(data).decode(encoding=encoding)


def _b64decode(data: str):
	try:
		return b64decode(data)
	except:
		print(f"aes: error: invalid base64: \"{data}\"")


def _read_file(file: str, encoding: str = "utf-8"):
	try:
		with open(file, "r", encoding=encoding) as f:
			if f.readable():
				return f.read()
			else:
				print(f"aes: error: can't read file: \"{file}\"")
	except FileNotFoundError:
		print(f"aes: error: file not found: \"{file}\"")


def _write_file(file: str, data: str):
	with open(file, "w") as f:
		if f.writable():
			return f.write(data)
		else:
			print(f"aes: error: can't write to file: \"{file}\"")


def _encrypt(args):
	if args.m:
		data = args.m
	elif args.s:
		data = _read_file(args.s)
		if not data: return
	
	if args.k:
		if len(args.k) == 16 or len(args.k) == 24 or len(args.k) == 32:
			key = _b64decode(args.k)
			if not key: return
		else:
			print("aes: error: the key must be 128, 192 or 256 bits long")
			return
	elif args.g:
		key = AES_genkey(args.g)
	
	data_encrypted, nonce, tag = AES_encrypt(data, key)
	keys_dict = {"key": _b64encode(key), "nonce": _b64encode(nonce), "tag": _b64encode(tag)}

	if args.j:
		if not _write_file(args.j, json.dumps(keys_dict, indent=4)): return
	else:
		for k in keys_dict:
			print(f"{k}:\t{keys_dict[k]}")
		print("aes: warning: make sure you have copied these values. You won't be able to see them again")
	
	return _b64encode(data_encrypted)


def _decrypt(args):
	if args.m:
		data_encrypted = _b64decode(args.m)
		if not data_encrypted: return
	elif args.s:
		data_encrypted = _read_file(args.s)
		if not data_encrypted: return
		data_encrypted = _b64decode(data_encrypted)
		if not data_encrypted: return
	
	if args.k:
		key = _b64decode(args.k[0])
		if not key: return
		nonce = _b64decode(args.k[1])
		if not nonce: return
		tag = _b64decode(args.k[2])
		if not tag: return
	elif args.j:
		keys_json = _read_file(args.j)
		if not keys_json: return
		try:
			keys_dict: dict = json.loads(keys_json)
		except:
			print(f"aes: error: can't decode JSON data: \"{args.j}\"")
			return
		key = _b64decode(keys_dict["key"])
		if not key: return
		nonce = _b64decode(keys_dict["nonce"])
		if not nonce: return
		tag = _b64decode(keys_dict["tag"])
		if not tag: return

	data_decrypted = AES_decrypt(data_encrypted, key, nonce, tag)
	if data_decrypted:
		return data_decrypted.decode('utf8')
	else:
		print("aes: error: can't decrypt: key incorrect or data corrupted")


parser = ArgumentParser(prog="aes", description="Encrypts and decrypts data with AES algorith")
subparsers = parser.add_subparsers(required=True)
parser_e = subparsers.add_parser("encrypt", help="Encrypt data")
parser_e.set_defaults(func=_encrypt)
parser_d = subparsers.add_parser("decrypt", help="Decrypt data")
parser_d.set_defaults(func=_decrypt)

parser_e_input = parser_e.add_mutually_exclusive_group(required=True)
parser_e_input.add_argument("-m", metavar="<msg>", help="Message to encrypt")
parser_e_input.add_argument("-s", metavar="<file>", help="File to encrypt")

parser_e_key = parser_e.add_mutually_exclusive_group(required=True)
parser_e_key.add_argument("-k", metavar="<key>",
	help="A key for encryption, must be 128, 192 or 256 bits long. Always use different keys for encryption!")
parser_e_key.add_argument("-g", metavar="<n>", type=int, choices=[128, 192, 256],
	help="Generate a key, n - number of bits (128 - not recommended | 192  | 256)")

parser_e.add_argument("-j", metavar="<file>",
	help="Put the keys in a JSON file. If not specified, it will print on the screen")

parser_d_input = parser_d.add_mutually_exclusive_group(required=True)
parser_d_input.add_argument("-m", metavar="<msg>", help="Message to decrypt")
parser_d_input.add_argument("-s", metavar="<file>", help="File to decrypt")

parser_d_key = parser_d.add_mutually_exclusive_group(required=True)
parser_d_key.add_argument("-k", metavar=("<key>", "<nonce>", "<tag>"), nargs=3,
	help="A key for decryption (must be 128, 192 or 256 bits long), nonce for decryption and mac tag for data authentification")
parser_d_key.add_argument("-j", metavar="<file>",
	help="A JSON file that stores the values of key, nonce and tag")

parser.add_argument("-o", metavar="<file>", help="Output file. If not specified, it will print on the screen")

args = parser.parse_args()
result = args.func(args)
if result:
	if args.o:
		_write_file(args.o, result)
	else:
		print(result)