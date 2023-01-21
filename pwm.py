from argparse import ArgumentParser
from core.pwm import Pwm


def yesorno(msg: str):
	inp = ""
	try:
		while inp != "y" and inp != "n":
			inp = input(msg)
		if inp == "y": return True
		else: return False
	except KeyboardInterrupt:
		return False


parser = ArgumentParser(prog="pwm", description="Password manager")

parser.add_argument("name", help="Password name")
parser.add_argument("password", nargs="?", help="Password")
parser.add_argument("-s", metavar="<file>", default="data.pw", help="Data file")
parser.add_argument("-r", action="store_true", help="Remove password")
parser.add_argument("-f", action="store_true", help="Suppress warnings")

args = parser.parse_args()
masterpw = input("Master password: ")
try:
	if args.password:
		pwm = Pwm(args.s, masterpw)
		if pwm.exists(args.name):
			if args.f:
				pwm.set(args.name, args.password)
				pwm.save()
			else:
				print(f"pwm: warning: a password with name \"{args.name}\" already exists")
				if yesorno("Are you sure you want to overwrite it? (y, n): "):
					pwm.set(args.name, args.password)
					pwm.save()
				else:
					exit()
		else:
			pwm.set(args.name, args.password)
			pwm.save()
	else:
		pwm = Pwm(args.s, masterpw)
		if args.name == "*":
			if args.r:
				if args.f:
					pwm.remove("*")
					pwm.save()
				else:
					print(f"pwm: warning: this action will remove ALL existing passwords")
					if yesorno("Are you sure you want to continue? (y, n): "):
						pwm.remove("*")
						pwm.save()
					else:
						exit()
			else:
				res = pwm.get(args.name)
				for name in res:
					print(f"{name}: {res[name]}")
		else:
			if args.r:
				if args.f:
					pwm.remove(args.name)
					pwm.save()
				else:
					print(f"pwm: warning: this action will remove \"{args.name}\" password")
					if yesorno("Are you sure you want to continue? (y, n): "):
						pwm.remove(args.name)
						pwm.save()
					else:
						exit()
			else:
				print(pwm.get(args.name))
except Exception as err:
	print(f"pwm: error: {err}")