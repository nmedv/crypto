from core.gammer import gammer, Error

import argparse
parser = argparse.ArgumentParser(
	prog="gammer",
	description="Encrypts and decrypts data using gamma encryption.",
	epilog="To decrypt, the data must be re-encrypted using this tool.")

parser.add_argument("-d", action="store_true", help="Decrypt data")

parser_input = parser.add_mutually_exclusive_group(required=True)
parser_input.add_argument("-m", metavar="<msg>", help="Message for encryption")
parser_input.add_argument("-s", metavar="<file>", help="Data source file for encryption")

parser_gamma = parser.add_mutually_exclusive_group(required=True)
parser_gamma.add_argument("-g", metavar="<gamma>", help="Gamma")
parser_gamma.add_argument("-gb64", metavar="<gamma>", help="Gamma (base64)")
parser_gamma.add_argument("-gs", metavar="<file>", help="Gamma source file")
parser_gamma.add_argument("-gsb64", metavar="<file>", help="Gamma source file (base64)")
parser_gamma.add_argument("-gn", metavar="<n>", type=int, help="Generate gamma, n - number of bytes")

parser.add_argument("-o", metavar="<file>", help="Output file. If not specified, it will print on the screen")
parser.add_argument("-e", metavar="<encoding>", default="utf-8", help="Data encoding. Default is \"utf-8\"")
parser.add_argument("-w", action="store_true", help="Suppress warnings")

args = parser.parse_args()

try:
	gamma, result = gammer(
		args.m,
		args.s,
		args.d,
		args.g,
		args.gb64,
		args.gn,
		args.gs,
		args.gsb64,
		args.o,
		args.e)
except Error as err:
	print(f"gammer: error: {err}")
	exit()

if args.gn:
	print(f"gamma: {gamma}")
	if not args.w:
		if args.d:
			print("gammer: warning: decryption uses randomly generated gamma")
		else:
			print("gammer: warning: make sure you have copied these value. You won't be able to see it again")

if not args.o:
	print(f"result: {result}")