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
					| fun_declaration'''
	p[0] = p[1]

def p_var_declaration(p):
	''' var_declaration : type_specifier ID '''
	p[0] = AST.VariableNode(p[1], p[2])

def p_fun_declaration(p):
	''' fun_declaration : type_specifier ID '(' ')' statement '''
	p[0] = AST.FunctionNode(p[1], p[2], p[5])

def p_statement(p):
	''' statement : expression_stmt
					| compound_stmt
					| return_stmt'''
	p[0] = p[1]

def p_expression_stmt(p):
	''' expression_stmt : expression ';'
						| ';' '''
	p[0] = AST.ExpressionNode(p[1])

def p_compound_stmt(p):
	''' compound_stmt : '{' statement_list '}' '''
	p[0] = AST.CompoundStmtNode(p[2])

def p_return_stmt(p):
	''' return_stmt : RETURN ';'
					| RETURN expression ';' '''
	p[0] = AST.ReturnNode(p[1], p[2])

def p_statement_list(p):
	''' statement_list : statement_list statement '''
	p[0] = AST.StatementListNode(p[1], p[2])

def p_expression(p):
	''' expression : mutable '=' expression
					| simple_expression'''
	p[0] = AST.ExpressionNode(p[1], p[3])

def p_simple_expression(p):
	''' simple_expression : expression SUM_OP expression
							| expression MUL_OP expression'''
	p[0] = AST.ExpressionNode((p[1]),p[3])

def p_mutable(p):
	''' mutable : ID '''
	p[0] = AST.TokenNode(p[1])

def p_type_specifier(p):
	''' type_specifier : VOID
						| INT
						| FLOAT
						| BOOL 
						| CHAR '''
	p[0] = AST.TypeNode(p[1])
	
def p_minus(p):
    ''' statement : SUM_OP statement %prec UMINUS'''
    p[0] = AST.OpNode(p[1], [p[2]])
    	

precedence = (
    ('left', 'SUM_OP'),
    ('left', 'MUL_OP'),
    ('right', 'UMINUS'),  
)




def p_error(p):
	if p:
		print ("Syntax error in line %d" % p.lineno)
		yacc.errok()
	else:
		print ("Sytax error: unexpected end of file!")

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