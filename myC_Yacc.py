import ply.yacc as yacc
from myC_Lex import tokens


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
	vars_1				: ID vars_2 vars_3
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

# Return type for functions
def p_rtype(p):
	'''
	rtype				: INT
						| FLOAT
						| CHAR
						| BOOL
						| VOID
	'''

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
	funcs				: FUNC rtype ID params LCURLY funcs_1 statement funcs_2 RCURLY funcs_3
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
	params_1			: type ID params_2 params_3
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
	assign				: ID assign_1 EQUAL expression SEMICOL
	'''
def p_assign_1(p):
	'''
	assign_1			: dims
						| empty
	'''

def p_dims(p):
	'''
	dims				: LBRACK expression dims_1 RBRACK
	'''
def p_dims_1(p):
	'''
	dims_1				: COMMA expression
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
						| callfunc
						| read
						| write
						| loadfile
	'''

def p_cond(p):
	'''
	cond				: IF LPAR expression RPAR block cond_1
	'''
def p_cond_1(p):
	'''
	cond_1				: ELSE cond_2
	'''
def p_cond_2(p):
	'''
	cond_2				: IF LPAR expression RPAR block cond_3
						| block
	'''
def p_cond_3(p):
	'''
	cond_3				: cond_1
						| empty
	'''

# Conditional loop
def p_cloop(p):
	'''
	cloop				: WHILE LPAR expression RPAR block
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
	callfunc_1			: ID callfunc_2 callfunc_3
						| empty
	'''
def p_callfunc_2(p):
	'''
	callfunc_2			: dims
						| empty
	'''
def p_callfunc_3(p):
	'''
	callfunc_3			: COMMA callfunc_1
						| empty
	'''

def p_read(p):
	'''
	read				: READ LPAR read_1 RPAR SEMICOL
	'''
def p_read_1(p):
	'''
	read_1				: ID read_2 read_3
	'''
def p_read_2(p):
	'''
	read_2				: dims
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
	write_1				: write_2 write_3
	'''
def p_write_2(p):
	'''
	write_2				: expression
						| CTES
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
	expression			: sexp expression_1
	'''
def p_expression_1(p):
	'''
	expression_1		: expression_2 expression
						| empty
	'''
def p_expression_2(p):
	'''
	expression_2		: OR
						| AND
	'''

def p_sexp(p):
	'''
	sexp				: exp sexp_1
	'''
def p_sexp_1(p):
	'''
	sexp_1				: sexp_2 exp
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

def p_exp(p):
	'''
	exp					: term exp_1
	'''
def p_exp_1(p):
	'''
	exp_1				: exp_2 exp
						| empty
	'''
def p_exp_2(p):
	'''
	exp_2				: PLUS
						| MINUS
	'''

def p_term(p):
	'''
	term				: factor term_1
	'''
def p_term_1(p):
	'''
	term_1				: term_2 term
						| empty
	'''
def p_term_2(p):
	'''
	term_2				: TIMES
						| DIV
	'''

def p_factor(p):
	'''
	factor				: factor_1 factor_2
	'''
def p_factor_1(p):
	'''
	factor_1			: ID factor_3
						| callfunc
						| CTEI
						| CTEF
						| CTEB
						| CTEC
						| empty
	'''
def p_factor_2(p):
	'''
	factor_2			: LPAR expression RPAR
						| empty
	'''
def p_factor_3(p):
	'''
	factor_3			: dims
						| empty
	'''

def p_main(p):
	'''
	main				: MAIN LPAR RPAR LCURLY main_1 statement END SEMICOL RCURLY
	'''
def p_main_1(p):
	'''
	main_1				: vars
	'''


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



parser = yacc.yacc()

filename = input("file name: ")

try:
	f = open(filename, 'r')
	data = f.read()
	f.close()
	result = parser.parse(data)
	print('Success!')
except EOFError:
	print(EOFError)