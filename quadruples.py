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
		# self.temp = 1				# Used to assign temporary variables
		self.resourceInt = 0		# Used to count int temporary variables
		self.resourceFloat = 0		# Used to count float temporary variables
		self.resourceBool = 0		# Used to count bool temporary variables
		self.resourceChar = 0		# Used to count char temporary variables

	# def generate(self, operator, operandL, operandR):
	# 	self.listOfQuadruples.append(quad)
	# 	increase_count()

	def increase_count(self):
		# print(f"quadruple {self.count} generated: ", end='')
		# self.listOfQuadruples[-1].print()
		# print(f"stack of operators: {self.stackOperators}")
		# print(f"stack of operands: {self.stackOperands}")
		self.count += 1

	def get_ops_type(self):
		opRight = self.pop_operands()
		typeRight = self.pop_types()

		opLeft = self.pop_operands()
		typeLeft = self.pop_types()

		operator = self.pop_operators()

		typeRes = self.check_for_mismatch(typeLeft, typeRight, operator)
		return operator, opLeft, opRight, typeRes

	# Automatically generates the next quadruple
	def generate(self, operator, opLeft, opRight, typeRes, address):
		
		temp = address
		# self.add_count(typeRes)

		# Normal operators have two operands but '=' has only one so we need to make a different function
		if (not operator == '='):
			newQuad = Quadruple(operator, opLeft, opRight, temp)
			self.listOfQuadruples.append(newQuad)
			self.push_id_type(temp, typeRes)
			# newQuad.print()
		else:
			self.generate_equal(opRight, opLeft)

		# self.temp += 1
		self.increase_count()

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
			newQuad = Quadruple('GOTOF', cond, None, None)
			self.listOfQuadruples.append(newQuad)
			# newQuad.print()
			self.stackJumps.append(self.count-1)
			self.increase_count()
	
	def generate_end(self):
		newQuad = Quadruple('END', None, None, None)
		self.listOfQuadruples.append(newQuad)
		self.increase_count()

	# Generates a quadruple for the CONDITIONAL LOOP
	def generate_g_cond_loop_s(self):
		typeExp = self.pop_types()
		if (not typeExp == 'bool'):
			print("ERROR, conditional must be of type BOOL")
			exit()
		else:
			result = self.pop_operands()
			newQuad = Quadruple('GOTOF', result, None, None)
			self.listOfQuadruples.append(newQuad)
			self.stackJumps.append(self.count-1)
			self.increase_count()
	
	def generate_g_cond_loop_e(self):
		end = self.pop_jumps()
		ret = self.pop_jumps()
		newQuad = Quadruple('GOTO', None, f'*{ret - 1}', None)	# GOTO brginning of loop
		self.listOfQuadruples.append(newQuad)

		self.fill_jump(end, self.count)					# Fill the jump to the end of the loop
		self.increase_count()
	
	def generate_g_nloop_s_pre(self):
		self.stackJumps.append(self.count-1)	# Push the jump to the start
		self.stackJumps.append(self.count)
		
		# self.push_operator('<')
		opRight = self.pop_operands()
		typeRight = self.pop_types()

		opLeft = self.pop_operands()
		typeLeft = self.pop_types()

		operator = '<'

		typeRes = self.check_for_mismatch(typeLeft, typeRight, operator)

		return operator, opLeft, typeLeft, opRight, typeRes

	def generate_g_nloop_s(self, operator, opLeft, typeLeft, opRight, typeRes, address):
		# self.add_count(typeRes)

		newQuad = Quadruple(operator, opLeft, opRight, address)
		self.listOfQuadruples.append(newQuad)

		self.push_id_type(opLeft, typeLeft)
		self.push_id_type(address, typeRes)
		# newQuad.print()

		# self.temp += 1
		self.increase_count()

		res = self.pop_operands()
		resType = self.pop_types()

		newQuad = Quadruple('GOTOF', res, None, None)
		self.listOfQuadruples.append(newQuad)
		self.increase_count()
		# print('jumps : ', self.stackJumps)

	def generate_g_nloop_e_pre(self):
		end = self.pop_jumps()
		ret = self.pop_jumps()

		my = self.pop_operands()
		myType = self.pop_types()

		resType = self.check_for_mismatch(myType, 'int', '+')

		return end, ret, my, resType


	def generate_g_nloop_e(self, end, ret, my, resType, address, address_1):
		# self.add_count(resType)

		newQuad = Quadruple('+', my, address_1, address)
		self.listOfQuadruples.append(newQuad)
		self.stackTypes.append(resType)
		self.push_id_type(address, resType)

		self.increase_count()
		# self.temp += 1 

		res = self.top_operands()
		newQuad = Quadruple('=', res, None, my)
		self.listOfQuadruples.append(newQuad)

		self.increase_count()
		self.fill_jump(end, self.count)

		newQuad = Quadruple('GOTO', None, f'*{ret}', None)
		self.listOfQuadruples.append(newQuad)
		self.increase_count()

	
	# Fills the GOTO jump from qFrom to qTarget
	def fill_jump(self, qFrom, qTarget):
		self.listOfQuadruples[qFrom].fill_jump(qTarget)
	
	# Generates a quadruple for the NP of the ELSE
	def generate_g_else(self):
		false = self.pop_jumps()
		newQuad = Quadruple('GOTO', None, None, None)
		self.listOfQuadruples.append(newQuad)
		self.stackJumps.append(self.count-1)
		self.fill_jump(false, self.count)
		self.increase_count()
	
	
	def generate_g_read(self):
		op = self.pop_operands()
		newQuad = Quadruple('READ', None, None, op)
		self.listOfQuadruples.append(newQuad)
		self.increase_count()

	def generate_g_write(self, size=1):
		op = self.pop_operands()
		newQuad = Quadruple('WRITE', op, f'*{size}', None)
		self.listOfQuadruples.append(newQuad)
		self.increase_count()

	def generate_g_verify(self, d, size, m, dims, address = 0, address2 = 0):
		top = self.top_operands()
		newQuad = Quadruple('VER', top, f'*{0}', f'*{size - 1}')
		self.listOfQuadruples.append(newQuad)
		self.increase_count()
		
		if (dims != d):
			T = address
			aux = self.pop_operands()
			newQuad = Quadruple('*', aux, f'*{m}', T)
			self.listOfQuadruples.append(newQuad)
			self.increase_count()
			self.stackOperands.append(T)

		if (d > 1):
			T = address2
			aux2 = self.pop_operands()
			aux1 = self.pop_operands()
			newQuad = Quadruple('+', aux1, aux2, T)
			self.listOfQuadruples.append(newQuad)
			self.increase_count()
			self.stackOperands.append(T)

	def generate_g_dims_end(self, base, address):
		T = address
		aux = self.pop_operands()
		newQuad = Quadruple('+', aux, f'*{base}', T)
		self.listOfQuadruples.append(newQuad)
		self.increase_count()
		self.stackOperands.append(f'${T}')
		self.pop_operators()
	
	def generate_g_return(self):
		op = self.pop_operands()
		newQuad = Quadruple('RETURN', op, None, None)
		self.listOfQuadruples.append(newQuad)
		self.increase_count()
	
	def generate_g_histogram(self, address, xDim):
		op = self.pop_operands()
		newQuad = Quadruple('HIST', f'*{address}', f'*{xDim}', op)
		self.listOfQuadruples.append(newQuad)
		self.increase_count()
	
	def generate_g_mean(self, address, xDim, newAddress):
		newQuad = Quadruple('MEAN', f'*{address}', f'*{xDim}', newAddress)
		self.listOfQuadruples.append(newQuad)
		self.increase_count()
		self.stackOperands.append(newAddress)
		self.stackTypes.append('float')
	
	def generate_g_mode(self, address, xDim, newAddress):
		newQuad = Quadruple('MODE', f'*{address}', f'*{xDim}', newAddress)
		self.listOfQuadruples.append(newQuad)
		self.increase_count()
		self.stackOperands.append(newAddress)
		self.stackTypes.append('int')
	
	def generate_g_variance(self, address, xDim, newAddress):
		newQuad = Quadruple('VAR', f'*{address}', f'*{xDim}', newAddress)
		self.listOfQuadruples.append(newQuad)
		self.increase_count()
		self.stackOperands.append(newAddress)
		self.stackTypes.append('float')
	
	def generate_g_standard_deviation(self, address, xDim, newAddress):
		newQuad = Quadruple('SD', f'*{address}', f'*{xDim}', newAddress)
		self.listOfQuadruples.append(newQuad)
		self.increase_count()
		self.stackOperands.append(newAddress)
		self.stackTypes.append('float')

	def generate_g_scale(self, address, xDim, newAddress):
		newQuad = Quadruple('SCALE', f'*{address}', f'*{xDim}', newAddress)
		self.listOfQuadruples.append(newQuad)
		self.increase_count()
		self.stackOperands.append(newAddress)
		self.stackTypes.append('float')

	def generate_g_average(self, address, xDim, newAddress):
		newQuad = Quadruple('AVG', f'*{address}', f'*{xDim}', newAddress)
		self.listOfQuadruples.append(newQuad)
		self.increase_count()
		self.stackOperands.append(newAddress)
		self.stackTypes.append('float')
	
	def generate_g_median(self, address, xDim, newAddress):
		newQuad = Quadruple('MEDIAN', f'*{address}', f'*{xDim}', newAddress)
		self.listOfQuadruples.append(newQuad)
		self.increase_count()
		self.stackOperands.append(newAddress)
		self.stackTypes.append('float')

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
			return self.stackOperands[-1]
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
	
	def get_list_of_quadruples(self):
		return self.listOfQuadruples
	
	def generate_g_end_func(self):
		newQuad = Quadruple('ENDFUNC', None, None, None)
		self.listOfQuadruples.append(newQuad)
		self.increase_count()

	def add_count(self, type):
		if type == 'int':
			self.resourceInt += 1
		elif type == 'float':
			self.resourceFloat += 1
		elif type == 'char':
			self.resourceChar += 1
		elif type == 'bool':
			self.resourceBool += 1
		else:
			print('ERROR: Type not found')
			exit()
	
	def reset_counts(self):
		ints = self.resourceInt
		floats = self.resourceFloat
		chars = self.resourceChar
		bools = self.resourceBool

		self.resourceInt = 0
		self.resourceFloat = 0
		self.resourceChar = 0
		self.resourceBool = 0

		return ints, floats, chars, bools

	# Generates quadruple for Activation Record Expansion
	def generate_g_era(self, i, f, c, b):
		newQuad = Quadruple('ERAI', f'*{i}', None, None)
		self.listOfQuadruples.append(newQuad)
		self.increase_count()

		newQuad = Quadruple('ERAF', f'*{f}', None, None)
		self.listOfQuadruples.append(newQuad)
		self.increase_count()

		newQuad = Quadruple('ERAC', f'*{c}', None, None)
		self.listOfQuadruples.append(newQuad)
		self.increase_count()

		newQuad = Quadruple('ERAB', f'*{b}', None, None)
		self.listOfQuadruples.append(newQuad)
		self.increase_count()
	
	def generate_g_param(self, argument, k):
		newQuad = Quadruple('PARAM', f'*{argument}', None, f'*{k}')
		self.listOfQuadruples.append(newQuad)
		self.increase_count()
	
	def generate_g_gosub(self, funcName, init, save):
		newQuad = Quadruple('GOSUB', funcName, f'*{init}', save)
		self.listOfQuadruples.append(newQuad)
		self.increase_count()
	
	def generate_main_goto(self):
		newQuad = Quadruple('GOTO', None, None, None)
		self.listOfQuadruples.append(newQuad)
		self.increase_count()

	# Prints all the quadruples generated
	def print(self):
		cont = 0
		# print(len(self.listOfQuadruples))
		# print(self.stackOperators)
		# print(self.stackOperands)

		print("\n=========== Quadruples  Generated ===========\n")
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
		self.rightOperand = f'*{target}'

	# Prints an individual quadruple
	def print(self):
		print(f'[{self.operator}, {self.leftOperand}, {self.rightOperand}, {self.result}]', end='\n')
	
	def get_operator(self):
		return self.operator
	
	def get_left_operand(self):
		return self.leftOperand
	
	def get_right_operand(self):
		return self.rightOperand
	
	def get_result(self):
		return self.result
