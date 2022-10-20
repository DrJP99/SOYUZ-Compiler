'''
global variables: (0 - 1499)
	int			: (0 - 499)
	float		: (500 - 999)
	char		: (1000 - 1499)

local variables	: (1500 - 4999)		# includes temporary variables
	int			: (1500 - 2499)
	float		: (2500 - 3499)
	char		: (3500 - 4499)
'''
# CHAR is stored as INTs, min = 0, max = 127

class VirtualMemory:
	def __init__(self):
		self.global_int_start = 0
		self.global_float_start = 500
		self.global_char_start = 1000
		
		self.max_global_int = 499
		self.max_global_float = 999
		self.max_global_char = 1499

		self.local_int_start = 1500
		self.local_float_start = 2500
		self.local_char_start = 3500

		self.max_local_int = 2499
		self.max_local_float = 3499
		self.max_local_char = 4499

		self.g_i_counter = self.global_int_start
		self.g_f_counter = self.global_float_start
		self.g_c_counter = self.global_char_start

		self.l_i_counter = self.local_int_start
		self.l_f_counter = self.local_float_start
		self.l_c_counter = self.local_char_start

		self.memory = {}
	
	# Creates virtual memory direction for declared variables
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
	
	def create_memory(self, scope, type):
		if (scope == 0):
			if (type == "int"):
				return self.create_global_int()
			elif (type == "float"):
				return self.create_global_float()
			elif (type == "char"):
				return self.create_global_char()
		elif (scope > 1):
			if (type == "int"):
				return self.create_local_int()
			elif (type == "float"):
				return self.create_local_float()
			elif (type == "char"):
				return self.create_local_char()
		else:
			print(f"Error: Trying to create memory for {scope} {type} but does not exist")
			exit()
	
	# Checks if direction exists in memory
	def check_direction(self, direction):
		if (direction in self.memory):
			return True
		else:
			return False
	
	# Gets the value at direction
	def get_value(self, direction):
		if self.check_direction(direction):
			return self.memory[direction]
		else:
			print(f"Error: Trying to get direction {direction} but does not exist")
			exit()
	
	# Sets the value at direction
	def set_value(self, direction, value):
		if self.check_direction(direction):
			if ((direction >= self.global_char_start and direction <= self.max_global_char) or (direction >= self.local_char_start and direction <= self.max_local_char)):
				value %= 128
			self.memory[direction] = value
		else:
			print(f"Error: Trying to set direction {direction} but does not exist")
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