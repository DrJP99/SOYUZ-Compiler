# Main file for compiler

from myC_Yacc import start_parse
import sys

if __name__ == '__main__':
	n = len(sys.argv)
	start_parse(sys.argv[1] if n >= 2 else '')