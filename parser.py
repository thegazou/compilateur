import ply.yacc as yacc

from lex import tokens
import AST

from collections import defaultdict
vars = defaultdict(list)

def p_programme_statement(p):
    ''' programme : statement '''
    p[0] = AST.ProgramNode(p[1])

def p_programme_recursive(p):
    ''' programme : statement ';' programme '''
    p[0] = AST.ProgramNode([p[1]]+p[3].children)

def p_statement(p):
    ''' statement : declaration
        | assignation
        | structure '''
    p[0] = p[1]
    	
def p_statement_print(p):
    ''' statement : PRINT expression '''
    p[0] = AST.PrintNode(p[2])

def p_structure(p):
    ''' structure : WHILE expression '{' programme '}' '''
    p[0] = AST.WhileNode([p[2],p[4]])

def p_expression_op(p):
    '''expression : expression ADD_OP expression
            | expression MUL_OP expression'''
    p[0] = AST.OpNode(p[2], [p[1], p[3]])

def p_expression_num_or_var(p):
    '''expression : NUMBER_INT
        | NUMBER_FLOAT
        | IDENTIFIER '''
    p[0] = AST.TokenNode(p[1])
    	
def p_expression_paren(p):
    '''expression : '(' expression ')' '''
    p[0] = p[2]
    	
def p_minus(p):
    ''' expression : ADD_OP expression %prec UMINUS'''
    p[0] = AST.OpNode(p[1], [p[2]])

def p_declaration(p):
    ''' declaration : type declaration_init '''

    try:
        #used if it's a assignement
        vars[p[2].children[0].tok].append(p[1].tok)

    except:
        #used if it's a tokenNod
        vars[p[2].tok].append(p[1].tok)
        vars[p[2].tok].append(None)
        vars[p[2].tok].append(False)
    p[0] = AST.DeclarationNode([p[1],p[2]])

def p_delaration_init(p):
    ''' declaration_init : expression
        | assignation '''
    p[0] = p[1]

def p_type(p):
    '''type : FLOAT
        | INT'''
    p[0]=AST.TypeNode(p[1])

def p_assign(p):
    ''' assignation : IDENTIFIER '=' expression '''
    p[0] = AST.AssignNode([AST.TokenNode(p[1]),p[3]])

def p_error(p):
    if p:
        print ("Syntax error in line %d" % p.lineno)
        'yacc.errok()'
    else:
        print ("Syntax error: unexpected end of file!")


precedence = (
    ('left', 'ADD_OP'),
    ('left', 'MUL_OP'),
    ('right', 'UMINUS'),  
)

def parse(program):
    result=[]
    result.append(yacc.parse(program))
    result.append(vars)
    return result

yacc.yacc(outputdir='generated')

if __name__ == "__main__":
    import sys 
    	
    prog = open(sys.argv[1]).read()
    result=[]
    result.append(yacc.parse(prog))
    result.append(vars)
    if result:
        print (result[0])
            
        '''import os
        graph = result.makegraphicaltree()
        name = os.path.splitext(sys.argv[1])[0]+'-ast.pdf'
        graph.write_pdf(name) 
        print ("wrote ast to", name)'''
    else:
        print ("Parsing returned no result!")