from core.utils import writefileb
from core.utils import strtobytes, bytestostr
from core.aes import AES_encrypt, AES_decrypt
from core.exeptions import Error
from hashlib import sha256
import json

class Pwm:

	def __init__(self, datafile: str, masterpw: str):
		self.datafile = datafile
		self.masterpw = sha256(strtobytes(masterpw)).digest()

		try:
			with open(self.datafile, "rb") as df:
				self.alldata = df.read()
			self.newfile = False
		except:
			self.alldata = b""
			self.newfile = True

		if self.newfile:
			self.pwmap = {}
		else:
			if self.alldata[:2] != b"pw":
				raise Error("wrong file signature")
			
			self.nonce_size = self.alldata[2]
			self.tag_size = self.alldata[3]
			self.data_size = int.from_bytes(self.alldata[4:6])
			ptr = 6
			self.nonce = self.alldata[ptr : ptr + self.nonce_size]
			ptr += self.nonce_size
			self.tag = self.alldata[ptr : ptr + self.tag_size]
			ptr += self.tag_size
			self.data_encrypted = self.alldata[ptr : ptr + self.data_size]

			try:
				self.data_decrypted = AES_decrypt(self.data_encrypted, self.masterpw, self.nonce, self.tag)
			except:
				return None
			
			self.pwmap: dict = json.loads(bytestostr(self.data_decrypted))


	def get(self, name: str):
		if name == "*":
			return self.pwmap
		else:
			try:
				return self.pwmap[name]
			except:
				raise Error(f"can't find password with name \"{name}\"")


	def exists(self, name: str):
		return name in self.pwmap


	def set(self, name: str, pw: str):
		if name == "*":
			raise Error("can't create a password with name \"*\"")
		else:
			self.pwmap[name] = pw


	def remove(self, name: str):
		try:
			if name == "*":
				self.pwmap.clear()
			else:
				self.pwmap.pop(name)
		except:
			raise Error(f"can't find password with name \"{name}\"")


	def save(self):
		self.data_decrypted = strtobytes(json.dumps(self.pwmap))
		self.data_encrypted, self.nonce, self.tag = AES_encrypt(self.data_decrypted, self.masterpw)
		self.nonce_size = len(self.nonce)
		self.tag_size = len(self.tag)
		self.data_size = len(self.data_encrypted)
		self.alldata = \
			b"pw" + \
			self.nonce_size.to_bytes() + \
			self.tag_size.to_bytes() + \
			self.data_size.to_bytes(2) + \
			self.nonce + \
			self.tag + \
			self.data_encrypted
		
		writefileb(self.datafile, self.alldata)


def yesorno(msg: str):
	inp = ""
	try:
		while inp != "y" and inp != "n":
			inp = input(msg)
		if inp == "y": return True
		else: return False
	except KeyboardInterrupt:
		return False