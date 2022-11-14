from virtualMemory import *
import json

# Deals with all the functions related to the functions/variables tables
class DirFunc:
	def __init__(self):
		# Creates the dict for the global scope
		self.table = {
			"global": {
				"returnType": "int", "params": [], "resources":
				{"int": 0, "float": 0, "char": 0, "bool": 0}
			}
		}
		self.vars = {0: {
			"function": "global", "vars": {}
		}}
		# Use Virtual Memory inside the function directory to make things easier
		self.memory = VirtualMemory()

	# TODO see if function exists

	# Creates a new function on the dictionary using the directory of the nth scope
	def addFunction(self, scope, name, returnT):
		if (self.find_function(name)):
			print("Error: function ", name, " is already declared")
			exit()
		else:
			res = {"int": 0, "float": 0, "char": 0, "bool": 0}
			# self.table[scope] = {}
			self.table[name] = {}
			self.table[name]["returnType"] = returnT
			self.table[name]["params"] = []
			self.table[name]["resources"] = res
			self.table[name]["init"] = 0


			self.vars[scope] = {}
			self.vars[scope]["function"] = name
			
			self.vars[scope]["vars"] = {}

	# Removes a function directory from the table, this will be used at the end of a function when it will no longer be used
	def remove_function(self, scope):
		return self.vars.pop(scope)
	

	# Returns the current scope's function's return type
	def get_return_type(self, scope):
		return self.table[self.vars[scope]["function"]]["returnType"]
	
	def get_return_type_name(self, name):
		return self.table[name]["returnType"]
	
	def get_func_name(self, scope):
		return self.vars[scope]["function"]
	

	# Adds Param to list of function's parameters and adds those variables to list of variables
	def add_param(self, scope, newVar):
		name = self.vars[scope]["function"]

		varName = list(newVar.keys())[0]
		varType = newVar[varName]["type"]
		if (self.find_var(scope, varName) == scope):
			print(f"Error: Param {varName} is already declared")
			exit()
		else:
			param = varType
			self.table[name]["params"].append(param)
			self.add_var(scope, newVar)
			
			

	# Check if a param has already been declared
	def find_param(self, scope, varName):
		return varName in self.table[scope]["params"]

	def get_params(self, name):
		return self.table[name]["params"]

	# Adds a variable to the scope's list of variables
	def add_var(self, scope, newVar):
		varName = list(newVar.keys())[0]	# Get the head of newVar, as that is the name of that variable
		if (self.find_var(scope, varName) == scope):
			# If the variable is found in the current scope, an error is thrown as it is already declared
			print("Error: variable ", varName, " is already declared in current scope ", scope)
			exit()
		else:
			# If the variable is NOT found in the current scope or is found in the global scope (if the current scope is not the global), the variable is stored
			dims = newVar[varName]["dims"]
			xDim = newVar[varName]["xDim"]
			yDim = newVar[varName]["yDim"]
			varType = newVar[varName]["type"]

			size = 0;
			if (dims == 0):
				size = 1
			elif (dims == 1):
				size = xDim
			elif (dims == 2):
				size = xDim * yDim

			address = self.memory.create_many_memory(scope, varType, size)
			newVar[varName]["address"] = address
			self.vars[scope]["vars"].update(newVar)

			ints = floats = bools = chars = 0

			if (varType == 'int'):
				ints = size
			elif (varType == 'float'):
				floats = size
			elif (varType == 'char'):
				chars = size
			elif (varType == 'bool'):
				bools = size
			
			# self.add_resources(scope, ints, floats, chars, bools)
	

	# Return type of variables from the table
	def get_var_type(self, scope, name):
		newScope = self.find_var(scope, name)
		if (newScope == -1):
			print("ERROR: ", name, " has not been declared in this scope")
			exit()
		else:
			return self.vars[newScope]["vars"][name]["type"]
	
	# Get offset of address for vars with dims
	def dim_offset(self, dims, xDim ,yDim, xSize):
		if (dims == 0):
			return 0
		elif (dims == 1):
			return xDim
		elif (dims == 2):
			return (xSize * yDim) + xDim
	
	# Returns the value for variables of 0 dimensions
	def get_var_value(self, scope, name):
		newScope = self.find_var(scope, name)
		if (newScope == -1):
			print("ERROR: ", name, " has not been declared in this scope")
			exit()
		else:
			offset = self.dim_offset(self.vars[newScope]["vars"][name]["dims"], self.vars[newScope]["vars"][name]["xDim"], self.vars[newScope]["vars"][name]["yDim"], self.vars[newScope]["vars"][name]["xSize"])
			address = self.vars[newScope]["vars"][name]["address"]
			return self.memory.get_value(address + offset)
				# print("Variable has ", self.vars[newScope]["vars"][name]["dims"], " dimensions")
	
	# Gets value at address
	def get_value(self, address):
		return self.memory.get_value(address)
	
	# Set the value for variables of 0 dimensions
	def set_var_value(self, scope, name, value, xDim = 0, yDim = 0):
		newScope = self.find_var(scope, name)
		if (newScope == -1):
			print("ERROR: ",name, " has not been declared in this scope")
			exit()
		else:
			offset = self.dim_offset(self.vars[newScope]["vars"][name]["dims"], xDim, yDim, self.vars[newScope]["vars"][name]["xDim"])

			address = self.vars[newScope]["vars"][name]["address"]
			self.memory.set_value(address + offset, value)
			# print("Variable has ", self.vars[newScope]["vars"][name]["dims"], " dimensions")

	def set_value_at_address(self, address, value):
		self.memory.set_value(address, value)

	def get_var_address(self, scope, name):
		newScope = self.find_var(scope, name)
		if (newScope == -1):
			print("ERROR: ", name, " has not been declared in this scope")
			exit()
		else:
			return self.vars[newScope]["vars"][name]["address"]
			# print("Variable has ", self.vars[newScope]["vars"][name]["dims"], " dimensions")

	
	def get_var_xDim(self, scope, name):
		newScope = self.find_var(scope, name)
		if (newScope == -1):
			print("ERROR: ", name, " has not been declared in this scope")
			exit()
		else:
			return self.vars[newScope]["vars"][name]["xDim"]
	
	def get_var_yDim(self, scope, name):
		newScope = self.find_var(scope, name)
		if (newScope == -1):
			print("ERROR: ", name, " has not been declared in this scope")
			exit()
		else:
			return self.vars[newScope]["vars"][name]["yDim"]
	
	def get_var_limits(self, scope, name):
		newScope = self.find_var(scope, name)
		if (newScope == -1):
			print("ERROR: ", name, " has not been declared in this scope")
			exit()
		else:
			limitI = self.vars[newScope]["vars"][name]["address"]
			xDim = self.vars[newScope]["vars"][name]["xDim"]
			yDim = self.vars[newScope]["vars"][name]["yDim"]
			limitS = xDim * yDim
			return limitI, limitS

	def get_var_dims_count(self, scope, name):
		newScope = self.find_var(scope, name)
		if (newScope == -1):
			print("ERROR: ", name, " has not been declared in this scope")
			exit()
		else:
			if (self.vars[newScope]["vars"][name]["xDim"] != None):
				if (self.vars[newScope]["vars"][name]["yDim"] != None):
					return 2
				else:
					return 1
			else:
				return 0
	
	def get_var_dims(self, scope, name):
		newScope = self.find_var(scope, name)
		if (newScope == -1):
			print("ERROR: ", name, " has not been declared in this scope")
			exit()
		else:
			xDim = self.vars[newScope]["vars"][name]["xDim"]
			yDim = self.vars[newScope]["vars"][name]["yDim"]
			return xDim, yDim

	def add_resource(self, scope, type):
		name = self.vars[scope]["function"]
		self.table[name]["resources"][type] += 1
	
	def add_resources(self, scope, ints, floats, chars, bools):
		name = self.vars[scope]["function"]

		self.table[name]["resources"]["int"] += ints
		self.table[name]["resources"]["float"] += floats
		self.table[name]["resources"]["char"] += chars
		self.table[name]["resources"]["bool"] += bools
	
	def get_resources(self, name):
		i = self.table[name]["resources"]["int"]
		f = self.table[name]["resources"]["float"]
		c = self.table[name]["resources"]["char"]
		b = self.table[name]["resources"]["bool"]
		return i, f, c, b
	
	def set_var_dims(self, scope, name, dims):
		newScope = self.find_var(scope, name)
		if (newScope == -1):
			print("ERROR: ", name, " has not been declared in this scope")
			exit()
		else:
			self.vars[newScope]["vars"][name]["dims"] = dims
	
	def set_var_xDim(self, scope, name, xDim):
		newScope = self.find_var(scope, name)
		if (newScope == -1):
			print("ERROR: ", name, " has not been declared in this scope")
			exit()
		else:
			self.vars[newScope]["vars"][name]["xDim"] = xDim
	
	def set_var_yDim(self, scope, name, yDim):
		newScope = self.find_var(scope, name)
		if (newScope == -1):
			print("ERROR: ", name, " has not been declared in this scope")
			exit()
		else:
			self.vars[newScope]["vars"][name]["yDim"] = yDim

	# Sees if a variable exists or not
	def find_var(self, scope, name):
		if (name in self.vars[scope]["vars"]):
			# Look for variable in the current scope, return the current scope if it is found, else:
			return scope
		else:
			if (name in self.vars[0]["vars"]):
				# If the variable was not found in the current scope, look for it in the global scope, returns 0 if it is found
				return 0
			else:
				# Return -1 if it's NOT found in the current scope or the global scope
				return -1
		
	def fill_resources(self, scope, wipe=False):
		i, f, c, b= self.memory.reset_resources()
		self.add_resources(scope, i, f, c, b)

		if (wipe):
			self.memory.pop_memory("local", "int", i)
			self.memory.pop_memory("local", "float", f)
			self.memory.pop_memory("local", "char", c)
			self.memory.pop_memory("local", "bool", b)

	
	def find_function(self, name):
		return name in self.table
	
	def generate_memory(self, scope, type, const=False):
		return self.memory.create_memory(scope, type, const)
	
	def update_init(self, scope, value):
		name = self.vars[scope]["function"]
		self.table[name]["init"] = value
	
	def get_init(self, name):
		return self.table[name]["init"]

	def print_memory(self):
		self.memory.print()

	def print(self):
		print(json.dumps(self.table, indent=4, sort_keys=False))
		print(json.dumps(self.vars, indent=4, sort_keys=False))



class varAttributes:
	def __init__(self):
		self.atts = {}
	
	def create_var(self, name, type, dims, xDim = None, yDim = None):
		self.atts = {name: {"type": type, "dims": dims, "xDim": xDim, "yDim": yDim}}
		return self.atts

	def set_address(self, name, address):
		self.atts[name]["address"] = address
	
	def get_address(self, name):
		return self.atts[name]["address"]

	def get_name(self):
		return list(self.atts.keys())[0]
	
	def get_type(self, name):
		return self.atts[name]["type"]
