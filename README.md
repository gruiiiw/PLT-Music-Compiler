# PLT-Music-Compiler
Music Compiler

## Lexical Grammar
Our program ignores whitespace. 

KEYWORD= ["times", "play"] <br>

Rules: <br>
"times" has to follow an integer. <br> 
"times" has to be followed by an open bracket "{" <br> 
"play" has to be followed by an open parenthesis "(" <br>


<br>
NUMBERS = [0-9] <br>
Rules: <br>
A number can appear before times as first token. <br>
A number can be part of a note. It must follow a letter (note key) [A-G] and precede a length key (w|h|q|e|s) <br>

<br>
IDENTIFIER = ['A-Z']['a-z']* <br>
    Examples: Happy, Birthday, Variable <br>
Rules: <br>
A variable can be defined as a single captial letter [A-Z] followed by any length string of [a-z] chars. <br>
An identifier must precede an '=' sign <br>


<br>
OPERATORS = ["="] <br>
Rules: <br>
An equals sign must follow an identifier and be followed by a NOTE token. 
<br>
<br>

NOTE = [("A-G")(1-8)("w|h|q|e|s")] <br>
Examples: A4w, B3h, G4w, C4w, D4w. <br>
Rules:
A note can be defined after an '=' char <br>
A note can be defined after an open parenthesis '(' <br>
<br>


DELIMITER = ["(", ")", '{', '}'] <br>
Rules: <br>
'(' follows "play" keyword and must have a enclosing '). <br>
'{' follows "times" keyword and must have enclosing '}' <br>


Example Program: <br>
    Variable_name= A4w C2h B43  <br>
    2times {play ( variable_name )}  <br>

<br>
## Shell Script to Execute Lexer
Installation Steps <br>

## Tests


## Usage  
Make sure you have python3 installed. You can install it from here https://www.python.org/downloads/
### Option 1, Our own test cases
Now make sure to set the permission for the .sh files. You can use these two commands. 
``` chmod +x run_scanner.sh ```
``` chmod +x run_tests.sh ```
<br>
The provided test cases above are also built into our code. You can run these test cases using the following command. <br> 

``` ./run_tests.sh ``` 

### Option 1, Scan input from the command line
You can enter your own input into the system using the command, replacing the 0 with a 1 <br>
``` ./run_scanner.sh ``` 
When you are done entering your own input, to send the EOF, press control + d on mac or ctrl + z on windows. 


## Steps
Please refer to our DFA image for steps of the Lexer. <br>
![DFA Image](dfa_image.png)


## Team
Grace Dong grd2120 <br>
Ben Cyna bc3096 <br>



