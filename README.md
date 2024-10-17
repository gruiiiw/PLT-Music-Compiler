# PLT-Music-Compiler
Music Compiler

## Lexical Grammar
Define the lexical grammar for your language, ensuring each token and its rules are
documented in a README file. Design the lexical grammar that has at least 5 different
token types.

KEYWORD = ["times", "play"] <br>
NUMBERS = [0-9] <br>
IDENTIFIER = ['A-Z']['a-z']* <br>
    Examples: Happy, Birthday, Variable
OPERATORS = ["="] <br>
NOTE = [("A-G")(1-8)("w|h|q|e|s")] <br>
    Examples: 
WHITESPACE = ['\n', '\t',] <br>
DELIMITER = ["(", ")", '{', '}'] <br>

Example Program: <br>
    Variable_name= A4w C2h B43  <br>
    2times {play ( variable_name A4w )}  <br>

Rules:  <br>

## Shell Script to Execute Lexer
Installation Steps <br>

** Do not assume anything. We could be running it on a system without python. The easiest way to sort out this requirement would be to add a Dockerfile with all the build steps, that can be run on any system.


## Steps
Please refer to our DFA image for steps of the Lexer. <br>
![DFA Image](dfa_image.png)
add DFA here

1. When parsing the string from the start*  


## Team
Grace Dong grd2120 <br>
Ben Cyna bc3096 



