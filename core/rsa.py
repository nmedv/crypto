# import rsa
# from rsa import key, common
# import math
import argparse

parser = argparse.ArgumentParser(
	prog="rsa",
	description="Encrypts and decrypts data with RSA algorith.")
group_input = parser.add_mutually_exclusive_group(required=True)
group_input.add_argument("-e", metavar="<file>", type=str, help="Encrypt file")
group_input.add_argument("-d", metavar="<file>", type=str, help="Decrypt file")
group_key = parser.add_mutually_exclusive_group(required=True)
group_key.add_argument("-k", metavar="({e, n} | {d, n})", type=str,
	help="A public key for encryption or a private key for decryption")
group_key.add_argument("-kf", metavar="<file>", type=str,
	help="A file with a public key for encryption or a private key for decryption")
group_key.add_argument("-g", metavar="<n>", type=int, nargs="?", default=2048,
	help="Generate a public and private key, n - number of bits (2048 by default)")
parser.add_argument("-o", metavar="<file>", type=str,
	help="Output file. If not specified, it will print on the screen")
args = parser.parse_args()

if args.k:
	print(args.k)

# if args.e:
# 	data = bytes(args.e)
# elif args.ef:
# 	file = open(args.ef, "rb")
# 	if file.readable():
# 		data = file.read()
# 	else:
# 		file.close()
# 		print(f"rsa: error: can't read file \"{args.ef}\"")
# 		exit()
# 	file.close()
# else:
# 	print("rsa: error: no input")
# 	exit()



# (pub_key, priv_key) = key.newkeys(keybits)
# max_block_size = common.byte_size(pub_key.n) - 11

# data_blocks = []
# for i in range(math.ceil(len(data) / max_block_size)):
# 	data_blocks.append(data[i * max_block_size:(i + 1) * max_block_size])

# data_blocks_encrypted = []
# for block in data_blocks:
# 	data_blocks_encrypted.append(rsa.encrypt(block, pub_key))

# data_encrypted = b"".join(data_blocks_encrypted)