import random

# Print numeric representation of string
# data - string
# len - length of string
# mod - (0 = bin; 1 = hex; 2 = dec). Use macros:
BIN = 0
HEX = 1
DEC = 2
# cols - amount of columns
def print_data(data: str, mod: int, cols: int):
	for i in range(len(data)):
		if mod == BIN:
			print(f"{ord(data[i]):b}", end="")
		elif mod == HEX:
			print(f"{ord(data[i]):x}", end="")
		elif mod == DEC:
			print(ord(data[i]), end="")
		if (i + 1) % cols == 0 or i == len(data) - 1:
			print()
		else: print("\t", end="")

def gamma(data: str, g: str):
	res = list(data)
	g_len = len(g)
	j = 0
	for i in range(len(data)):
		res[i] = chr(ord(data[i]) ^ ord(g[j]))
		if j == g_len - 1:
			j = 0
		else:
			j += 1
	res = "".join(res)
	return res

def gen_gamma(len: int):
	res: str
	for i in range(len):
		res += chr(random.randint(0, 65535))
	return res

import argparse
parser = argparse.ArgumentParser(
	prog="gammer",
	description="Encrypts and decrypts data using gamma encryption.",
	epilog="To decrypt, the data must be re-encrypted using this tool.")
parser.add_argument("-m", metavar="--msg", help="Message for encryption")
parser.add_argument("-s", metavar="--src", help="Data source file for encryption")
parser.add_argument("-g", metavar="--gamma", help="Gamma")
parser.add_argument("-gs", metavar="--gamma-src", help="Gamma source file")
parser.add_argument("-o", metavar="--output", help="Output file. If not specified, it will print on the screen")
# parser.add_argument("-p", action="store_true", help="Print output")
args = parser.parse_args()

if args.m:
	s = args.m
elif args.s:
	file = open(args.s, "r", encoding="utf8")
	if file.readable():
		s = file.read()
	else:
		file.close()
		print(f"gammer: error: can't read file \"{args.s}\"")
		exit()
	file.close()
else:
	print("gammer: error: no input")
	exit()

if args.g:
	g = args.g
elif args.gs:
	g_file = open(args.gs, "r")
	if g_file.readable():
		g = g_file.read()
	else:
		g_file.close()
		print(f"gammer: error: can't read file \"{args.gs}\"")
		exit()
	g_file.close()
else:
	print("gammer: error: no gamma")
	exit()

r = gamma(s, g)

if args.o:
	o_file = open(args.o, "w", encoding="utf8")
	if o_file.writable():
		o_file.write(r)
	else:
		o_file.close()
		print(f"gammer: error: can't write to file \"{args.gs}\"")
	o_file.close()
else:
	print(r)
	exit()