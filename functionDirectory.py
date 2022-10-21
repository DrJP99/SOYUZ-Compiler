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
	def get_return_type(self, name):
		return self.table[name]["returnType"]
	

	# Adds Param to list of function's parameters and adds those variables to list of variables
	def add_param(self, scope, newVar):
		name = self.vars[scope]["function"]

		varName = list(newVar.keys())[0]
		varType = newVar[varName]["type"]
		if (self.find_var(scope, varName)):
			print("Error: Param is already declared")
		else:
			param = varType
			self.table[name]["params"].append(param)
			self.add_var(scope, newVar)
			
			

	# Check if a param has already been declared
	def find_param(self, scope, varName):
		return varName in self.table[scope]["params"]


	# Adds a variable to the scope's list of variables
	def add_var(self, scope, newVar):
		varName = list(newVar.keys())[0]	# Get the head of newVar, as that is the name of that variable
		if (self.find_var(scope, varName) == scope):
			# If the variable is found in the current scope, an error is thrown as it is already declared
			print("Error: variable ", varName, " is already declared in current scope ", scope)
			exit()
		else:
			# If the variable is NOT found in the current scope or is found in the global scope (if the current scope is not the global), the variable is stored
			address = self.memory.create_memory(scope, newVar[varName]["type"])
			newVar[varName]["address"] = address
			self.vars[scope]["vars"].update(newVar)
			self.add_resource(scope, newVar[varName]["type"])
	

	# Return type of variables from the table
	def get_var_type(self, scope, name):
		newScope = self.find_var(scope, name)
		if (newScope == -1):
			print("ERROR: ", name, " has not been declared in this scope")

		else:
			return self.vars[newScope]["vars"][name]["type"]
	

	# Returns the value for variables of 0 dimensions
	def get_var_value(self, scope, name):
		newScope = self.find_var(scope, name)
		if (newScope == -1):
			print(name, " has not been declared in this scope")
		else:
			if (self.vars[newScope]["vars"][name]["dims"] == 0):
				address = self.vars[newScope]["vars"][name]["address"]
				return self.memory.get_value(address)
			else:
				print("Variable has ", self.vars[newScope]["vars"][name]["dims"], " dimensions")
				# TODO: impelemnt a function to deal with lists and matrixes
	
	# Set the value for variables of 0 dimensions
	def set_var_value(self, scope, name, value):
		newScope = self.find_var(scope, name)
		if (newScope == -1):
			print(name, " has not been declared in this scope")
		else:
			if (self.vars[newScope]["vars"][name]["dims"] == 0):
				address = self.vars[newScope]["vars"][name]["address"]
				self.memory.set_value(address, value)
			else:
				print("Variable has ", self.vars[newScope]["vars"][name]["dims"], " dimensions")
				# TODO: impelemnt a function to deal with lists and matrixes

	def set_value_at_address(self, address, value):
		self.memory.set_value(address, value)

	def get_var_address(self, scope, name):
		newScope = self.find_var(scope, name)
		if (newScope == -1):
			print(name, " has not been declared in this scope")
		else:
			if (self.vars[newScope]["vars"][name]["dims"] == 0):
				return self.vars[newScope]["vars"][name]["address"]
			else:
				print("Variable has ", self.vars[newScope]["vars"][name]["dims"], " dimensions")
				# TODO: impelemnt a function to deal with lists and matrixes

	def add_resource(self, scope, type):
		name = self.vars[scope]["function"]
		self.table[name]["resources"][type] += 1
	
	def add_resources(self, scope, ints, floats, chars, bools):
		name = self.vars[scope]["function"]

		self.table[name]["resources"]["int"] += ints
		self.table[name]["resources"]["float"] += floats
		self.table[name]["resources"]["char"] += chars
		self.table[name]["resources"]["bool"] += bools

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
	
	def find_function(self, name):
		return name in self.table
	
	def generate_memory(self, scope, type):
		return self.memory.create_memory(scope, type)
	
	def update_init(self, scope, value):
		name = self.vars[scope]["function"]
		self.table[name]["init"] = value


	def print(self):
		print(json.dumps(self.table, indent=4, sort_keys=False))
		print(json.dumps(self.vars, indent=4, sort_keys=False))



class varAttributes:
	def __init__(self):
		self.atts = {}
	
	def create_var(self, name, type, dims):
		self.atts = {name: {"type": type, "dims": dims}}
		return self.atts

	def set_address(self, name, address):
		self.atts[name]["address"] = address
	
	def get_address(self, name):
		return self.atts[name]["address"]

	def get_name(self):
		return list(self.atts.keys())[0]
	
	def get_type(self, name):
		return self.atts[name]["type"]
