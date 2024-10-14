from Parser import Parser
data = "Kbcdj = A4w"
data2 = "9 times"

parser = Parser()
lexical_analysis = parser.scan(data)
lexical_analysis2 = parser.scan(data2)

print(lexical_analysis)   
print(lexical_analysis2)


# TODO executre scanning algorithm to produce error or lexical tokens

# TODO a. Scan the input programs written in your language and output a list of tokens in the following format: <Token Type, Token Value>.
def scan():
    pass

# TODO handle lexical errors 
def handleErrors():
    pass

# TODO Provide 5 sample input programs

# TODO Make an execution script that will run the lexical analyzer or provide instructions on how to do soc


