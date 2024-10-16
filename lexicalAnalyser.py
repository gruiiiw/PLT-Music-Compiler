from Parser import Parser
data = "Abcdj = A4w"
data2 = "9 times: { play (A4w) }"

parser = Parser()
lexical_analysis = parser.scan(data)
lexical_analysis2 = parser.scan(data2)

print(lexical_analysis)   
print(lexical_analysis2)


# TODO Provide 5 sample input programs

# TODO Make an execution script that will run the lexical analyzer or provide instructions on how to do soc


