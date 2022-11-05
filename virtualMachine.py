import pickle
import string
import virtualMemory

class VirtualMachine:
	def __init__(self, memory, quads, df):
		self.memory = memory
		self.quads = quads
		self.df = df

	def start_machine(self):
		ip = 0			# instruction pointer
		checkpoint = []	# checkpoint stack
		startedWriting = True
		finishedWriting = False
		print("> ", end="")
		while (self.quads[ip].get_operator() != "END"):
			
			quad = self.quads[ip]
			# print(f'curr ip: #{ip}', end=" ")
			# quad.print()
			operator, opLeft, opRight, result = self.parse_quad(quad)
			### SWITCH ###
			### ARYTHMETICS ###
			if (operator == "="):
				value = opLeft
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
				value = opLeft / opRight
				self.memory.set_value(result, value)
				# self.memory.set_value(result, opLeft / opRight)
			
			# Used to sum the base value for an array
			elif (operator == "BSUM"):
				value = opLeft + quad.get_right_operand()
				# print(f'BSUM: {value}, storing in {result}')
				self.memory.set_value(result, value)
			
			elif (operator == "VER"):
				if (opLeft < 0 or opLeft > quad.get_result()):
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
				myType = self.memory.get_myType(result)
				if (myType == "int"):
					value = int(value)
				elif (myType == "float"):
					value = float(value)
				elif (myType == "char"):
					value = value
				elif (myType == "bool"):
					value = bool(value)
				self.memory.set_value(result, value)

			elif (operator == "WRITE"):
				i = 0
				size = quad.get_right_operand()
				opLeft = quad.get_left_operand()
				if (type(opLeft) == str and opLeft[0] == "$"):
					opLeft = opLeft.replace('$', '')
					opLeft = int(opLeft)
					opLeft = self.memory.get_value(opLeft)

				while(i < size):

						
					value = self.memory.get_value(opLeft + i)

					if (self.memory.get_type(opLeft + i) == "char"):
						value = chr(value)

					if (value == "\n"):
						print("\n> ", end = "")
					else:
						print(value, end = "")

					i += 1
			
			elif (operator == "ENDFUNC"):
				x = 1
			
			elif (operator == "END"):
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

		if (type(opLeft) == str and opLeft[0] == "$"):
			opLeft = int(opLeft.replace("$", ""))
			opLeft = self.memory.get_value(opLeft)
			opLeft = self.memory.get_value(opLeft)
		elif (type(opLeft) == str and opLeft[0] == "*"):
			opLeft = int(opLeft.replace("*", ""))
		elif (opLeft != None):
			opLeft = self.memory.get_value(opLeft)
		
		if (type(opRight) == str and opRight[0] == "$"):
			opRight = int(opRight.replace("$", ""))
			opRight = self.memory.get_value(opRight)
			opRight = self.memory.get_value(opRight)
		elif (type(opRight) == str and opRight[0] == "*"):
			opRight = int(opRight.replace("*", ""))
		elif (opRight != None):
			opRight = self.memory.get_value(opRight)
		
		if (type(result) == str and result[0] == "$"):
			result = int(result.replace("$", ""))
			result = self.memory.get_value(result)
		
		# $ indicates a pointer
		# * indicates a quad address
		
		# print (f'opLeft: {opLeft}, opRight: {opRight}, result: {result}')
		return operator, opLeft, opRight, result




objectData = None
with open ('object.ovj', 'rb') as handle:
    objectData = pickle.load(handle)

quads = objectData['quadruples']
df = objectData['dirFunc']
memory  = objectData['memory']

machine = VirtualMachine(memory, quads, df)
machine.start_machine()
print()
memory.print()