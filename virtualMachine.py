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
			# print(f'curr ip:\t{ip}')
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
			elif (operator == "BASESUM"):
				value = opLeft + quad.get_right_operand()
				self.memory.set_value(result, value)

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
				ip = int(quad.get_right_operand()) - 1
			elif (operator == "GOTOF"):
				if (not opLeft):
					ip = int(quad.get_right_operand()) - 1

			### READ / WRITE ###
			elif (operator == "READ"):
				value = input()
				type = self.memory.get_type(result)
				if (type == "int"):
					value = int(value)
				elif (type == "float"):
					value = float(value)
				elif (type == "char"):
					value = value
				elif (type == "bool"):
					value = bool(value)
				self.memory.set_value(result, value)

			elif (operator == "WRITE"):
				i = 0
				size = quad.get_right_operand()
				while(i < size):

					value = self.memory.get_value(quad.get_left_operand() + i)

					if (self.memory.get_type(quad.get_left_operand() + i) == "char"):
						value = chr(value)

					if (value == "\n"):
						print("\n> ", end = "")
					else:
						print(value, end="")

					i += 1
			
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
		if (type(opRight) == str and opRight[0] == "$"):
			opRight = int(opRight.replace("$", ""))
			opRight = self.memory.get_value(opRight)
		if (type(result) == str and result[0] == "$"):
			result = int(result.replace("$", ""))
			result = self.memory.get_value(result)

		if (opLeft != None):
			opLeft = self.memory.get_value(opLeft)
		if (opRight != None):
			opRight = self.memory.get_value(opRight)
		if (result != None):
			result = self.memory.get_value(result)
		return operator, opLeft, opRight, result




objectData = None
with open ('object.ovj', 'rb') as handle:
    objectData = pickle.load(handle)

quads = objectData['quadruples']
df = objectData['dirFunc']
memory  = objectData['memory']

machine = VirtualMachine(memory, quads, df)
machine.start_machine()
memory.print()