import pickle
from pstats import Stats
import string
import virtualMemory

import statistics
from matplotlib import pyplot as plt
import numpy as np
from scipy import stats

class VirtualMachine:
	def __init__(self, memory, quads, df):
		self.memory = memory
		self.quads = quads
		self.df = df

	def start_machine(self):
		ip = 0			# instruction pointer
		checkpoint = []	# checkpoint stack
		ERAi = []		# ERA int stack
		ERAf = []		# ERA float stack
		ERAc = []		# ERA char stack
		ERAb = []		# ERA bool stack

		res = 0 		# Saves the result of a FUNC call

		self.offsetint = 0
		self.offsetfloat = 0
		self.offsetchar = 0
		self.offsetbool = 0

		ERAi.append(df["main"]["resources"]["int"])
		ERAf.append(df["main"]["resources"]["float"])
		ERAc.append(df["main"]["resources"]["char"])
		ERAb.append(df["main"]["resources"]["bool"])

		countint = 0
		countfloat = 0
		countchar = 0
		countbool = 0

		print("> ", end="")
		while (True):
			
			quad = self.quads[ip]

			# print(f'curr ip: #{ip}', end=" ")
			# quad.print()

			operator, opLeft, opRight, result = self.parse_quad(quad)
			### SWITCH ###
			### ARYTHMETICS ###
			if (operator == "="):
				value = opLeft
				if (memory.get_type(opLeft) == "int" and memory.get_type(result) == "float"):
					value = float(value)
				elif (memory.get_type(opLeft) == "float" and memory.get_type(result) == "int"):
					value = int(value)
				
				if (memory.get_type(result) == "bool"):
					if (value > 0):
						value = 1
					else:
						value = 0
					
				self.memory.set_value(result, value)
				# self.memory.set_value(result, opLeft)
				
			elif (operator == "+"):
				value = opLeft + opRight
				self.memory.set_value(result, value)
				# self.memory.set_value(result, opLeft + opRight)
				
			elif (operator == "-"):
				value = opLeft - opRight
				self.memory.set_value(result, value)
				# self.memory.set_value(result, opLeft - opRight)
				
			elif (operator == "*"):
				value = opLeft * opRight
				self.memory.set_value(result, value)
				# self.memory.set_value(result, opLeft * opRight)
				
			elif (operator == "/"):
				value = float(opLeft) / float(opRight)
				self.memory.set_value(result, value)
				# self.memory.set_value(result, opLeft / opRight)
			
			# Used to sum the base value for an array
			elif (operator == "BSUM"):
				value = opLeft + opRight
				# print(f'BSUM: {value}, storing in {result}')
				self.memory.set_value(result, value)
			
			# Verifies if the index is within the array bounds
			elif (operator == "VER"):
				if (opLeft < 0 or opLeft > result):
					print(f'Error: Index out of bounds: {opLeft}')
					exit()

			### RELATIONAL ###
			elif (operator == "=="):
				if (opLeft == opRight):
					self.memory.set_value(result, 1)
				else:
					self.memory.set_value(result, 0)
			elif (operator == "!="):
				if (opLeft != opRight):
					self.memory.set_value(result, 1)
				else:
					self.memory.set_value(result, 0)
			elif (operator == ">"):
				if (opLeft > opRight):
					self.memory.set_value(result, 1)
				else:
					self.memory.set_value(result, 0)
			elif (operator == ">="):
				if (opLeft >= opRight):
					self.memory.set_value(result, 1)
				else:
					self.memory.set_value(result, 0)
			elif (operator == "<"):
				if (opLeft < opRight):
					self.memory.set_value(result, 1)
				else:
					self.memory.set_value(result, 0)
			elif (operator == "<="):
				if (opLeft <= opRight):
					self.memory.set_value(result, 1)
				else:
					self.memory.set_value(result, 0)
			elif (operator == "&&"):
				if (opLeft and opRight):
					self.memory.set_value(result, 1)
				else:
					self.memory.set_value(result, 0)
			elif (operator == "||"):
				if (opLeft or opRight):
					self.memory.set_value(result, 1)
				else:
					self.memory.set_value(result, 0)

			### JUMPS ###
			elif (operator == "GOTO"):
				ip = opRight - 1
			elif (operator == "GOTOF"):
				if (not opLeft):
					ip = opRight - 1

			### READ / WRITE ###
			elif (operator == "READ"):
				value = input()
				myType = self.memory.get_type(result)
				if (myType == "int"):
					value = int(value)
				elif (myType == "float"):
					value = float(value)
				elif (myType == "char"):
					value = value
				elif (myType == "bool"):
					if (int(value) > 0 or value == "True"):
						value = 1
					elif (int(value) == 0 or value == "False"):
						value = 0
					else:
						print(f'Error: Invalid value for type bool')
						exit()
				
				self.memory.set_value(result, value)
				print("> ", end="")

			elif (operator == "WRITE"):
				i = 0
				size = opRight
				# print(f"Trying to write {size} values from {opLeft}")
				if (type(quad.get_left_operand()) == str):
					if (quad.get_left_operand()[0] == "$"):
						opLeft = int(quad.get_left_operand().replace("$", ""))
						opLeft = self.memory.get_value(opLeft)
					elif (quad.get_left_operand()[0] == "*"):
						opLeft = int(quad.get_left_operand().replace("*", ""))
				else:
					opLeft = quad.get_left_operand()

				while(i < size):
					offset = i + self.get_offset(opLeft)
					value = memory.get_value(opLeft + offset)

					if (self.memory.get_type(opLeft + offset) == "char"):
						value = chr(value)
					elif (self.memory.get_type(opLeft + offset) == "float"):
						value = round(float(value), 4)

					if (value == "\n"):
						print("\n> ", end = "")
					else:
						print(value, end = "")

					i += 1
			

			### FUNCTIONS ###

			elif (operator == "ERAI"):
				memory.create_many_memory(1, "int", opLeft)
				self.offsetint += ERAi[-1]
				ERAi.append(opLeft)
			
			elif (operator == "ERAF"):
				memory.create_many_memory(1, "float", opLeft)
				self.offsetfloat += ERAf[-1]
				ERAf.append(opLeft)

			elif (operator == "ERAC"):
				memory.create_many_memory(1, "char", opLeft)
				self.offsetchar += ERAc[-1]
				ERAc.append(opLeft)
			
			elif (operator == "ERAB"):
				memory.create_many_memory(1, "bool", opLeft)
				self.offsetbool += ERAb[-1]
				ERAb.append(opLeft)
			
			elif (operator == "PARAM"):
				paramType = self.memory.get_type(opLeft)
				newoff = 0
				oldoff = 0
				start = 0

				if (paramType == "int"):
					newoff = self.offsetint + countint
					oldoff = self.offsetint - ERAi[-2]
					start = memory.local_int_start
					# print(f"PARAM int {opLeft} {newoff} {oldoff} {start}")
					countint += 1
				elif (paramType == "float"):
					newoff = self.offsetfloat + countfloat
					oldoff = self.offsetfloat - ERAf[-2]
					start = memory.local_float_start
					countfloat += 1
				elif (paramType == "char"):
					newoff = self.offsetchar - ERAc[-2] + countchar
					oldoff = self.offsetchar - ERAc[-2]
					start = memory.local_char_start
					countchar += 1
				elif (paramType == "bool"):
					newoff = self.offsetbool - ERAb[-2] + countbool
					oldoff = self.offsetbool - ERAb[-2]
					start = memory.local_bool_start
					countbool += 1
				
				# print (f"VALUE: {opLeft} @ {quad.get_left_operand()}; TYPE: {paramType};  {newoff} {oldoff} {start}")
				# print(f"Trying to get value at {opLeft + oldoff}...")
				value = self.memory.get_value(opLeft + oldoff)
				# print(f"Got value {value} at {opLeft + oldoff}")
				# print(f"Trying to set value {value} at {start + newoff}...")
				memory.set_value(newoff + start, value)
				# print(f"Set value {value} at {start + newoff}...")

			elif (operator == "GOSUB"):
				checkpoint.append(ip)
				ip = opRight - 1

				countint = 0
				countfloat = 0
				countchar = 0
				countbool = 0

			elif (operator == "RETURN"):
				# print (opLeft)
				res = opLeft

			elif (operator == "ENDFUNC"):
				ip = checkpoint.pop()
				ei = ERAi.pop()
				ef = ERAf.pop()
				ec = ERAc.pop()
				eb = ERAb.pop()

				memory.pop_memory("local", "int", ei)
				memory.pop_memory("local", "float", ef)
				memory.pop_memory("local", "char", ec)
				memory.pop_memory("local", "bool", eb)

				self.offsetint -= ERAi[-1]
				self.offsetfloat -= ERAf[-1]
				self.offsetchar -= ERAc[-1]
				self.offsetbool -= ERAb[-1]

				gosquad = self.quads[ip]
				operator, opLeft, opRight, result = self.parse_quad(gosquad)
				# print (f"Returning to {operator} {opLeft} {opRight} {result}")
				if (result != None):
					# print(res)
					self.memory.set_value(result, res)
			
			### STATISTIC STUFFS ###

			elif (operator == "HIST"):

				if (memory.get_type(result) == "int"):
					bins = memory.get_value(result)
					values = [opRight]
					
					for i in range(opRight):
						values.append(self.memory.get_value(opLeft + i))
					plt.hist(np.array(values), bins=bins, align='mid',
					         color='yellow', edgecolor='black', linewidth=2)
					plt.show()
				else:
					print("ERROR: HISTOGRAM BINS MUST BE AN INTEGER")
					exit()

			elif (operator == "MEAN"):
				values = [opRight]

				for i in range(opRight):
					values.append(float(self.memory.get_value(opLeft + i)))

				mean = np.mean(np.array(values))
				self.memory.set_value(result, mean)
			
			elif (operator == "MEDIAN"):
				values = [opRight]

				for i in range(opRight):
					values.append(float(self.memory.get_value(opLeft + i)))
				
				median = np.median(np.array(values))
				self.memory.set_value(result, median)
			
			elif (operator == "MODE"):
				values = [opRight]

				for i in range(opRight):
					values.append(float(self.memory.get_value(opLeft + i)))
				
				mode = statistics.mode(np.array(values))
				self.memory.set_value(result, mode)

			elif (operator == "VAR"):
				values = [opRight]

				for i in range(opRight):
					values.append(float(self.memory.get_value(opLeft + i)))
				
				variance = statistics.variance(values)
				self.memory.set_value(result, variance)

			elif (operator == "SD"):
				values = [opRight]

				for i in range(opRight):
					values.append(float(self.memory.get_value(opLeft + i)))

				sd = np.std(np.array(values))
				self.memory.set_value(result, sd)

			elif (operator == "SCALE"):
				values = [opRight]

				for i in range(opRight):
					values.append(float(self.memory.get_value(opLeft + i)))
				
				newArray = stats.zscore(values)

				for i in range(opRight):
					self.memory.set_value(result + i, newArray[i])


			elif (operator == "AVG"):
				values = [opRight]

				for i in range(opRight):
					values.append(float(self.memory.get_value(opLeft + i)))
				
				avg = np.average(np.array(values))
				self.memory.set_value(result, avg)

			### END ###
			elif (operator == "END"):
				print()
				# memory.print()
				memory.pop_all()
				exit()
			


			else:
				# TODO fix newline bug
				print(f"\nSorry, operator {operator} is not supported yet.\n")
			ip += 1

	def parse_quad(self, quad):
		operator = quad.get_operator()
		opLeft  = quad.get_left_operand()
		opRight = quad.get_right_operand()
		result  = quad.get_result()

		if (opLeft != None):

			if (type(opLeft) == str and opLeft[0] == "$"):
				opLeft = int(opLeft.replace("$", ""))
				offset = self.get_offset(opLeft)
				opLeft = self.memory.get_value(opLeft + offset)
				opLeft = self.memory.get_value(opLeft + offset)
			elif (type(opLeft) == str and opLeft[0] == "*"):
				opLeft = int(opLeft.replace("*", ""))
			elif (type(opLeft) == str):
				opLeft = opLeft
			elif (opLeft != None):
				offset = self.get_offset(opLeft)
				opLeft = self.memory.get_value(opLeft + offset)

		if (opRight != None):
			if (type(opRight) == str and opRight[0] == "$"):
				opRight = int(opRight.replace("$", ""))
				offset = self.get_offset(opRight)
				opRight = self.memory.get_value(opRight + offset)
				opRight = self.memory.get_value(opRight + offset)
			elif (type(opRight) == str and opRight[0] == "*"):
				opRight = int(opRight.replace("*", ""))
			elif (opRight != None):
				offset = self.get_offset(opRight)
				opRight = self.memory.get_value(opRight + offset)
		
		if (result != None):
			if (type(result) == str and result[0] == "$"):
				result = int(result.replace("$", ""))
				offset = self.get_offset(result)
				result = self.memory.get_value(result + offset)
			elif (type(result) == str and result[0] == "*"):
				result = int(result.replace("*", ""))
			else:
				offset = self.get_offset(result)
				result = result + offset
		
		### "$" indicates a pointer
		### "*" indicates a literal value
		
		# print (f'opLeft: {opLeft}, opRight: {opRight}, result: {result}')
		return operator, opLeft, opRight, result
	
	
	def get_offset(self, var):
		offset = 0
		if (memory.get_scope(var) == 1):
			if (memory.get_type(var) == "int"):
				offset = self.offsetint
			elif (memory.get_type(var) == "float"):
				offset = self.offsetfloat
			elif (memory.get_type(var) == "char"):
				offset = self.offsetchar
			elif (memory.get_type(var) == "bool"):
				offset = self.offsetbool
			
		return offset




objectData = None
with open ('object.ovj', 'rb') as handle:
    objectData = pickle.load(handle)

quads = objectData['quadruples']
df = objectData['dirFunc']
memory  = objectData['memory']

machine = VirtualMachine(memory, quads, df)
machine.start_machine()