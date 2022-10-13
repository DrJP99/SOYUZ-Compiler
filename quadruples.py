from oracle import TIRESIAS

# TODO generate QUADS for WHILE and FOR loops

# Quadruple Table class deals with storing all the Quadruples plus the auxiliary stacks
class QuadrupleTable:
	def __init__(self):
		self.stackOperators = []	# Stack of operators
		self.stackOperands = []		# stack of IDs of operands
		self.stackTypes = []		# stack of types
		self.stackJumps = []		# stack of JUMPS for IFs and LOOPs
		self.listOfQuadruples = []	# list of generated Quadruples
		self.count = 1				# Points to the next Quadruple
		self.temp = 1				# Used to assign temporary variables

	# def generate(self, operator, operandL, operandR):
	# 	self.listOfQuadruples.append(quad)
	# 	count += 1

	# Automatically generates the next quadruple
	def generate(self):
		opRight = self.pop_operands()
		typeRight = self.pop_types()

		opLeft = self.pop_operands()
		typeLeft = self.pop_types()

		operator = self.pop_operators()

		typeRes = self.check_for_mismatch(typeLeft, typeRight, operator)
		# Normal operators have two operands but '=' has only one so we need to make a different function
		if (not operator == '='):
			newQuad = Quadruple(operator, opLeft, opRight, f't{self.temp}')
			self.listOfQuadruples.append(newQuad)
			self.push_id_type(f't{self.temp}', typeRes)
			# newQuad.print()
		else:
			self.generate_equal(opRight, opLeft)

		self.temp += 1
		self.count += 1

	# Generates a quadruple for the '=' operator
	def generate_equal(self, assignFrom, assignTo):
		newQuad = Quadruple('=', assignFrom, None, assignTo)
		self.listOfQuadruples.append(newQuad)
		# newQuad.print()

	# Generates a quadruple for the first NP of the IF
	def generate_g_if(self):
		cond = self.pop_operands()
		typeCond = self.pop_types()

		if (not typeCond == 'bool'):
			print("ERROR, conditional must be of type BOOL")
			exit()
		else:
			newQuad = Quadruple('gotoF', cond, None, None)
			self.listOfQuadruples.append(newQuad)
			# newQuad.print()
			self.stackJumps.append(self.count-1)
			self.count += 1
	
	def generate_end(self):
		newQuad = Quadruple('END', None, None, None)
		self.listOfQuadruples.append(newQuad)
		self.count += 1

	# Generates a quadruple for the CONDITIONAL LOOP
	def generate_g_cond_loop_s(self):
		typeExp = self.pop_types()
		if (not typeExp == 'bool'):
			print("ERROR, conditional must be of type BOOL")
			exit()
		else:
			result = self.pop_operands()
			newQuad = Quadruple('gotoF', result, None, None)
			self.listOfQuadruples.append(newQuad)
			self.stackJumps.append(self.count-1)
			self.count += 1
	
	def generate_g_cond_loop_e(self):
		end = self.pop_jumps()
		ret = self.pop_jumps()
		newQuad = Quadruple('goto', ret, None, None)
		self.listOfQuadruples.append(newQuad)
		self.fill_jump(end, self.count)
		self.count += 1
	
	def generate_g_nloop_s(self):
		self.stackJumps.append(self.count-1)
		self.stackJumps.append(self.count)
		
		self.push_operator('<')
		opRight = self.pop_operands()
		typeRight = self.pop_types()

		opLeft = self.pop_operands()
		typeLeft = self.pop_types()

		operator = '<'

		typeRes = self.check_for_mismatch(typeLeft, typeRight, operator)
		newQuad = Quadruple(operator, opLeft, opRight, f't{self.temp}')
		self.listOfQuadruples.append(newQuad)

		self.push_id_type(opLeft, typeLeft)
		self.push_id_type(f't{self.temp}', typeRes)
		# newQuad.print()

		self.temp += 1
		self.count += 1


		res = self.pop_operands()
		resType = self.pop_types()

		newQuad = Quadruple('gotoF', res, None, None)
		self.listOfQuadruples.append(newQuad)
		self.count += 1
		print('jumps : ', self.stackJumps)

	def generate_g_nloop_e(self):
		end = self.pop_jumps()
		ret = self.pop_jumps()

		my = self.pop_operands()
		myType = self.pop_types()

		resType = self.check_for_mismatch(myType, 'int', '+')
		newQuad = Quadruple('+', my, 1, f't{self.temp}')
		self.listOfQuadruples.append(newQuad)
		self.stackTypes.append(resType)
		self.push_id_type(f't{self.temp}', resType)

		self.count += 1
		self.temp += 1 

		res = self.top_operands()
		newQuad = Quadruple('=', res, None, my)
		self.listOfQuadruples.append(newQuad)

		self.count += 1
		self.fill_jump(end, self.count)

		newQuad = Quadruple('goto', ret, None, None)
		self.listOfQuadruples.append(newQuad)
		self.count += 1

	
	# Fills the GOTO jump from qFrom to qTarget
	def fill_jump(self, qFrom, qTarget):
		self.listOfQuadruples[qFrom].fill_jump(qTarget)
	
	# Generates a quadruple for the NP of the ELSE
	def generate_g_else(self):
		false = self.pop_jumps()
		newQuad = Quadruple('goto', None, None, None)
		self.listOfQuadruples.append(newQuad)
		self.stackJumps.append(self.count-1)
		self.fill_jump(false, self.count)
		self.count += 1
	
	
	def generate_g_read(self):
		op = self.pop_operands()
		newQuad = Quadruple('read', None, None, op)
		self.listOfQuadruples.append(newQuad)
		self.count += 1

	def generate_g_write(self):
		op = self.pop_operands()
		newQuad = Quadruple('write', op, None, None)
		self.listOfQuadruples.append(newQuad)
		self.count += 1

	## PUSH ##
	# Since ID and TYPE are always pushed at the same time, they are combined in this function
	def push_id_type(self, newId, newType):
		self.stackOperands.append(newId)
		self.stackTypes.append(newType)
		# print('operands: ', self.stackOperands)
		# print('types   : ', self.stackTypes)

	# Pushes to the stack of operators
	def push_operator(self, op):
		self.stackOperators.append(op)
		# print('oprtors : ', self.stackOperators)
	
	# Pushes a fake bottom FF to the stack of operators
	def push_ff(self):
		self.stackOperators.append('(')

	def push_jump(self, jump):
		self.stackJumps.append(self.count + jump)

	## POP ##

	# Removes last element and returns it #
	def pop_operators(self):
		return self.stackOperators.pop()

	def pop_operands(self):
		return self.stackOperands.pop()
	
	def pop_types(self):
		return self.stackTypes.pop()
	
	def pop_jumps(self):
		return self.stackJumps.pop()
	
	def pop_ff(self):
		self.pop_operators()

	
	#### GETTERS ####
	
	# PEEKS to the last element of the stack without needing to POP it
	def top_operators(self):
		if (self.stackOperators):
			return f'{self.stackOperators[-1]}'
		else:
			return None

	def top_operands(self):
		if (self.stackOperands):
			return f'{self.stackOperands[-1]}'
		else:
			return None
	
	def top_types(self):
		if (self.stackTypes):
			return self.stackTypes[-1]
		else:
			return None
	
	def top_jumps(self):
		if (self.stackJumps):
			return self.stackJumps[-1]
		else:
			return None
	
	# Returns the current counter
	def get_curr_counter(self):
		return self.count
	
	# Checks with the ORACLE if the types are allowed together and returns the result type, otherwise returns a type MISMATCH ERROR
	def check_for_mismatch(self, typeL, typeR, op):
		# print('trying to check types:', typeL, typeR, op)
		try:
			resType = TIRESIAS[typeL][typeR][op]
			# print ('results in: ', resType)
			return resType
		except:
			print(f'Type mismatch! Impossible to {typeL} {op} {typeR}')
			exit()
	
	# Prints all the quadruples generated
	def print(self):
		cont = 0
		# print(len(self.listOfQuadruples))
		# print(self.stackOperators)
		# print(self.stackOperands)
		print("\n~~~>Quadruples generated<~~~")
		while cont < len(self.listOfQuadruples):
			print(f'#{cont}:', end='\t')
			self.listOfQuadruples[cont].print()
			cont += 1

# Quadruples class helps with atomic Quadruples
class Quadruple:
	def __init__(self, operator, leftOperand, rightOperand, result):
		self.operator = operator
		self.leftOperand = leftOperand
		self.rightOperand = rightOperand
		self.result = result
	
	# Fills the jump target of a GOTO quadruple
	def fill_jump(self, target):
		self.rightOperand = target

	# Prints an individual quadruple
	def print(self):
		print(f'[{self.operator}, {self.leftOperand}, {self.rightOperand}, {self.result}]', end='\n')
