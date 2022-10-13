'''
Grammar for the SOYUZ Programming Language
Created by Juan Pablo González 2022(C)
Created for the Compiler Design Course
'''

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

quad = QuadrupleTable()

# Start of program
def p_program_start(p):
	'''
	program_start		: PROGRAM ID SEMICOL program_start_1 program_start_2 main
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
	vars_2				: dims
						| empty
	'''
def p_vars_3(p):
	'''
	vars_3				: COMMA vars_1
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
	funcs				: FUNC rtype ID see_id see_func_start params LCURLY funcs_1 statement funcs_2 see_func_end RCURLY funcs_3
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
	assign				: ID see_id assign_1 push_id EQUAL push_equal expression generate_assign SEMICOL
	'''
def p_assign_1(p):
	'''
	assign_1			: dims
						| empty
	'''

def p_dims(p):
	'''
	dims				: LBRACK expression see_dims dims_1 RBRACK
	'''
def p_dims_1(p):
	'''
	dims_1				: COMMA expression see_dims
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
						| callfunc SEMICOL
						| read
						| write
						| loadfile
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
	nloop				: FROM ID nloop_1 nloop_2 TO expression block
	'''
def p_nloop_1(p):
	'''
	nloop_1				: dims
						| empty
	'''
def p_nloop_2(p):
	'''
	nloop_2				: EQUAL expression
						| empty
	'''

def p_callfunc(p):
	'''
	callfunc			: ID LPAR callfunc_1 RPAR
	'''
def p_callfunc_1(p):
	'''
	callfunc_1			: expression callfunc_3
						| empty
	'''
# def p_callfunc_2(p):
# 	'''
# 	callfunc_2			: dims
# 						| empty
# 	'''
def p_callfunc_3(p):
	'''
	callfunc_3			: COMMA callfunc_1
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
	factor_1			: ID see_id factor_3 push_id print_value reset_dims
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
	main				: MAIN see_id LPAR RPAR LCURLY see_func_start main_1 statement END SEMICOL RCURLY see_func_end
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
	global currDims
	currDims = currDims + 1

def p_push_var(p):
	'''
	push_var			: empty
	'''
	global currId, currType, currDims, currScope, vAtts, df
	# print("Variable added:", currId, "\ttype:", currType, "\tdims:", currDims, "\tscope: ", currScope)
	df.addVar(currScope, vAtts.createVar(currId, currType, currDims, None))
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
	currScope = currScope + 1
	df.addFunction(currScope, currId, currReturnType)

def p_see_func_end(p):
	'''
	see_func_end		: empty
	'''
	global currScope, df
	# df.printFunc()
	df.removeFunction(currScope)
	currScope = currScope - 1

def p_see_end_param(p):
	'''
	see_end_param		: empty
	'''
	global currScope, currId, currDims, df, vAtts
	df.addParam(currScope, vAtts.createVar(currId, currType, currDims, None))

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
	global quad
	if (quad.top_operators() == '&&' or quad.top_operators() == '||'):
		quad.generate()

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
	global quad
	# print('checking relational... ', quad.top_operators())
	rel = ['==', '!=', '>', '>=', '<', '<=',]
	if (quad.top_operators() in rel):
		# print('generating relational...')
		quad.generate()

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
	global quad
	# print('checking sum...', quad.top_operators())
	if (quad.top_operators() == '+' or quad.top_operators() == '-'):
		quad.generate()

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
	global quad
	# print('checking mul/div... ', quad.top_operators())
	if (quad.top_operators() == '*' or quad.top_operators() == '/'):
		quad.generate()

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
	global quad
	quad.push_id_type(p[-1], 'int')

def p_push_float(p):
	'''
	push_float			: empty
	'''
	global quad
	quad.push_id_type(p[-1], 'float')

def p_push_bool(p):
	'''
	push_bool			: empty
	'''
	global quad
	quad.push_id_type(p[-1], 'bool')

def p_push_char(p):
	'''
	push_char			: empty
	'''
	global quad
	quad.push_id_type(p[-1], 'char')

def p_push_string(p):
	'''
	push_string			: empty
	'''
	global quad
	quad.push_id_type(f'{p[-1]}', 'string')

def p_push_id(p):
	'''
	push_id				: empty
	'''
	global df, currId, currDims, currScope, quad
	# print('trying to push id: ', currId)
	quad.push_id_type(currId, df.getVarType(currScope, currId))

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
	global quad
	# print('trying to assign')
	quad.generate()

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
	global quad
	quad.generate_g_write()

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
	quad.print()
	print('File compiled successfully!')
except EOFError:
	print(EOFError)