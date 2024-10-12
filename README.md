# PLT-Music-Compiler
Music Compiler

## Lexical Grammar
Define the lexical grammar for your language, ensuring each token and its rules are
documented in a README file. Design the lexical grammar that has at least 5 different
token types.


# Regular Expresions for Lexical Grammer
KEYWORD = ["times", "play"]
NUMBERS = [0-9]
IDENTIFIER = ['A-Z']['a-z']*
OPERATORS = ["="]
NOTE = [("A-G")(1-8)("whqes")]
WHITESPACE = ['\n', '\t', ' ']
DELIMITER = [":","(", ")", '{', '}']


Happy = [A-Z][a-z]* - Identifier


## Shell Script to Execute Lexer
Installation Steps <br>

** Do not assume anything. We could be running it on a system without python. The easiest way to sort out this requirement would be to add a Dockerfile with all the build steps, that can be run on any system.


## Steps
- 

## Team
Grace Dong grd2120 <br>
Ben Cyna bc3096 



