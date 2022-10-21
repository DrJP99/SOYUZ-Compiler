import pickle
import virtualMemory

class VirtualMachine:
	def __init__(self, memory, quads, df):
		self.memory = memory
		self.quads = quads
		self.df = df

	def start_machine(self):
		ip = 0			# instruction pointer
		checkpoint = []	# checkpoint stack
		while (self.quads[ip].get_operator() != "END"):
			# print(f'curr ip:\t{ip}')
			quad = self.quads[ip]
			### SWITCH ###
			### ARYTHMETICS ###
			if (quad.get_operator() == "="):
				value = self.memory.get_value(quad.get_left_operand())
				self.memory.set_value(quad.get_result(), value)
				# self.memory.set_value(quad.get_result(), self.memory.get_value(quad.get_left_operand()))
				
			elif (quad.get_operator() == "+"):
				opLeft = self.memory.get_value(quad.get_left_operand())
				opRight = self.memory.get_value(quad.get_right_operand())
				result = opLeft + opRight
				self.memory.set_value(quad.get_result(), result)
				# self.memory.set_value(quad.get_result(), self.memory.get_value(quad.get_left_operand()) + self.memory.get_value(quad.get_right_operand()))
				
			elif (quad.get_operator() == "-"):
				opLeft = self.memory.get_value(quad.get_left_operand())
				opRight = self.memory.get_value(quad.get_right_operand())
				result = opLeft - opRight
				self.memory.set_value(quad.get_result(), result)
				# self.memory.set_value(quad.get_result(), self.memory.get_value(quad.get_left_operand()) - self.memory.get_value(quad.get_right_operand()))
				
			elif (quad.get_operator() == "*"):
				opLeft = self.memory.get_value(quad.get_left_operand())
				opRight = self.memory.get_value(quad.get_right_operand())
				result = opLeft * opRight
				self.memory.set_value(quad.get_result(), result)
				# self.memory.set_value(quad.get_result(), self.memory.get_value(quad.get_left_operand()) * self.memory.get_value(quad.get_right_operand()))
				
			elif (quad.get_operator() == "/"):
				opLeft = self.memory.get_value(quad.get_left_operand())
				opRight = self.memory.get_value(quad.get_right_operand())
				result = opLeft / opRight
				self.memory.set_value(quad.get_result(), result)
				# self.memory.set_value(quad.get_result(), self.memory.get_value(quad.get_left_operand()) / self.memory.get_value(quad.get_right_operand()))
				

			### RELATIONAL ###
			elif (quad.get_operator() == "=="):
				if (self.memory.get_value(quad.get_left_operand()) == self.memory.get_value(quad.get_right_operand())):
					self.memory.set_value(quad.get_result(), 1)
				else:
					self.memory.set_value(quad.get_result(), 0)
			elif (quad.get_operator() == "!="):
				if (self.memory.get_value(quad.get_left_operand()) != self.memory.get_value(quad.get_right_operand())):
					self.memory.set_value(quad.get_result(), 1)
				else:
					self.memory.set_value(quad.get_result(), 0)
			elif (quad.get_operator() == ">"):
				if (self.memory.get_value(quad.get_left_operand()) > self.memory.get_value(quad.get_right_operand())):
					self.memory.set_value(quad.get_result(), 1)
				else:
					self.memory.set_value(quad.get_result(), 0)
			elif (quad.get_operator() == ">="):
				if (self.memory.get_value(quad.get_left_operand()) >= self.memory.get_value(quad.get_right_operand())):
					self.memory.set_value(quad.get_result(), 1)
				else:
					self.memory.set_value(quad.get_result(), 0)
			elif (quad.get_operator() == "<"):
				if (self.memory.get_value(quad.get_left_operand()) < self.memory.get_value(quad.get_right_operand())):
					self.memory.set_value(quad.get_result(), 1)
				else:
					self.memory.set_value(quad.get_result(), 0)
			elif (quad.get_operator() == "<="):
				if (self.memory.get_value(quad.get_left_operand()) <= self.memory.get_value(quad.get_right_operand())):
					self.memory.set_value(quad.get_result(), 1)
				else:
					self.memory.set_value(quad.get_result(), 0)
			elif (quad.get_operator() == "&&"):
				if (self.memory.get_value(quad.get_left_operand()) and self.memory.get_value(quad.get_right_operand())):
					self.memory.set_value(quad.get_result(), 1)
				else:
					self.memory.set_value(quad.get_result(), 0)
			elif (quad.get_operator() == "||"):
				if (self.memory.get_value(quad.get_left_operand()) or self.memory.get_value(quad.get_right_operand())):
					self.memory.set_value(quad.get_result(), 1)
				else:
					self.memory.set_value(quad.get_result(), 0)

			### JUMPS ###
			elif (quad.get_operator() == "GOTO"):
				ip = quad.get_right_operand() - 1
			elif (quad.get_operator() == "GOTOF"):
				if (not self.memory.get_value(quad.get_left_operand())):
					ip = quad.get_right_operand() - 1

			### READ / WRITE ###
			elif (quad.get_operator() == "READ"):
				print("> ", end=" ")
				value = input()
				type = self.memory.get_type(quad.get_result())
				if (type == "int"):
					value = int(value)
				elif (type == "float"):
					value = float(value)
				elif (type == "char"):
					value = ascii(value)
				elif (type == "bool"):
					value = bool(value)
				self.memory.set_value(quad.get_result(), value)
			elif (quad.get_operator() == "WRITE"):
				print("> ", self.memory.get_value(quad.get_left_operand()))
			
			elif (quad.get_operator() == "END"):
				exit()
			


			else:
				print(f"Sorry, operator {quad.get_operator()} is not supported yet.")

			ip += 1




objectData = None
with open ('object.ovj', 'rb') as handle:
    objectData = pickle.load(handle)

quads = objectData['quadruples']
df = objectData['dirFunc']
memory  = objectData['memory']

machine = VirtualMachine(memory, quads, df)
machine.start_machine()