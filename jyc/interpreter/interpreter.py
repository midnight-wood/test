import ply.yacc as yacc
from sqllex import tokens

precedence = (
    ('left', 'and'),
    ('nonassoc', 'OP1', 'OP2', 'OP3', 'OP4', 'OP5', 'OP6')
)

def p_start(p):
    'start : command'
    p[0]=p[1]

def p_command(p):  
    """command : createtable DELIMITER
               | createindex DELIMITER
               | droptable DELIMITER
               | dropindex DELIMITER
               | selectfrom DELIMITER
               | insertinto DELIMITER
               | deletefrom DELIMITER
               | quit DELIMITER"""     
    p[0] = p[1]


def p_ddl_createtable(p):
    """createtable : create table ID \'(\' table_attr \')\'
                   | create table ID \'(\' table_attr \',\' primary_key \')\'"""
    if (len(p)==7):
        p[0]='''
        {
        "command": "createtable",
        "tablename": "'''+p[3]+'''",
        "table_attr": ['''+p[5]+'''],
        "primarykey": NULL
        }'''
    elif (len(p)==9):
        p[0]='''
        {
        "command": "createtable",
        "tablename": "'''+p[3]+'''",
        "table_attr": ['''+p[5]+'''],
        "primarykey": "'''+p[7]+'''"
        }'''

def p_ddl_createindex(p):
    """createindex : create index ID on ID \'(\' ID \')\'"""
    p[0]='''
    {
    "command": "createindex",
    "tablename": "'''+p[5]+'''",
    "colname": "'''+p[7]+'''",
    "indexname": "'''+p[3]+'''"
    }
    '''

def p_ddl_droptable(p):
    """droptable : drop table ID"""
    p[0]='''
    {
    "command": "droptable",
    "tablename": "'''+p[3]+'''"
    }
    '''

def p_ddl_dropindex(p):
    """dropindex : drop index ID"""
    p[0]='''
    {
    "command": "dropindex",
    "indexname": "'''+p[3]+'''"
    }'''

def p_dml_selectfrom(p):
    """selectfrom : select \'*\' from ID
                  | select \'*\' from ID where case"""
    if (len(p)==5):
        p[0]='''
        {
        "command": "select",
        "tablename": "'''+p[4]+'''",
        "case": []
        }'''
    elif (len(p)==7):
        p[0]='''
        {
        "command": "select",
        "tablename": "'''+p[4]+'''",
        "case": ['''+p[6]+''']
        }'''   

def p_dml_insertinto(p):
    """insertinto : insert into ID values \'(\' value \')\'"""
    p[0]='''
    {
    "command": "insert",
    "tablename": "'''+p[3]+'''",
    "values": ['''+p[6]+''']
    }'''

def p_dml_deletefrom(p):
    """deletefrom : delete from ID
                  | delete from ID where case"""
    if (len(p)==4):
        p[0]='''
        {
        "command": "delete",
        "tablename": "'''+p[3]+'''",
        "case": []
        }'''
    elif (len(p)==6):
        p[0]='''
        {
        "command": "delete",
        "tablename": "'''+p[3]+'''",
        "case": ['''+p[5]+''']
        }'''

def p_character(p):
    """character : char \'(\' INTNUMBER \')\'"""
    p[0]='''
    "type": "char",
    "length": '''+str(p[3])+''','''

def p_integer(p):
    """integer : int"""
    p[0]='''
    "type": "int",
    "length": 0,'''

def p_floating(p):
    """floating : float"""
    p[0]='''
    "type": "float",
    "length": 0,'''    

def p_type(p):
    """type : integer
            | floating
            | character"""
    p[0]=p[1]

def p_operation(p):
    """OP : OP1
          | OP2
          | OP3
          | OP4
          | OP5
          | OP6"""
    p[0]=p[1]


def p_string_full(p):
    """STRING_FULL : STRING"""
    p[0]='''
    "type": "string",
    "value": "'''+p[1][1:-1]+'''"
    '''

def p_intnumber_full(p):
    """INTNUMBER_FULL : INTNUMBER"""
    p[0]='''
    "type": "int",
    "value": '''+str(p[1])+'''
    '''    

def p_floatnumber_full(p):
    """FLOATNUMBER_FULL : FLOATNUMBER"""
    p[0]='''
    "type": "float",
    "value": '''+str(p[1])+'''
    '''    

def p_single_value(p):
    """single_value : STRING_FULL
                    | INTNUMBER_FULL
                    | FLOATNUMBER_FULL"""
    p[0]=p[1]

def p_case(p):
    """case : ID OP single_value
            | case and ID OP single_value"""
    if (len(p)==4):
        p[0]='''
        {
        "colname": "'''+p[1]+'''",
        "operation": "'''+p[2]+'''",
        '''+p[3]+'''
        }'''
    elif (len(p)==6):
        p[0]=p[1]+'''
        ,{
        "colname": "'''+p[3]+'''",
        "operation": "'''+p[4]+'''",
        '''+p[5]+'''
        }'''

def p_value(p):
    """value : single_value
             | value \',\' single_value"""
    if (len(p)==2):
        p[0]='''
        {
        '''+p[1]+'''
        }'''
    elif (len(p)==4):
        p[0]=p[1]+''',
        {
        '''+p[3]+'''
        }'''

def p_single_attr(p):
    """single_attr : ID type 
                   | ID type unique"""
    if (len(p)==3):
        p[0]='''
        {
        "name": "'''+p[1]+'''",
        '''+p[2]+'''
        "unique": false
        }'''
    elif (len(p)==4):
        p[0]='''
        {
        "name": "'''+p[1]+'''",
        '''+p[2]+'''
        "unique": true
        }'''        



def p_table_attr(p):
    """table_attr : single_attr 
                  | table_attr \',\' single_attr"""
    if (len(p)==2):
        p[0]=p[1]
    elif (len(p)==4):
        p[0]=p[1]+''','''+p[3]


def p_primary_key(p):
    """primary_key : primary key \'(\' ID \')\'"""
    p[0]=p[4]


def p_error(p):  
    if p:  
        print("Syntax error at '%s'" % p.value)  
    else:  
        print("Syntax error at EOF")  

parser = yacc.yacc() 

data='''
delete from a where b='123' and c='123' and d>123;
'''


res=parser.parse(data)
print(res)