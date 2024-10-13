import re

# define all Identifiers, Operators, Keywords, Delimiters, And whitespace and add it to the readme, also have it in table
KEYWORD = ["times", "play"]
NUMBERS = [0-9]
IDENTIFIER = ['A-Z']['a-z']*
OPERATORS = ["="]
NOTE = [("A-G")(1-8)("whqes")]
WHITESPACE = ['\n', '\t', ' ']
DELIMITER = [":","(", ")", '{', '}']

# TODO build state machine matrix
def getStateCode(value):
    if re.match(r'[A-G]', value): # we're not allowed to use the regular expression library unfortunately
        return 0
    
    if re.match(r'[1-8]', value):
        return 1
    
    if re.match(r'[whqes]', value):
        return 2
    
    if re.match(r'[\n]', value):
        return 3
    
    if re.match(r'[():{}]', value):
        return 4
    
    if re.match(r'[=]', value):
        return 5
    
    if re.match(r'[A-Za-z]', value):
        return 6
    
    if re.match(r'[tp]', value):
        return 7
    
    if re.match(r'[H-Z]', value):
        return 8
    

# TODO executre scanning algorithm to produce error or lexical tokens

# TODO a. Scan the input programs written in your language and output a list of tokens in the following format: <Token Type, Token Value>.
def scan():
    pass

# TODO handle lexical errors 
def handleErrors():
    pass

# TODO Provide 5 sample input programs

# TODO Make an execution script that will run the lexical analyzer or provide instructions on how to do soc


