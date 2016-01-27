import AST
from AST import addToClass
from functools import reduce
operations = {
    '+' : lambda x,y: x+y,
    '-' : lambda x,y: x-y,
    '*' : lambda x,y: x*y,
    '/' : lambda x,y: x/y,
}

@addToClass(AST.ProgramNode)
def execute(self):
    for c in self.children:
        c.execute()
    
@addToClass(AST.TokenNode)
def execute(self):
    if isinstance(self.tok, str):
        try:
            if vars[self.tok][0] is None:
                print("*** warning: variable %s has no type!" % self.tok)
        except IndexError:
            print("*** warning: variable %s is unknown!" % self.tok)
            return "error"
        vars[self.tok][2] = True
        if vars[self.tok][1] is None:
            print("*** warning: variable %s has not been set!" % self.tok)
            vars[self.tok][1] = 0
            vars[self.tok][2] = False
        return vars[self.tok][1]
    return self.tok

@addToClass(AST.OpNode)
def execute(self):
    args = [c.execute() for c in self.children]

    # TODO test si l'operation est faite avec des variables de meme type
    if len(args) == 1:
        args.insert(0,0)
    return reduce(operations[self.op], args)

@addToClass(AST.AssignNode)
def execute(self):
    #test si la variable a ete declaree.
    if len(vars[self.children[0].tok])==1:
        vars[self.children[0].tok].append(self.children[1].execute())
        vars[self.children[0].tok].append(False)
    else:
        vars[self.children[0].tok].append(None) #permet a l'interpreteur de verifier si la variable a ete declaree.
        vars[self.children[0].tok].append(self.children[1].execute())
        vars[self.children[0].tok].append(False)



@addToClass(AST.PrintNode)
def execute(self):
    print (self.children[0].execute())
    
@addToClass(AST.WhileNode)
def execute(self):
    while self.children[0].execute():
        self.children[1].execute()

@addToClass(AST.DeclarationNode)
def execute(self):
    self.children[1].execute()

if __name__ == "__main__":
    from compilateur.parser import parse
    import sys
    prog = open(sys.argv[1]).read()
    parser = parse(prog)
    ast = parser[0]
    vars = parser[1]
    ast.execute()
    print()
    print("check if every variable have been used...")
    used = True
    for key, value in vars.items():
        try:
            if(value[2]==False):
                used=False
                print("%s has not been used" % key)
        except IndexError:
            break
    if used == True:
        print("All variable have been used.")