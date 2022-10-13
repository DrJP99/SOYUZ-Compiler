
# Deals with all the functions related to the functions/variables tables
class DirFunc:
	def __init__(self):
		# Creates the dict for the global scope
		self.table = {
			0: {
				"name": "global", "returnType": "int", "vars": {}
			}
		}

	# TODO see if function exists
	# TODO Maybe create a different list for declared funcs that will not get popped to see if they exist and so on

	# Creates a new function on the dictionary using the directory of the nth scope
	def addFunction(self, scope, name, returnT):
		self.table[scope] = {}
		self.table[scope]["name"] = name
		self.table[scope]["returnType"] = returnT
		self.table[scope]["params"] = {}
		self.table[scope]["vars"] = {}
	

	# Removes a function directory from the table, this will be used at the end of a function when it will no longer be used
	def removeFunction(self, scope):
		return self.table.pop(scope)
	

	# Returns the current scope's function's return type
	def getReturnType(self, scope):
		return self.table[scope]["returnType"]
	

	# Adds Param to list of function's parameters and adds those variables to list of variables
	def addParam(self, scope, newVar):
		varName = list(newVar.keys())[0]
		varType = newVar[varName]["type"]
		if (self.findParam(scope, varName)):
			print("Error: Param is already declared")
		else:
			param = {varName: {"type": varType}}
			self.table[scope]["params"].update(param)
			self.addVar(scope, newVar)
			

	# Check if a param has already been declared
	def findParam(self, scope, varName):
		return varName in self.table[scope]["params"]


	# Adds a variable to the scope's list of variables
	def addVar(self, scope, newVar):
		varName = list(newVar.keys())[0]	# Get the head of newVar, as that is the name of that variable
		if (self.findVar(scope, varName) == scope):
			# If the variable is found in the current scope, an error is thrown as it is already declared
			print("Error: variable ", varName, " is already declared in current scope ", scope)
			exit()
		else:
			# If the variable is NOT found in the current scope or is found in the global scope (if the current scope is not the global), the variable is stored
			self.table[scope]["vars"].update(newVar)
	

	# Return type of variables from the table
	def getVarType(self, scope, name):
		newScope = self.findVar(scope, name)
		if (newScope == -1):
			print("ERROR: ", name, " has not been declared in this scope")

		else:
			return self.table[newScope]["vars"][name]["type"]
	

	# Returns the value for variables of 0 dimensions
	def getVarValue(self, scope, name):
		newScope = self.findVar(scope, name)
		if (newScope == -1):
			print(name, " has not been declared in this scope")
		else:
			if (self.table[newScope]["vars"][name]["dims"] == 0):
				return self.table[newScope]["vars"][name]["value"]
			else:
				print("Variable has ", self.table[newScope]["vars"][name]["dims"], " dimensions")
				# TODO: impelemnt a function to deal with lists and matrixes
	
	# Set the value for variables of 0 dimensions
	def setVarValue(self, scope, name, value):
		newScope = self.findVar(scope, name)
		if (newScope == -1):
			print(name, " has not been declared in this scope")
		else:
			if (self.table[newScope]["vars"][name]["dims"] == 0):
				self.table[newScope]["vars"][name]["value"] = value
			else:
				print("Variable has ", self.table[newScope]["vars"][name]["dims"], " dimensions")
				# TODO: impelemnt a function to deal with lists and matrixes


	# Sees if a variable exists or not
	def findVar(self, scope, name):
		if (name in self.table[scope]["vars"]):
			# Look for variable in the current scope, return the current scope if it is found, else:
			return scope
		else:
			if (name in self.table[0]["vars"]):
				# If the variable was not found in the current scope, look for it in the global scope, returns 0 if it is found
				return 0
			else:
				# Return -1 if it's NOT found in the current scope or the global scope
				return -1


	def printFunc(self):
		print(self.table)



class varAttributes:
	def __init__(self):
		self.atts = {}
	
	def createVar(self, name, type, dims, value):
		self.atts = {name: {"type": type, "dims": dims, "value": value}}
		return self.atts

