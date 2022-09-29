#####################
### SEMANTIC CUBE ###
#####################

'''
typeResult = SEMANTIC[type1][type2][operator]
'''

SEMANTIC = {
	"int": {
		"int" :{
			"+" : "int",
			"-" : "int",
			"*" : "int",
			"/" : "float",
			">" : "bool",
			">=" : "bool",
			"<" : "bool",
			"<=" : "bool",
			"==" : "bool",
			"!=" : "bool",
			"=" : "int"
		},
		"float": {
			"+" : "float",
			"-" : "float",
			"*" : "float",
			"/" : "float",
			">" : "bool",
			">=" : "bool",
			"<" : "bool",
			"<=" : "bool",
			"==" : "bool",
			"!=" : "bool",
			"=" : "int"
		},
		"char": {
			"+" : "char",
			"-" : "char",
			">" : "bool",
			">=" : "bool",
			"<" : "bool",
			"<=" : "bool",
			"==" : "bool",
			"!=" : "bool",
			"=" : "int"
		}
	},
	"float": {
		"int" :{
			"+" : "float",
			"-" : "float",
			"*" : "float",
			"/" : "float",
			">" : "bool",
			">=" : "bool",
			"<" : "bool",
			"<=" : "bool",
			"==" : "bool",
			"!=" : "bool",
			"=" : "float"
		},
		"float": {
			"+" : "float",
			"-" : "float",
			"*" : "float",
			"/" : "float",
			">" : "bool",
			">=" : "bool",
			"<" : "bool",
			"<=" : "bool",
			"==" : "bool",
			"!=" : "bool",
			"=" : "float"
		}
	},
	"char": {
		"int" :{
			"+" : "char",
			"-" : "char",
			">" : "bool",
			">=" : "bool",
			"<" : "bool",
			"<=" : "bool",
			"==" : "bool",
			"!=" : "bool",
			"=" : "char"
		},
		"char": {
			"+" : "char",
			"-" : "char",
			">" : "bool",
			">=" : "bool",
			"<" : "bool",
			"<=" : "bool",
			"==" : "bool",
			"!=" : "bool",
			"=" : "char"
		}
	},
	"bool": {
		"int" :{
			"=" : "bool"
		},
		"bool": {
			">=" : "bool",
			"<" : "bool",
			"<=" : "bool",
			"==" : "bool",
			"!=" : "bool",
			"&&" : "bool",
			"||" : "bool",
			"=" : "bool"
		}
	}
}

