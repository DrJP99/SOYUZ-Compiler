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

		self.g_i_counter = self.global_int_start
		self.g_f_counter = self.global_float_start
		self.g_c_counter = self.global_char_start
		self.g_b_counter = self.global_bool_start

		self.l_i_counter = self.local_int_start
		self.l_f_counter = self.local_float_start
		self.l_c_counter = self.local_char_start
		self.l_b_counter = self.local_bool_start

		self.memory = {}
	
	# Creates virtual memory address for declared variables
	def create_global_int(self):
		if (self.g_i_counter <= self.max_global_int):
			self.memory[self.g_i_counter] = 0
			self.g_i_counter += 1
			return self.g_i_counter - 1
		else:
			print("Error: no more global int memory available")
			exit()

	def create_global_float(self):
		if (self.g_f_counter <= self.max_global_float):
			self.memory[self.g_f_counter] = 0.0
			self.g_f_counter += 1
			return self.g_f_counter - 1
		else:
			print("Error: no more global float memory available")
			exit()
	
	def create_global_char(self):
		if (self.g_c_counter <= self.max_global_char):
			self.memory[self.g_c_counter] = 0
			self.g_c_counter += 1
			return self.g_c_counter - 1
		else:
			print("Error: no more global char memory available")
			exit()
	
	def create_global_bool(self):
		if (self.g_b_counter <= self.max_global_bool):
			self.memory[self.g_b_counter] = False
			self.g_b_counter += 1
			return self.g_b_counter - 1
		else:
			print("Error: no more global bool memory available")
			exit()

	def create_local_int(self):
		if (self.l_i_counter <= self.max_local_int):
			self.memory[self.l_i_counter] = 0
			self.l_i_counter += 1
			return self.l_i_counter - 1
		else:
			print("Error: no more local int memory available")
			exit()
	
	def create_local_float(self):
		if (self.l_f_counter <= self.max_local_float):
			self.memory[self.l_f_counter] = 0.0
			self.l_f_counter += 1
			return self.l_f_counter - 1
		else:
			print("Error: no more local float memory available")
			exit()
	
	def create_local_char(self):
		if (self.l_c_counter <= self.max_local_char):
			self.memory[self.l_c_counter] = 0
			self.l_c_counter += 1
			return self.l_c_counter - 1
		else:
			print("Error: no more local char memory available")
			exit()
	
	def create_local_bool(self):
		if (self.l_b_counter <= self.max_local_bool):
			self.memory[self.l_b_counter] = False
			self.l_b_counter += 1
			return self.l_b_counter - 1
		else:
			print("Error: no more local bool memory available")
			exit()
	
	def create_memory(self, scope, type):
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
							print(f"ERROR: Invalid escape character sequence {value}")
							exit()
					else:
						print("ERROR: Invalid char")
						exit()
				elif (type(value) == bool):
					if (value or value != 0):
						value = 1
					else:
						value = 0
			value %= 128
			self.memory[address] = value
		else:
			print(f"Error: Trying to set address {address} but does not exist")
			exit()
	
	def get_type(self, address):
		if (address >= self.global_int_start and address < self.global_float_start or address >= self.local_int_start and address < self.local_float_start):
			return "int"
		elif (address >= self.global_float_start and address < self.global_char_start or address >= self.local_float_start and address < self.local_char_start):
			return "float"
		elif (address >= self.global_char_start and address < self.global_bool_start or address >= self.local_char_start and address < self.local_bool_start):
			return "char"
		elif (address >= self.global_bool_start and address <= self.max_global_bool or address >= self.local_bool_start and address <= self.max_local_bool):
			return "bool"
		else:
			print(f"Error: Trying to get type of address {address} but is out of bounds")
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
	
	# To speed up deleting unused memory
	def pop_memory(self, scope, type, n=1):
		if scope == "global":
			if type == "int":
				for i in range(n):
					self.pop_global_int()
			elif type == "float":
				for i in range(n):
					self.pop_global_float()
			elif type == "char":
				for i in range(n):
					self.pop_global_char()
			elif type == "bool":
				for i in range(n):
					self.pop_global_bool()

		elif scope == "local":
			if type == "int":
				for i in range(n):
					self.pop_local_int()
			elif type == "float":
				for i in range(n):
					self.pop_local_float()
			elif type == "char":
				for i in range(n):
					self.pop_local_char()
			elif type == "bool":
				for i in range(n):
					self.pop_local_bool()
	
	def print(self):
		print(json.dumps(self.memory, indent=4, sort_keys=False))
		# print(self.memory)