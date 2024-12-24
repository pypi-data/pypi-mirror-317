import json

class savedata:
	def __init__(self, filename, enckey="", _type=0):
		self.key = enckey
		self.filename = filename
		self._type = _type
		self._data = {}

	@property
	def type(self):
		return self._type

	@type.setter
	def type(self, value):
		self._type = value

	def load(self):
		try:
			with open(self.filename, "r") as f:
				data = f.read()
				if self.key:
					data = self.decrypt(data, self.key)
				if self._type == 0:
					self._data = json.loads(data)
				else:
					self._data = self.ini_to_dict(data)
		except FileNotFoundError:
			pass

	def save(self):
		if self._type == 0:
			data = json.dumps(self._data)
		else:
			data = self.dict_to_ini(self._data)
		if self.key:
			data = self.encrypt(data, self.key)
		with open(self.filename, "w") as f:
			f.write(data)

	def add(self, name, value):
		self._data[name] = value

	def read(self, name):
		return self._data.get(name, "")

	@property
	def keys(self):
		return list(self._data.keys())

	def exists(self, key):
		return key in self._data

	def clear(self):
		self._data.clear()

	def decrypt(self, data, key):
		# I have no knowledge
		return data

	def encrypt(self, data, key):
		# I have no knowledge
		return data

	def ini_to_dict(self, data):
		d = {}
		for line in data.split("\n"):
			if "=" in line:
				key, value = line.split("=", 1)
				d[key] = value
		return d

	def dict_to_ini(self, d):
		lines = []
		for key, value in d.items():
			lines.append(f"{key}={value}")
		return "\n".join(lines)
