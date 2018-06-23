import ply.lex as lex


reserved={
	'create':'create',
	'table':'table',
	'int':'int','float':'float','char':'char',
	'unique':'unique','primary':'primary','key':'key',
	'index':'index',
	'drop':'drop',
	'on':'on',
	'select':'select','from':'from','where':'where',
	'and':'and','or':'or',
	'insert':'insert','into':'into','values':'values',
	'delete':'delete','quit':'quit'}

# reserved=(
# 	'create',
# 	'table',
# 	'int','float','char',
# 	'unique','primary','key',
# 	'index',
# 	'drop',
# 	'on',
# 	'select','from','where',
# 	'and','or',
# 	'insert','into','values',
# 	'delete','quit')

tokens=['OP1','OP2','OP3','OP4','OP5','OP6',
	'STRING','INTNUMBER','FLOATNUMBER',
	'DELIMITER','ID']+list(reserved.values())

# print(tokens)

literals=['(',')',',','*']


t_DELIMITER=r';'



t_OP1=r'='
t_OP2=r'<>'
t_OP3=r'<'
t_OP4=r'>'
t_OP5=r'<='
t_OP6=r'>='



def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type=reserved.get(t.value,'ID')
    return t

def t_FLOATNUMBER(t):
    r'[0-9]*[\.][0-9]*'
    t.value=float(t.value)
    return t



def t_INTNUMBER(t):
    r'[1-9][0-9]*'
    t.value=int(t.value)
    return t


def t_STRING(t):
    r"\'[^']*\'"
    return t

t_ignore  = ' \t\n'


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


lexer = lex.lex()

data="delete from a where b='123' and c='123' and d>123;"




lexer.input(data)

while True:
    tok = lexer.token()
    if not tok: 
        break     
    print(tok)

