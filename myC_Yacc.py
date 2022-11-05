'''
Grammar for the SOYUZ Programming Language
Created by Juan Pablo González 2022(C)
Created for the Compiler Design Course
'''

import subprocess
import pickle
import ply.yacc as yacc
from myC_Lex import tokens
from functionDirectory import DirFunc as DF
from functionDirectory import varAttributes as VA
from quadruples import QuadrupleTable 

df = DF()
vAtts = VA()

currId = ""
currType = ""
currScope = 0
currDims = 0
currReturnType = ""
currFunc = ""
xDim = 0
yDim = 0

stackDims = []
stackDimsId = []

writeStr = False
strLen = 1

quad = QuadrupleTable()

# Start of program
def p_program_start(p):
	'''
	program_start		: main_goto PROGRAM ID SEMICOL program_start_1 program_start_2 main
	'''

# Can have global vars or not
def p_program_start_1(p):
	'''
	program_start_1		: vars
	'''

# Can have funcs or not
def p_program_start_2(p):
	'''
	program_start_2		: funcs
						| empty
	'''

def p_vars(p):
	'''
	vars				: VAR type COL vars_1 SEMICOL vars
						| empty
	'''
def p_vars_1(p):
	'''
	vars_1				: ID see_id vars_2 push_var vars_3
	'''
def p_vars_2(p):
	'''
	vars_2				: dims_assign
						| empty
	'''
def p_vars_3(p):
	'''
	vars_3				: COMMA vars_1
						| empty
	'''

def p_dims_assign(p):
	'''
	dims_assign			: LBRACK see_dims_a CTEI see_dims_num dims_assign_1 RBRACK
	'''
def p_dims_assign_1(p):
	'''
	dims_assign_1		: COMMA see_dims_a CTEI see_dims_num
						| empty
	'''

# Variable type
def p_type(p):
	'''
	type				: INT
						| FLOAT
						| CHAR
						| BOOL
	'''
	global currType
	currType = p[1]
	# print(currType)

# Return type for functions
def p_rtype(p):
	'''
	rtype				: INT
						| FLOAT
						| CHAR
						| BOOL
						| VOID
	'''
	global currReturnType
	currReturnType = p[1]

def p_block(p):
	'''
	block				: LCURLY block_1 RCURLY
	'''
def p_block_1(p):
	'''
	block_1				: statement
	'''

def p_funcs(p):
	'''
	funcs				: FUNC rtype ID see_id see_func_start params LCURLY funcs_1 set_func_init statement funcs_2 see_func_end RCURLY funcs_3
	'''
def p_funcs_1(p):
	'''
	funcs_1				: vars
	'''
def p_funcs_2(p):
	'''
	funcs_2				: RETURN expression SEMICOL
						| empty
	'''
def p_funcs_3(p):
	'''
	funcs_3				: funcs
						| empty
	'''

def p_params(p):
	'''
	params				: LPAR params_1 RPAR
	'''
def p_params_1(p):
	'''
	params_1			: type ID see_id params_2 see_end_param reset_dims params_3
						| empty
	'''
def p_params_2(p):
	'''
	params_2			: dims
						| empty
	'''
def p_params_3(p):
	'''
	params_3			: COMMA params_1
						| empty
	'''

def p_assign(p):
	'''
	assign				: ID see_id push_id assign_1 EQUAL push_equal expression generate_assign SEMICOL
	'''
def p_assign_1(p):
	'''
	assign_1			: dims
						| empty
	'''

def p_dims(p):
	'''
	dims				: LBRACK see_dims expression generate_g_verify_f dims_1 RBRACK dims_end
	'''
def p_dims_1(p):
	'''
	dims_1				: COMMA see_dims_s expression generate_g_verify_s
						| empty
	'''

def p_statement(p):	
	'''
	statement			: statement_1 statement
						| empty
	'''
def p_statement_1(p):
	'''
	statement_1			: assign
						| cond
						| cloop
						| nloop
						| read
						| write
						| loadfile
						| callfunc SEMICOL
	'''

def p_cond(p):
	'''
	cond				: IF LPAR expression RPAR generate_g_if block cond_1 finish_if
	'''
def p_cond_1(p):
	'''
	cond_1				: ELSE generate_g_else cond_2
	'''
def p_cond_2(p):
	'''
	cond_2				: cond_3
						| block
	'''
def p_cond_3(p):
	'''
	cond_3				: cond
						| empty
	'''

# Conditional loop
def p_cloop(p):
	'''
	cloop				: WHILE cloop_push_jump LPAR expression generate_g_cloop_start RPAR block generate_g_cloop_end
	'''

# Non-conditional loop [from x = 1 to 10]
def p_nloop(p):
	'''
	nloop				: FROM ID see_id nloop_1 push_id nloop_2 TO expression generate_g_nloop_s block generate_g_nloop_e
	'''
def p_nloop_1(p):
	'''
	nloop_1				: dims
						| empty
	'''
def p_nloop_2(p):
	'''
	nloop_2				: push_id EQUAL push_equal expression generate_assign
						| empty
	'''

def p_callfunc(p):
	'''
	callfunc			: ID see_id verify_func LPAR activate_record callfunc_1 verify_p_num RPAR
	'''
def p_callfunc_1(p):
	'''
	callfunc_1			: expression verify_params callfunc_3
						| empty
	'''
# def p_callfunc_2(p):
# 	'''
# 	callfunc_2			: dims
# 						| empty
# 	'''
def p_callfunc_3(p):
	'''
	callfunc_3			: COMMA increase_p_count callfunc_1
						| empty
	'''
# def p_callfunc_4(p):
# 	'''
# 	callfunc_4			: ID callfunc_2
# 						| callfunc
# 						| CTEI
# 						| CTEF
# 						| CTEB
# 						| CTEC
# 	'''

def p_read(p):
	'''
	read				: READ LPAR read_1 RPAR SEMICOL
	'''
def p_read_1(p):
	'''
	read_1				: ID see_id read_2 push_id generate_g_read read_3
	'''
def p_read_2(p):
	'''
	read_2				: dims reset_dims
						| empty
	'''
def p_read_3(p):
	'''
	read_3				: COMMA read_1
						| empty
	'''

def p_write(p):
	'''
	write				: WRITE LPAR write_1 RPAR SEMICOL
	'''
def p_write_1(p):
	'''
	write_1				: write_2 generate_g_write write_3
	'''
def p_write_2(p):
	'''
	write_2				: expression
						| CTES push_string
	'''
def p_write_3(p):
	'''
	write_3				: COMMA write_1
						| empty
	'''

# READFILE
def p_loadfile(p):
	'''
	loadfile			: LOADFILE LPAR ID COMMA CTES COMMA loadfile_1 COMMA loadfile_2 RPAR SEMICOL
	'''

def p_loadfile_1(p):
	'''
	loadfile_1			: CTEI
						| ID
	'''

def p_loadfile_2(p):
	'''
	loadfile_2			: CTEI
						| ID
	'''

def p_expression(p):
	'''
	expression			: sexp check_and_or expression_1
	'''
def p_expression_1(p):
	'''
	expression_1		: expression_2 push_and_or expression
						| empty
	'''
def p_expression_2(p):
	'''
	expression_2		: OR
						| AND
	'''
	global quad
	quad.push_operator(f'{p[1]}')

def p_sexp(p):
	'''
	sexp				: exp check_relational sexp_1
	'''
def p_sexp_1(p):
	'''
	sexp_1				: sexp_2 push_relational sexp
						| empty
	'''
def p_sexp_2(p):
	'''
	sexp_2				: ISEQUAL		
						| EQUAL			
						| NOTEQUAL		
						| GREATERTHAN	
						| GREATERORQUAL	
						| LESSTHAN		
						| LESSOREQUAL	
	'''
	global quad
	quad.push_operator(f'{p[1]}')

def p_exp(p):
	'''
	exp					: term check_sum exp_1
	'''
def p_exp_1(p):
	'''
	exp_1				: exp_2 push_sum exp
						| empty
	'''
def p_exp_2(p):
	'''
	exp_2				: PLUS
						| MINUS
	'''
	global quad
	quad.push_operator(f'{p[1]}')

def p_term(p):
	'''
	term				: factor check_mul_div term_1
	'''
def p_term_1(p):
	'''
	term_1				: term_2 push_mul_div term
						| empty
	'''
def p_term_2(p):
	'''
	term_2				: TIMES
						| DIV
	'''
	global quad
	quad.push_operator(f'{p[1]}')

def p_factor(p):
	'''
	factor				: factor_1 
						| factor_2
	'''
def p_factor_1(p):
	'''
	factor_1			: ID see_id push_id factor_3 print_value reset_dims
						| callfunc
						| CTEI push_int
						| CTEF push_float
						| CTEB push_bool
						| CTEC push_char
						| MINUS factor_1
	'''
def p_factor_2(p):
	'''
	factor_2			: LPAR add_ff expression RPAR pop_ff
	'''
def p_factor_3(p):
	'''
	factor_3			: dims
						| empty
	'''

def p_main(p):
	'''
	main				: MAIN see_id LPAR RPAR LCURLY see_func_start main_1 set_func_init fill_main_goto statement END SEMICOL RCURLY see_func_end generate_end
	'''
def p_main_1(p):
	'''
	main_1				: vars
	'''

# Neuralgic points

def p_see_id(p):
	'''
	see_id				: empty
	'''
	global currId
	currId = p[-1]


def p_see_dims(p):
	'''
	see_dims			: empty
	'''
	global currDims, xDim, yDim, df, quad, currScope, stackDims, stackDimsId
	if (df.get_var_dims(currScope, currId) == 0):
		print(f"Error: Variable {currId} is not an array")
	else:
		currDims = 1
		stackDims.append(currDims)
		quad.pop_operands()
		stackDimsId.append(currId)
		quad.push_ff()

def p_see_dims_s(p):
	'''
	see_dims_s			: empty
	'''
	global currDims, stackDims, stackDimsId
	currDims += 1
	stackDims[-1] = currDims

def p_generate_g_verify_f(p):
	'''
	generate_g_verify_f	: empty
	'''
	global quad, df, quad, currScope, stackDimsId, stackDims, currDims
	size = df.get_var_xDim(currScope, stackDimsId[-1])
	# print(f"id: {stackDimsId[-1]}")
	# print(f"size: {size}")
	dims = df.get_var_dims(currScope, stackDimsId[-1])
	m = df.get_var_xDim(currScope, stackDimsId[-1])
	tempAddress = 0
	tempAddress2 = 0
	d = stackDims[-1]
	if (dims != d):
		tempAddress = df.generate_memory(currScope, 'int')
	if (d > 1):
		tempAddress2 = df.generate_memory(currScope, 'int')

	quad.generate_g_verify(d, size, m, dims, tempAddress, tempAddress2)  # type: ignore

def p_generate_g_verify_s(p):
	'''
	generate_g_verify_s	: empty
	'''
	global quad, df, quad, currScope, stackDimsId, stackDims
	size = df.get_var_yDim(currScope, stackDimsId[-1])
	dims = df.get_var_dims(currScope, stackDimsId[-1])
	m = df.get_var_xDim(currScope, stackDimsId[-1])
	tempAddress = 0
	tempAddress2 = 0
	d = stackDims[-1]
	if (dims != d):
		tempAddress = df.generate_memory(currScope, 'int')
	if (d > 1):
		tempAddress2 = df.generate_memory(currScope, 'int')
	quad.generate_g_verify(d, size, m, dims, tempAddress, tempAddress2)  # type: ignore

def p_dims_end(p):
	'''
	dims_end			: empty
	'''
	global currDims, stackDims, stackDimsId, quad, df
	# T = df.generate_memory(currScope, 'int')
	base = df.get_var_address(currScope, stackDimsId[-1])
	temp = df.generate_memory(currScope, 'int')
	quad.generate_g_dims_end(base, temp)

	stackDims.pop()
	stackDimsId.pop()

def p_see_dims_a(p):
	'''
	see_dims_a			: empty
	'''
	global currDims, currId, df, stackDims
	currDims += 1


def p_see_dims_num(p):
	'''
	see_dims_num		: empty
	'''
	global currDims, currId, df, xDim, yDim
	last = p[-1]
	if (currDims == 1):
		xDim = last
	else:
		yDim = last

def p_push_var(p):
	'''
	push_var			: empty
	'''
	global currId, currType, currDims, currScope, vAtts, df, xDim, yDim
	# print("Variable added:", currId, "\ttype:", currType, "\tdims:", currDims, "\tscope: ", currScope)
	newVar = {}
	if (currDims == 0):
		newVar = vAtts.create_var(currId, currType, currDims)
	elif (currDims == 1):
		newVar = vAtts.create_var(currId, currType, currDims, xDim)
	elif (currDims == 2):
		newVar = vAtts.create_var(currId, currType, currDims, xDim, yDim)
	df.add_var(currScope, newVar)
	currDims = 0

# def p_see_return_type(p):
# 	'''
# 	see_return_type		: empty
# 	'''
# 	global currReturnType
# 	currReturnType = p[-1]

def p_see_func_start(p):
	'''
	see_func_start		: empty
	'''
	global currId, currReturnType, currScope, df
	currScope += 1
	df.addFunction(currScope, currId, currReturnType)

def p_see_func_end(p):
	'''
	see_func_end		: empty
	'''
	global currScope, df, quad
	# df.printFunc()
	quad.generate_g_end_func()
	ints, floats, bools, chars = quad.reset_counts()
	df.add_resources(currScope, ints, floats, bools, chars)
	df.remove_function(currScope)
	currScope -= 1

def p_set_func_init(p):
	'''
	set_func_init		: empty
	'''
	global currScope, df, quad
	df.update_init(currScope, quad.get_curr_counter() - 1)

def p_see_end_param(p):
	'''
	see_end_param		: empty
	'''
	global currScope, currId, currDims, df, vAtts
	df.add_param(currScope, vAtts.create_var(currId, currType, currDims))

def p_reset_dims(p):
	'''
	reset_dims			: empty
	'''
	global currDims
	currDims = 0 

def p_print_value(p):
	'''
	print_value			: empty
	'''
	global currId, currDims, currScope, df
	# print(currId, ":", df.getVarValue(currScope, currId))

def p_check_and_or(p):
	'''
	check_and_or		: empty
	'''
	global quad, currScope, df
	if (quad.top_operators() == '&&' or quad.top_operators() == '||'):
		operator, opLeft, opRight, typeRes = quad.get_ops_type()
		address = df.generate_memory(currScope, typeRes)
		quad.generate(operator, opLeft, opRight, typeRes, address)

def p_push_and_or(p):
	'''
	push_and_or			: empty
	'''
	# global quad
	# quad.push_operator(f'{p[-1]}')

def p_check_relational(p):
	'''
	check_relational	: empty
	'''
	global quad, currScope, df
	# print('checking relational... ', quad.top_operators())
	rel = ['==', '!=', '>', '>=', '<', '<=',]
	if (quad.top_operators() in rel):
		# print('generating relational...')
		operator, opLeft, opRight, typeRes = quad.get_ops_type()
		address = df.generate_memory(currScope, typeRes)
		quad.generate(operator, opLeft, opRight, typeRes, address)

def p_push_relational(p):
	'''
	push_relational		: empty
	'''
	# global quad
	# quad.push_operator(f'{p[-1]}')

def p_check_sum(p):
	'''
	check_sum			: empty
	'''
	global quad, currScope, df
	# print('checking sum...', quad.top_operators())
	if (quad.top_operators() == '+' or quad.top_operators() == '-'):
		operator, opLeft, opRight, typeRes = quad.get_ops_type()
		address = df.generate_memory(currScope, typeRes)
		quad.generate(operator, opLeft, opRight, typeRes, address)

def p_push_sum(p):
	'''
	push_sum			: empty
	'''
	# global quad
	# quad.push_operator(f'{p[-1]}')

def p_check_mul_div(p):
	'''
	check_mul_div		: empty
	'''
	global quad, currScope, df
	# print('checking mul/div... ', quad.top_operators())
	if (quad.top_operators() == '*' or quad.top_operators() == '/'):
		operator, opLeft, opRight, typeRes = quad.get_ops_type()
		address = df.generate_memory(currScope, typeRes)
		quad.generate(operator, opLeft, opRight, typeRes, address)

def p_push_mul_div(p):
	'''
	push_mul_div		: empty
	'''
	# global quad
	# quad.push_operator(f'{p[-1]}')

def p_add_ff(p):
	'''
	add_ff				: empty
	'''
	global quad
	quad.push_ff()

def p_pop_ff(p):
	'''
	pop_ff				: empty
	'''
	global quad
	quad.pop_ff()

def p_push_int(p):
	'''
	push_int			: empty
	'''
	global quad, currScope, df
	address = df.generate_memory(currScope, 'int')
	df.set_value_at_address(address, p[-1])
	quad.push_id_type(address, 'int')

def p_push_float(p):
	'''
	push_float			: empty
	'''
	global quad, currScope, df
	address = df.generate_memory(currScope, 'float')
	df.set_value_at_address(address, p[-1])
	quad.push_id_type(address, 'float')

def p_push_bool(p):
	'''
	push_bool			: empty
	'''
	global quad, currScope, df
	address = df.generate_memory(currScope, 'bool')
	df.set_value_at_address(address, p[-1])
	quad.push_id_type(address, 'bool')

def p_push_char(p):
	'''
	push_char			: empty
	'''
	global quad
	address = df.generate_memory(currScope, 'char')
	df.set_value_at_address(address, p[-1])
	quad.push_id_type(address, 'char')

def p_push_string(p):
	'''
	push_string			: empty
	'''
	global quad, strLen, writeStr
	value = p[-1]
	# address = df.generate_memory(currScope, "char")
	# df.set_value_at_address(address, value[0])
	address = 0
	i = 0
	size = len(value)
	first = True
	newSize = size

	while i < size:
		newValue = value[i]
		
		if (value[i] == "\\"):
			# print(f'next : {value[i+1]}')
			if (value[i+1] == "\\"):
				newValue = "\\\\"
			elif (value[i+1] == "n"):
				newValue = "\\n"
			elif (value[i+1] == "t"):
				newValue = "\\t"
			elif (value[i+1] == "\\?"):
				newValue = "\\?"
			elif (value[i+1] == "\'"):
				newValue = "\\\'"
			elif (value[i+1] == "\""):
				newValue = "\\\""
			elif (value[i+1] == "a"):
				newValue = "\\a"
			elif (value[i+1] == "b"):
				newValue = "\\b"
			elif (value[i+1] == "v"):
				newValue = "\\v"
			elif (value[i+1] == "f"):
				newValue = "\\f"
			elif (value[i+1] == "r"):
				newValue = "\\r"
			elif (value[i+1] == "e"):
				newValue = "\\e"
			else:
				newValue = "\\" + value[i+1]
			i += 1
			newSize -= 1
		i += 1
		newAddress = df.generate_memory(currScope, "char")
		df.set_value_at_address(newAddress, newValue)

		if (first):
			address = newAddress
			first = False
			
	quad.push_id_type(address, "char")
	strLen = newSize
	writeStr = True

def p_push_id(p):
	'''
	push_id				: empty
	'''
	global df, currId, currDims, currScope, quad, xDim, yDim
	# print('trying to push id: ', currId)
	address = df.get_var_address(currScope, currId)
	quad.push_id_type(address, df.get_var_type(currScope, currId))

def p_push_equal(p):
	'''
	push_equal			: empty
	'''
	global quad
	quad.push_operator('=')


def p_generate_assign(p):
	'''
	generate_assign		: empty
	'''
	global quad, currScope, df
	# print('trying to assign')
	operator, opLeft, opRight, typeRes = quad.get_ops_type()
	address = df.generate_memory(currScope, typeRes)
	quad.generate(operator, opLeft, opRight, typeRes, address)

def p_generate_g_if(p):
	'''
	generate_g_if		: empty
	'''
	global quad
	quad.generate_g_if()

def p_finish_if(p):
	'''
	finish_if			: empty
	'''
	global quad
	quad.fill_jump(quad.pop_jumps(), quad.get_curr_counter()-1)

def p_generate_g_else(p):
	'''
	generate_g_else		: empty
	'''
	global quad
	quad.generate_g_else()

def p_generate_g_read(p):
	'''
	generate_g_read		: empty
	'''
	global quad
	quad.generate_g_read()

def p_generate_g_write(p):
	'''
	generate_g_write	: empty
	'''
	global quad, writeStr, strLen
	if (writeStr):
		len = strLen
	else:
		len = 1
	quad.generate_g_write(len)
	writeStr = False
	strLen = 1

def p_cloop_push_jump(p):
	'''
	cloop_push_jump		: empty
	'''
	global quad
	quad.push_jump(0)

def p_generate_g_cloop_start(p):
	'''
	generate_g_cloop_start	: empty
	'''
	global quad
	quad.generate_g_cond_loop_s()

def p_generate_g_cloop_end(p):
	'''
	generate_g_cloop_end	: empty
	'''
	global quad
	quad.generate_g_cond_loop_e()

def p_generate_g_nloop_s(p):
	'''
	generate_g_nloop_s	: empty
	'''
	global quad, df, currScope
	operator, opLeft, typeLeft, opRight, typeRes = quad.generate_g_nloop_s_pre()
	address = df.generate_memory(currScope, typeRes)
	quad.generate_g_nloop_s(operator, opLeft, typeLeft, opRight, typeRes, address)

def p_generate_g_nloop_e(p):
	'''
	generate_g_nloop_e	: empty
	'''
	global quad, df, currScope
	end, ret, my, resType = quad.generate_g_nloop_e_pre()
	address_1 = df.generate_memory(currScope, "int")
	address = df.generate_memory(currScope, resType)
	df.set_value_at_address(address_1, 1)
	quad.generate_g_nloop_e(end, ret, my, resType, address, address_1)

def p_generate_end(p):
	'''
	generate_end		: empty
	'''
	global quad
	quad.generate_end()

def p_verify_func(p):
	'''
	verify_func			: empty
	'''
	global currId, df, currFunc
	if (not df.find_function(currId)):
		print(f'Error: function {currId} not defined')
		exit()
	else:
		currFunc = currId

def p_activate_record(p):
	'''
	activate_record		: empty
	'''
	global paramCounter, paramList, argumentList, quad, df, currFunc, currScope, init_address
	i, f, c, b = df.get_resources(currFunc)
	quad.generate_g_era(i, f, c, b)
	paramCounter = 0
	paramList = df.get_params(currFunc)
	argumentList = []
	init_address = df.get_init(currFunc)

def p_verify_params(p):
	'''
	verify_params		: empty
	'''
	global paramCounter, paramList, argumentList, quad, df, currId, typeError
	typeError = False
	argument = quad.pop_operands()
	argumentType = quad.pop_types()
	argumentList.append(argumentType)
	if (argumentType == paramList[paramCounter]):
		quad.generate_g_param(argument, paramCounter)
	else:
		typeError = True

def p_increase_p_count(p):
	'''
	increase_p_count	: empty
	'''
	global paramCounter
	paramCounter += 1

def p_verify_p_num(p):
	'''
	verify_p_num		: empty
	'''
	global paramCounter, paramList, argumentList, init_address, currFunc
	if ((paramCounter + 1) != len(paramList) or typeError):
		print(f"Error: number or type of parameters does not match function {currFunc} definition\n\t\texpected ( " , end="")
		for p in paramList:
			print(f"{p}", end=" ")
		print(") and recieved ( ", end="")
		for a in argumentList:
			print(f"{a}", end=" ")
		print(")")
		exit()
	else:
		quad.generate_g_gosub(currFunc, init_address)

def p_main_goto(p):
	'''
	main_goto			: empty
	'''
	global quad
	quad.generate_main_goto()

def p_fill_main_goto(p):
	'''
	fill_main_goto		: empty
	'''
	global quad, df
	main_init = df.get_init("main")
	quad.fill_jump(0, main_init)


# Empty symbol = ε
def p_empty(p):
	'''
	empty				: 
	'''
	pass

# Error rule for syntax errors
def p_error(p):
	if p is not None:
		print ("Line %s, illegal token %s" % (p.lineno, p.value))
	else:
		print ("Unexpected end of input")
	exit()



parser = yacc.yacc(debug=True)

filename = input("file name: ")

try:
	f = open(filename, 'r')
	data = f.read()
	f.close()
	result = parser.parse(data)
	df.print_memory()
	df.print()
	quad.print()

	# Generate OBJECT (.ovj) file
	with open('object.ovj', 'wb') as handle:
		pickle.dump(
			{
				"quadruples": quad.listOfQuadruples,
				"dirFunc": df.table,
				"memory": df.memory
			}, handle
		)

	print("\n=============================================")
	subprocess.call(['python', 'VirtualMachine.py'])
	print("=============================================\n\n")

	print('File compiled successfully!')
except EOFError:
	print(EOFError)