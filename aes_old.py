from argparse import ArgumentParser
from core.aes import *


def _encrypt(args):
	try:
		key, nonce, tag, data = aes_encrypt(args.m, args.s, args.k, args.kb64, args.g, args.o)
	except Error as err:
		print(f"aes: error: {err}")
		exit()
	except ValueError as err:
		print(f"aes: error: {err}")
		exit()

	if args.g:
		print(f"Key: {key}")
	
	if not args.o:
		print(f"Nonce: {nonce}")
		print(f"Tag: {tag}")
		print(data)

	if not args.w:
		print("aes: warning: make sure you have copied these values. You won't be able to see them again")


def _decrypt(args):
	try:
		data = aes_decrypt(args.m, args.s, args.k[0], args.kb64, args.k[1], args.k[2], args.o)
	except Error as err:
		print(f"aes: error: {err}")
		exit()
	except ValueError as err:
		print(f"aes: error: {err}")
		exit()
	
	if not args.o:
		print(data)


parser = ArgumentParser(prog="aes", description="Encrypts and decrypts data with AES algorithm")
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
parser_e_key.add_argument("-kb64", metavar="<key>", help="A key for encryption (base64)")
parser_e_key.add_argument("-g", metavar="<n>", type=int, choices=[128, 192, 256],
	help="Generate a key, n - number of bits (128 - not recommended | 192  | 256)")

# parser_e.add_argument("-j", metavar="<file>",
# 	help="Put the keys in a JSON file. If not specified, it will print on the screen")

parser_d_input = parser_d.add_mutually_exclusive_group(required=True)
parser_d_input.add_argument("-m", metavar="<msg>", help="Message to decrypt")
parser_d_input.add_argument("-s", metavar="<file>", help="File to decrypt")

parser_d_key = parser_d.add_mutually_exclusive_group(required=True)
parser_d_key.add_argument("-k", metavar=("<key>", "<nonce>", "<tag>"), nargs=3,
	help="A key for decryption (must be 128, 192 or 256 bits long), nonce for decryption and mac tag for data authentification")
parser_d_key.add_argument("-kb64", metavar=("<key>", "<nonce>", "<tag>"), nargs=3,
	help="A key for decryption (base64), nonce and tag")
parser_d_key.add_argument("-j", metavar="<file>",
	help="A JSON file that stores the values of key, nonce and tag")

parser.add_argument("-o", metavar="<file>", help="Output file. If not specified, it will print on the screen")
parser.add_argument("-w", action="store_true", help="Suppress warnings")

args = parser.parse_args()
args.func(args)