#####################
### SEMANTIC CUBE ###
#####################

'''
typeResult = TIRESIAS[type1][type2][operator]
'''

TIRESIAS = {
	'int': {
		'int' : {
			'+' : 'int',
			'-' : 'int',
			'*' : 'int',
			'/' : 'float',
			'>' : 'bool',
			'>=' : 'bool',
			'<' : 'bool',
			'<=' : 'bool',
			'==' : 'bool',
			'!=' : 'bool',
			'=' : 'int'
		},
		'float': {
			'+' : 'float',
			'-' : 'float',
			'*' : 'float',
			'/' : 'float',
			'>' : 'bool',
			'>=' : 'bool',
			'<' : 'bool',
			'<=' : 'bool',
			'==' : 'bool',
			'!=' : 'bool',
			'=' : 'int'
		},
		'char': {
			'+' : 'char',
			'-' : 'char',
			'>' : 'bool',
			'>=' : 'bool',
			'<' : 'bool',
			'<=' : 'bool',
			'==' : 'bool',
			'!=' : 'bool',
			'=' : 'int'
		}
	},
	'float': {
		'int' :{
			'+' : 'float',
			'-' : 'float',
			'*' : 'float',
			'/' : 'float',
			'>' : 'bool',
			'>=' : 'bool',
			'<' : 'bool',
			'<=' : 'bool',
			'==' : 'bool',
			'!=' : 'bool',
			'=' : 'float'
		},
		'float': {
			'+' : 'float',
			'-' : 'float',
			'*' : 'float',
			'/' : 'float',
			'>' : 'bool',
			'>=' : 'bool',
			'<' : 'bool',
			'<=' : 'bool',
			'==' : 'bool',
			'!=' : 'bool',
			'=' : 'float'
		}
	},
	'char': {
		'int' :{
			'+' : 'char',
			'-' : 'char',
			'>' : 'bool',
			'>=' : 'bool',
			'<' : 'bool',
			'<=' : 'bool',
			'==' : 'bool',
			'!=' : 'bool',
			'=' : 'char'
		},
		'char': {
			'+' : 'char',
			'-' : 'char',
			'>' : 'bool',
			'>=' : 'bool',
			'<' : 'bool',
			'<=' : 'bool',
			'==' : 'bool',
			'!=' : 'bool',
			'=' : 'char'
		}
	},
	'bool': {
		'int' :{
			'=' : 'bool'
		},
		'bool': {
			'>=' : 'bool',
			'<' : 'bool',
			'<=' : 'bool',
			'==' : 'bool',
			'!=' : 'bool',
			'&&' : 'bool',
			'||' : 'bool',
			'=' : 'bool'
		}
	}
}

'''
Then came also the ghost of Theban >Tiresias<, with his 
golden sceptre in his hand. 'You want to know,' said he, 
'about your return home, but heaven will make this hard
for you. I do not think that you will escape the eye of 
Neptune, who still nurses his bitter grudge against you
for having blinded his son. Still, after much suffering 
you may get home if you can restrain yourself.'
'''