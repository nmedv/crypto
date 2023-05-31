from argparse import ArgumentParser
from core.pwm import Pwm, yesorno


parser = ArgumentParser(prog="pwm", description="Password manager")

parser.add_argument("name", help="Password name")
parser.add_argument("password", nargs="?", help="Password")
parser.add_argument("-s", metavar="<file>", default="data.pw", help="Data file")
parser.add_argument("-r", action="store_true", help="Remove password")
parser.add_argument("-f", action="store_true", help="Suppress warnings")

args = parser.parse_args()

try:
	masterpw = input("Master password: ")
	pwm = Pwm(args.s, masterpw)
	if not pwm:
		print("pwm: error: wrong master password")
		exit()

	if args.password:
		confirm = True
		if not args.f and pwm.exists(args.name):
			print(f"pwm: warning: a password with name \"{args.name}\" already exists")
			confirm = yesorno("Are you sure you want to overwrite it? (y, n): ")
		if confirm:
			pwm.set(args.name, args.password)
			pwm.save()
	elif args.r:
		confirm = True
		if not pwm.exists(args.name):
			print(f"pwm: error: password with name \"{args.name}\" doesn't exists")
			exit()
		if not args.f:
			if args.name == "*":
				print(f"pwm: warning: this action will remove ALL existing passwords")
			else:
				print(f"pwm: warning: this action will remove \"{args.name}\" password")
			confirm = yesorno("Are you sure you want to overwrite it? (y, n): ")
		if confirm:
			pwm.remove(args.name)
			pwm.save()
	else:
		res = pwm.get(args.name)
		if args.name == "*":
			for name in res:
				print(f"{name}: {res[name]}")
		else:
			print(pwm.get(args.name))

except Exception as err:
	print(f"pwm: error: {err}")