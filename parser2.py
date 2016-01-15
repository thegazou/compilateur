import ply.yacc as yacc

from lex import tokens
import AST

vars = {}

def p_program(p):
	''' program : declaration_list '''
	p[0] = AST.ProgramNode(p[1])

def p_declaration_list(p):
	''' declaration_list : declaration_list declaration 
							| declaration '''
	p[0] = AST.DeclarationNode(p[1], p[2])

def p_declaration(p):
	''' declaration : var_declaration  
					| fun_declaration '''
	p[0] = AST.DeclarationNode(p[1])

def p_var_declaration(p):
	''' var_declaration : type_specifier var_decl_list  '''
   #p[0] = AST.ProgramNode(p[1])

def p_scoped_var_declaration(p):
	''' scoped_var_declaration : scoped_type_specifier var_decl_list '''
   #p[0] = AST.ProgramNode(p[1])

def p_var_decl_list(p):
	''' var_decl_list : var_decl_list ',' var_decl_initialize 
						| var_decl_initialize '''
   #p[0] = AST.ProgramNode(p[1])

def p_var_decl_initialize(p):
	''' var_decl_initialize : var_decl_id 
							| var_decl_id ':' simple_expression '''
   #p[0] = AST.ProgramNode(p[1])

def p_var_decl_id(p):
	''' var_decl_id : ID 
					| ID '[' NUMBER ']' '''
	p[0] = AST.TokenNode(p[1], AST.TokenNode(p[3]))

def p_scoped_type_specifier(p):
	''' scoped_type_specifier :  type_specifier '''
#	p[0] = p[1]

def p_type_specifier(p):
	''' type_specifier : int 
						| float
						| bool 
						| char '''
   #p[0] = AST.ProgramNode(p[1])

def p_fun_declaration(p):
	''' fun_declaration : type_specifier ID '(' params ')' statement 
						| ID '(' params ')' statement '''
   #p[0] = AST.ProgramNode(p[1])

def p_params(p):
	''' params : param_list 
				|  '''
	p[0] = p[1]

def p_param_list(p):
	''' param_list : param_list ';' param_type_list 
					| param_type_list '''
   #p[0] = AST.ProgramNode(p[1])

def p_param_type_list(p):
	''' param_type_list : type_specifier param_id_list '''
#	p[0] = AST.ProgramNode(p[1])

def p_param_id_list(p):
	''' param_id_list : param_id_list ',' param_id 
						| param_id '''
   #p[0] = AST.ProgramNode(p[1])

def p_param_id(p):
	''' param_id : ID 
					| ID '[' ']' '''
	p[0] = AST.TokenNode(p[1])

def p_statement(p):
	''' statement : expression_stmt 
					| compound_stmt 
					| selection_stmt 
					| iteration_stmt 
					| return_stmt 
					| break_stmt '''
   #p[0] = AST.ProgramNode(p[1])

def p_compound_stmt(p):
	''' compound_stmt : '{' local_declarations statement_list '}' '''
   #p[0] = AST.ProgramNode(p[1])

def p_local_declarations(p):
	''' local_declarations : local_declarations scoped_var_declaration 
							|  '''
   #p[0] = AST.ProgramNode(p[1])

def p_statement_list(p):
	''' statement_list : statement_list statement 
						|  '''
   #p[0] = AST.ProgramNode(p[1])

def p_expression_stmt (p):
	''' expression_stmt  : expression ';' 
							| ';' '''
   #p[0] = AST.ProgramNode(p[1])

def p_selection_stmt (p):
	''' selection_stmt  : if '(' simple_expression ')' statement 
						| if '(' simple_expression ')' statement else statement '''
   #p[0] = AST.ProgramNode(p[1])

def p_iteration_stmt (p):
	''' iteration_stmt  : while '(' simple_expression ')' statement 
						| foreach '(' mutable in simple_expression ')' statement '''
#	p[0] = AST.ProgramNode(p[1])

def p_return_stmt (p):
	''' return_stmt  : return ';' 
						| return expression ';' '''
#	p[0] = AST.ProgramNode(p[1])

def p_break_stmt (p):
	''' break_stmt  : break ';' '''
   #p[0] = AST.ProgramNode(p[1])

def p_expression (p):
	''' expression  :  '''
   #p[0] = AST.ProgramNode(p[1])

def p_simple_expression (p):
	''' simple_expression : simple_expression 
							| and_expression '''
	p[0] = p[1]

def p_and_expression (p):
	''' and_expression  : and_expression '&' unary_rel_expression 
						| unary_rel_expression '''
   #p[0] = AST.ProgramNode(p[1])

def p_unary_rel_expression (p):
	''' unary_rel_expression  : '!' unary_rel_expression 
								| rel_expression '''
   #p[0] = AST.ProgramNode(p[1])

def p_rel_expression (p):
	''' rel_expression  : sum_expression relop sum_expression 
						| sum_expression '''
   #p[0] = AST.ProgramNode(p[1])

def p_relop (p):
	''' relop  : '''
#	p[0] = p[1]

def p_sum_expression (p):
	''' sum_expression  : sum_expression sumop term 
						| term '''
   #p[0] = AST.ProgramNode(p[1])

def p_sumop (p):
	''' sumop  : '+' 
				| '-' '''
	p[0] = p[1]

def p_term (p):
	''' term  : term mulop unary_expression 
				| unary_expression '''
   #p[0] = AST.ProgramNode(p[1])

def p_mulop (p):
	''' mulop  : '*' 
				| '/' 
				| '%' '''
	p[0] = p[1]

def p_unary_expression (p):
	''' unary_expression  : unaryop unary_expression 
							| factor '''
	p[0] = p[1]

def p_unaryop (p):
	''' unaryop  : '-' 
					| '*' 
					| '?' '''
	p[0] = p[1]

def p_factor (p):
	''' factor  : immutable 
				| mutable '''
	p[0] = p[1]

def p_mutable (p):
	''' mutable  : ID 
					| ID '[' expression ']' '''
   #p[0] = AST.ProgramNode(p[1])

def p_immutable (p):
	''' immutable  : '(' expression ')' 
					| call 
					| constant '''
   #p[0] = AST.ProgramNode(p[1])

def p_call (p):
	''' call  : ID '(' args ')' '''
   #p[0] = AST.ProgramNode(p[1])

def p_args (p):
	''' args  : arg_list 
				|  '''
	p[0] = p[1]

def p_arg_list (p):
	''' arg_list  : arg_list ',' expression 
					| expression '''
   #p[0] = AST.ProgramNode(p[1])

def p_constant (p):
	''' constant  : ID 
					| true 
					| false '''
	p[0] = p[1]

precedence = (
    ('left', 'ADD_OP'),
    ('left', 'MUL_OP'),
 #   ('right', 'UMINUS'),  
)

def parse(program):
	return yacc.parse(program)

yacc.yacc(outputdir='generated')

if __name__ == "__main__":
	import sys 
    	
	prog = open(sys.argv[1]).read()
	result = yacc.parse(prog)
	if result:
		print (result)
            
		import os
		graph = result.makegraphicaltree()
		name = os.path.splitext(sys.argv[1])[0]+'-ast.pdf'
		graph.write_pdf(name) 
		print ("wrote ast to", name)
	else:
		print ("Parsing returned no result!")