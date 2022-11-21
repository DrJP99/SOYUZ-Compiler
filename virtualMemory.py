'''
global variables: (0 - 1999)
	int			: (0 - 499)
	float		: (500 - 999)
	char		: (1000 - 1499)
	bool 		: (1500 - 1999)

local variables	: (2000 - 5999)		# includes temporary variables
	int			: (2000 - 2999)
	float		: (3000 - 3999)
	char		: (4000 - 4999)
	bool 		: (5000 - 5999)

constants		: (6000 - 9999)		# are global
	int			: (6000 - 6999)
	float		: (7000 - 7999)
	char		: (8000 - 8999)
	bool 		: (9000 - 9999)
'''	
# CHAR is stored as INTs, min = 0, max = 127

import json


class VirtualMemory:
	def __init__(self):
		self.global_int_start = 0
		self.global_float_start = 500
		self.global_char_start = 1000
		self.global_bool_start = 1500
		
		self.max_global_int = 499
		self.max_global_float = 999
		self.max_global_char =  1499
		self.max_global_bool = 1999

		self.local_int_start = 2000
		self.local_float_start = 3000
		self.local_char_start = 4000
		self.local_bool_start = 5000

		self.max_local_int = 2999
		self.max_local_float = 3999
		self.max_local_char = 4999
		self.max_local_bool = 5999

		self.constant_int_start = 6000
		self.constant_float_start = 7000
		self.constant_char_start = 8000
		self.constant_bool_start = 9000

		self.max_constant_int = 6999
		self.max_constant_float = 7999
		self.max_constant_char = 8999
		self.max_constant_bool = 9999

		self.g_i_counter = self.global_int_start
		self.g_f_counter = self.global_float_start
		self.g_c_counter = self.global_char_start
		self.g_b_counter = self.global_bool_start

		self.l_i_counter = self.local_int_start
		self.l_f_counter = self.local_float_start
		self.l_c_counter = self.local_char_start
		self.l_b_counter = self.local_bool_start

		self.c_i_counter = self.constant_int_start
		self.c_f_counter = self.constant_float_start
		self.c_c_counter = self.constant_char_start
		self.c_b_counter = self.constant_bool_start

		self.memory = {}

		self.resourceInt = 0		# Used to count int temporary variables
		self.resourceFloat = 0		# Used to count float temporary variables
		self.resourceBool = 0		# Used to count bool temporary variables
		self.resourceChar = 0		# Used to count char temporary variables
	
	# Creates virtual memory address for declared variables
	def create_global_int(self):
		if (self.g_i_counter <= self.max_global_int):
			self.memory[self.g_i_counter] = 0
			self.g_i_counter += 1
			self.resourceInt += 1
			return self.g_i_counter - 1
		else:
			print("Error: no more global int memory available")
			exit()

	def create_global_float(self):
		if (self.g_f_counter <= self.max_global_float):
			self.memory[self.g_f_counter] = 0.0
			self.g_f_counter += 1
			self.resourceFloat += 1
			return self.g_f_counter - 1
		else:
			print("Error: no more global float memory available")
			exit()
	
	def create_global_char(self):
		if (self.g_c_counter <= self.max_global_char):
			self.memory[self.g_c_counter] = 0
			self.g_c_counter += 1
			self.resourceChar += 1
			return self.g_c_counter - 1
		else:
			print("Error: no more global char memory available")
			exit()
	
	def create_global_bool(self):
		if (self.g_b_counter <= self.max_global_bool):
			self.memory[self.g_b_counter] = False
			self.g_b_counter += 1
			self.resourceBool += 1
			return self.g_b_counter - 1
		else:
			print("Error: no more global bool memory available")
			exit()

	def create_local_int(self):
		if (self.l_i_counter <= self.max_local_int):
			self.memory[self.l_i_counter] = 0
			self.l_i_counter += 1
			self.resourceInt += 1
			return self.l_i_counter - 1
		else:
			print("Error: no more local int memory available")
			exit()
	
	def create_local_float(self):
		if (self.l_f_counter <= self.max_local_float):
			self.memory[self.l_f_counter] = 0.0
			self.l_f_counter += 1
			self.resourceFloat += 1
			return self.l_f_counter - 1
		else:
			print("Error: no more local float memory available")
			exit()
	
	def create_local_char(self):
		if (self.l_c_counter <= self.max_local_char):
			self.memory[self.l_c_counter] = 0
			self.l_c_counter += 1
			self.resourceChar += 1
			return self.l_c_counter - 1
		else:
			print("Error: no more local char memory available")
			exit()
	
	def create_local_bool(self):
		if (self.l_b_counter <= self.max_local_bool):
			self.memory[self.l_b_counter] = False
			self.l_b_counter += 1
			self.resourceBool += 1
			return self.l_b_counter - 1
		else:
			print("Error: no more local bool memory available")
			exit()
	
	def create_constant_int(self, value=0):
		if (self.c_i_counter <= self.max_constant_int):
			self.memory[self.c_i_counter] = value
			self.c_i_counter += 1
			return self.c_i_counter - 1
		else:
			print("Error: no more constant int memory available")
			exit()
	
	def create_constant_float(self, value=0.0):
		if (self.c_f_counter <= self.max_constant_float):
			self.memory[self.c_f_counter] = value
			self.c_f_counter += 1
			return self.c_f_counter - 1
		else:
			print("Error: no more constant float memory available")
			exit()
	
	def create_constant_char(self, value=0):
		if (self.c_c_counter <= self.max_constant_char):
			self.memory[self.c_c_counter] = value
			self.c_c_counter += 1
			return self.c_c_counter - 1
		else:
			print("Error: no more constant char memory available")
			exit()
	
	def create_constant_bool(self, value=False):
		if (self.c_b_counter <= self.max_constant_bool):
			self.memory[self.c_b_counter] = value
			self.c_b_counter += 1
			return self.c_b_counter - 1
		else:
			print("Error: no more constant bool memory available")
			exit()
			
	
	def create_many_memory(self, scope, type, mySize=1):
		addressStart = -1
		if (mySize > 0):
			addressStart = self.create_memory(scope, type)

		for i in range(1, mySize):
			self.create_memory(scope, type)
		
		return addressStart

	def create_memory(self, scope, type, const=False):
		if (not const):
			if (scope == 0):
				if (type == "int"):
					return self.create_global_int()
				elif (type == "float"):
					return self.create_global_float()
				elif (type == "char"):
					return self.create_global_char()
				elif (type == "bool"):
					return self.create_global_bool()
			elif (scope > 0):
				if (type == "int"):
					return self.create_local_int()
				elif (type == "float"):
					return self.create_local_float()
				elif (type == "char"):
					return self.create_local_char()
				elif (type == "bool"):
					return self.create_local_bool()
			else:
				print(f"Error: Trying to create memory for {scope} {type} but does not exist")
				exit()
		else:
			if (type == "int"):
				return self.create_constant_int(0)
			elif (type == "float"):
				return self.create_constant_float(0.0)
			elif (type == "char"):
				return self.create_constant_char(0)
			elif (type == "bool"):
				return self.create_constant_bool(False)
			else:
				print(f"Error: Trying to create memory for {scope} {type} but does not exist")
				exit()
	
	def reset_resources(self):
		ints = self.resourceInt
		floats = self.resourceFloat
		bools = self.resourceBool
		chars = self.resourceChar

		self.resourceInt = 0
		self.resourceFloat = 0
		self.resourceChar = 0
		self.resourceBool = 0

		return ints, floats, chars, bools
	
	# Checks if address exists in memory
	def check_address(self, address):
		if (address in self.memory):
			return True
		else:
			return False
	
	# Gets the value at address
	def get_value(self, address):
		if self.check_address(address):
			if (self.get_type(address) == "bool"):
				if self.memory[address] == 0:
					return False
				else:
					return True
			return self.memory[address]
		else:
			print(f"Error: Trying to get address {address} but does not exist")
			exit()
	
	# Sets the value at address
	def set_value(self, address, value):
		if self.check_address(address):
			# Fix char 
			# print(f"Setting {address} to {value}")
			if (self.get_type(address) == "char"):
				# for i in value:
				# 	print(ascii(i), end=" ")
				# print(value)
				if (type(value) == str):
					if (len(value) == 1):
						value = ord(value)
					elif (len(value) == 2):
						if (value == "\\a"):
							value = 7
						elif (value == "\\b"):
							value = 8
						elif (value == "\\t"):
							value = 9
						elif (value == "\\n"):
							value = 10
						elif (value == "\\v"):
							value = 11
						elif (value == "\\f"):
							value = 12
						elif (value == "\\r"):
							value = 13
						elif (value == "\\e"):
							value = 27
						elif (value == "\\\""):
							value = 34
						elif (value == "\\\'"):
							value = 39
						elif (value == "\\?"):
							value = 63
						elif (value == "\\\\"):
							value = 92
						else:
							print(f"Error: Invalid escape character sequence {value}")
							exit()
					else:
						print("Error: Invalid char")
						exit()
				elif (type(value) == bool):
					if (value or value != 0):
						value = 1
					else:
						value = 0
				# value %= 128
			self.memory[address] = value
		else:
			print(f"Error: Trying to set address {address} but does not exist")
			exit()
	
	def get_type(self, address):
		if (address >= self.global_int_start and address < self.global_float_start or address >= self.local_int_start and address < self.local_float_start or address >= self.constant_int_start and address < self.constant_float_start):
			return "int"
		elif (address >= self.global_float_start and address < self.global_char_start or address >= self.local_float_start and address < self.local_char_start or address >= self.constant_float_start and address < self.constant_char_start):
			return "float"
		elif (address >= self.global_char_start and address < self.global_bool_start or address >= self.local_char_start and address < self.local_bool_start or address >= self.constant_char_start and address < self.constant_bool_start):
			return "char"
		elif (address >= self.global_bool_start and address <= self.max_global_bool or address >= self.local_bool_start and address <= self.max_local_bool or address >= self.constant_bool_start and address <= self.max_constant_bool):
			return "bool"
		else:
			print(f"Error: Trying to get type of address {address} but is out of bounds")
			exit()
	
	def get_scope(self, address):
		if (address >= self.global_int_start and address <= self.max_global_bool):
			return 0
		elif (address >= self.local_int_start and address <= self.max_local_bool):
			return 1
		elif (address >= self.constant_int_start and address <= self.max_constant_bool):
			return -1
		else:
			print(f"Error: Trying to get scope of address {address} but is out of bounds")
			exit()
	
	# Pop variables that are no longer used
	def pop_global_int(self):
		if (self.g_i_counter > self.global_int_start):
			self.g_i_counter -= 1
			return self.memory.pop(self.g_i_counter, -1)
	
	def pop_global_float(self):
		if (self.g_f_counter > self.global_float_start):
			self.g_f_counter -= 1
			return self.memory.pop(self.g_f_counter, -1)
	
	def pop_global_char(self):
		if (self.g_c_counter > self.global_char_start):
			self.g_c_counter -= 1
			return self.memory.pop(self.g_c_counter, -1)
	
	def pop_global_bool(self):
		if (self.g_b_counter > self.global_bool_start):
			self.g_b_counter -= 1
			return self.memory.pop(self.g_b_counter, -1)
	
	def pop_local_int(self):
		if (self.l_i_counter > self.local_int_start):
			self.l_i_counter -= 1
			return self.memory.pop(self.l_i_counter, -1)
	
	def pop_local_float(self):
		if (self.l_f_counter > self.local_float_start):
			self.l_f_counter -= 1
			return self.memory.pop(self.l_f_counter, -1)
	
	def pop_local_char(self):
		if (self.l_c_counter > self.local_char_start):
			self.l_c_counter -= 1
			return self.memory.pop(self.l_c_counter, -1)
	
	def pop_local_bool(self):
		if (self.l_b_counter > self.local_bool_start):
			self.l_b_counter -= 1
			return self.memory.pop(self.l_b_counter, -1)
	
	def pop_constant_int(self):
		if (self.c_i_counter > self.constant_int_start):
			self.c_i_counter -= 1
			return self.memory.pop(self.c_i_counter, -1)
	
	def pop_constant_float(self):
		if (self.c_f_counter > self.constant_float_start):
			self.c_f_counter -= 1
			return self.memory.pop(self.c_f_counter, -1)
	
	def pop_constant_char(self):
		if (self.c_c_counter > self.constant_char_start):
			self.c_c_counter -= 1
			return self.memory.pop(self.c_c_counter, -1)

	def pop_constant_bool(self):
		if (self.c_b_counter > self.constant_bool_start):
			self.c_b_counter -= 1
			return self.memory.pop(self.c_b_counter, -1)
	
	# To speed up deleting unused memory
	def pop_memory(self, scope, type, n=1):
		res = 0
		if scope == "global":
			if type == "int":
				for i in range(n):
					res = self.pop_global_int()
			elif type == "float":
				for i in range(n):
					res = self.pop_global_float()
			elif type == "char":
				for i in range(n):
					res = self.pop_global_char()
			elif type == "bool":
				for i in range(n):
					res = self.pop_global_bool()

		elif scope == "local":
			if type == "int":
				for i in range(n):
					res = self.pop_local_int()
			elif type == "float":
				for i in range(n):
					res = self.pop_local_float()
			elif type == "char":
				for i in range(n):
					res = self.pop_local_char()
			elif type == "bool":
				for i in range(n):
					res = self.pop_local_bool()
		
		elif scope == "constant":
			if type == "int":
				for i in range(n):
					res = self.pop_constant_int()
			elif type == "float":
				for i in range(n):
					res = self.pop_constant_float()
			elif type == "char":
				for i in range(n):
					res = self.pop_constant_char()
			elif type == "bool":
				for i in range(n):
					res = self.pop_constant_bool()
		# if (res == -1):
		# 	print(f"Error: Trying to pop {scope} {type} {self.} but there are none")
		# 	exit()
	
	# Deletes the whole memory
	def pop_all(self):
		self.memory.clear()
		
		self.g_i_counter = self.global_int_start
		self.g_f_counter = self.global_float_start
		self.g_c_counter = self.global_char_start
		self.g_b_counter = self.global_bool_start

		self.l_i_counter = self.local_int_start
		self.l_f_counter = self.local_float_start
		self.l_c_counter = self.local_char_start
		self.l_b_counter = self.local_bool_start

		self.c_i_counter = self.constant_int_start
		self.c_f_counter = self.constant_float_start
		self.c_c_counter = self.constant_char_start
		self.c_b_counter = self.constant_bool_start
	
	def print(self):
		print(json.dumps(self.memory, indent=4, sort_keys=True))
		# print(self.memory)