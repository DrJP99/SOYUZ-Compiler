from oracle import TIRESIAS

# Quadruple Table class deals with storing all the Quadruples plus the auxiliary stacks
class QuadrupleTable:
	def __init__(self):
		self.stackOperators = []	# Stack of operators
		self.stackOperands = []		# stack of IDs of operands
		self.stackTypes = []		# stack of types
		self.stackJumps = []		# stack of JUMPS for IFs and LOOPs
		self.listOfQuadruples = []	# list of generated Quadruples
		self.count = 1				# Points to the next Quadruple
		self.temp = 500				# Used to assign temporary variables

	# def generate(self, operator, operandL, operandR):
	# 	self.listOfQuadruples.append(quad)
	# 	count += 1

	def generate(self):
		opRight = self.pop_operands()
		typeRight = self.pop_types()

		opLeft = self.pop_operands()
		typeLeft = self.pop_types()

		operator = self.pop_operands()

		typeRes = self.check_for_missmatch(typeLeft, typeRight, operator)
		self.listOfQuadruples(operator, opLeft, opRight, f'temp{self.temp}')
		self.push_id_type(f'temp{self.temp}', typeRes)

		self.temp += 1
		self.count += 1


	## PUSH ##
	def push_id_type(self, newId, newType):
		self.stackOperands.append(newId)
		self.stackTypes.append(newType)

	def push_operator(self, op):
		self.stackOperators.append(op)
	
	def push_ff(self):
		self.stackOperators('(')

	## POP ##

	def pop_operators(self):
		return self.stackOperators.pop()

	def pop_operands(self):
		return self.stackOperands.pop()
	
	def pop_types(self):
		return self.stackTypes.pop()
	
	def pop_jumps(self):
		return self.stackJumps.pop()
	
	def pop_ff(self):
		if (self.get_top_operators == '('):
			self.pop_operators()

	
	#### GETTERS ####
	
	def top_operators(self):
		return self.stackOperators[-1]

	def top_operands(self):
		return self.stackOperands[-1]
	
	def top_types(self):
		return self.stackTypes[-1]
	
	def top_jumps(self):
		return self.stackJumps[-1]
	
	def get_curr_counter(self):
		return self.count
	
	def check_for_missmatch(self, typeL, typeR, op):
		try:
			resType = TIRESIAS[typeL][typeR][op]
			return resType
		except:
			print("Type missmatch!")
			exit()
	
	def print(self):
		for i in self.listOfQuadruples:
			print(f'#{i}:', end='\t')
			self.listOfQuadruples[i].print()

# Quadruples class helps with atomic Quadruples
class Quadruple:
	def __init__(self, operator, leftOperand, rightOperand, temp):
		self.operator = operator
		self.leftOperand = leftOperand
		self.rightOperand = rightOperand
		self.temp = temp
	
	def print(self):
		print(f'[{self.operator}, {self.leftOperand}, {self.rightOperand}, {self.temp}]')
