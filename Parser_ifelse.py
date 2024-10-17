class LexerDfa:
  def __init__(self, input_str):
    self.input_str = input_str
    self.position = 0
    self.cur_char = input_str[self.position] if input_str else None
    self.tokens = []
    self.errors = [] # List of errors, and their defaults 
    self.prev_char = None  

  def advance(self):
    self.prev_char = self.cur_char
    self.position += 1
    if self.position >= len(self.input_str):
      self.cur_char = None
    else:
      self.cur_char = self.input_str[self.position]

  def note_token(self):
      # Handles DFA State for recognizing a note Token
      Token = []
      Token.append(self.cur_char)
      self.advance()
      print("note_token")
      if self.cur_char.isdigit() and int(self.cur_char) in range(1, 9):
          Token.append(self.cur_char)
          self.advance()
          if self.cur_char in "whqes":
              Token.append(self.cur_char)
              self.tokens.append(("NOTE", ''.join(Token)))  # End of Note Token
              self.advance() # maybe leave the advance outside of the def 
              return True  # Note parsed
          else:
            self.errors.append("Error: Invalid note token, missing duration w, h, q, e, s, default as w.")
            Token.append("w")
            self.tokens.append(("NOTE", ''.join(Token)))
            self.advance() # maybe leave the advance outside of the def
            return True  # Note parsed
            # defaults as whole note if no duration is given
      elif self.cur_char == '9':
          self.errors.append(f"Error: Invalid octave number {self.cur_char}, default as octave 4.")
          Token.append("4")
          self.advance()
          print(self.cur_char + "42")
          if self.cur_char in "whqes":
              print("duration_43")
              Token.append(self.cur_char)
              self.tokens.append(("NOTE", ''.join(Token)))
              self.advance()
              return True
          else:
              self.errors.append("Error: Invalid note token, missing duration w, h, q, e, s, default as w.")
              Token.append("w")
              self.tokens.append(("NOTE", ''.join(Token)))
              self.advance()
              return True
      
      elif self.cur_char in "abcdefghijklmnopqrstuvwxyz":
        print("variable")
        return False # its a variable
      elif self.cur_char not in "abcdefghijklmnopqrstuvwxyz":
          Token.append("4")
          self.tokens.append(("NOTE", ''.join(Token)))
          self.errors.append("Error: Invalid note token, missing octave number 1-8, default as octave 4.")
          self.advance() # maybe leave the advance outside of the def
          if self.cur_char in "whqes":
              Token.append(self.cur_char)
              self.tokens.append(("NOTE", ''.join(Token)))
              self.advance()
              return True
              # defaults as octave 4 if no octave is given
      return False  # Note not parsed * maybe print an error message
    
  def variable_token(self): 
    # Handles DFA State for recognizing a Identity Token
    var_token = [self.prev_char]  # Initialize var_token with the previous character
    # you can variable with assignment and variable without assignment 
    while self.cur_char is not None and self.cur_char in "abcdefghijklmnopqrstuvwxyz":
        var_token.append(self.cur_char)
        self.advance()
    self.tokens.append(("IDENTIFIER", ''.join(var_token)))
    if self.cur_char.isspace():
        self.advance()
    if self.cur_char == "=": # then its being assigned to a note split this out
        print("equals")
        self.tokens.append(("OPERATOR", "="))
        self.advance()
        if self.cur_char.isspace():
          self.advance()  
          while self.cur_char is not None and self.cur_char in "ABCDEFG ": # this should be calling note_token i think
              if self.cur_char.isspace():
                  self.advance()
                  continue
              elif self.note_token():
                  print("variable note token")
                  continue
    else:
        return True

  def play_token(self): 
    # Handles DFA State for recognizing a Play Token
    if self.cur_char == "p":
      self.advance()
      if self.cur_char == "l":
        self.advance()
        if self.cur_char == "a":
          self.advance()
          if self.cur_char == "y":
            self.advance()
            self.tokens.append(("Keyword", "play"))
            if self.cur_char == "(":
              print("parenthesis")
              self.advance()
              self.tokens.append(("Delimiter", "("))
              print(self.cur_char) # it will either be variable starting with ABCDEFG variable with H-Z or a note
              
              while self.cur_char is not None:
                if self.cur_char.isspace():
                    self.advance()
                    continue
                elif self.cur_char in "ABCDEFG":  # Notes or variable starting with A-G
                    print("note or variable")
                    if self.note_token():  # Handle note
                        continue
                    elif self.cur_char in "abcdefghijklmnopqrstuvwxyz":  # Variable part
                        print("variable")
                        if self.variable_token():
                            continue
                elif self.cur_char in "HIJKLMNOPQRSTUVWXYZ":  # Variable starting with H-Z
                    print("variable token")
                    self.advance()
                    if self.variable_token():
                        continue
                elif self.cur_char == ")":
                  self.advance()
                  self.tokens.append(("Delimiter", ")"))
                  return True
            else: 
               self.errors.append("Error: Missing ( in play token.")
           
    return False
  
  def times_token(self): 
    # 5times 
    return True
  
  # Ignore white space, but remember for variables, they should be on a new line when declared?
  def run(self):
    while self.cur_char is not None:
      if self.cur_char.isspace():
        self.advance() # might go inside the note loop
        continue 
      while self.cur_char is not None and self.cur_char in "ABCDEFG ": # 
        if self.cur_char.isspace():
            self.advance()
            continue
        elif self.note_token(): # note 
          continue
        elif self.cur_char in "abcdefghijklmnopqrstuvwxyz": # then its part of a variable 
          if self.variable_token():
            continue
        else:
          break

      if self.cur_char is not None and self.cur_char in "HIJKLMNOPQRSTUVWXYZ":  # this part is buggy can't handle Happy then Birthday 
        #This means its a variable token
        self.advance()
        if self.variable_token(): # theres a bug here
          continue
  
      elif self.play_token(): # play token
        continue
      
      elif self.cur_char is not None and self.cur_char.isdigit(): # 5 Times KeywordToken /Integer 5 times { play (A4w) }
        print(f"Found digit: {self.cur_char}")
        self.tokens.append(("INTEGER", self.cur_char))
        self.advance()
        if self.cur_char == "t":
          self.advance()
          if self.cur_char == "i":
            self.advance()
            if self.cur_char == "m":
              self.advance()
              if self.cur_char == "e":
                self.advance()
                if self.cur_char == "s":
                  self.advance()
                  self.tokens.append(("Keyword", "times"))
                  if self.cur_char.isspace():
                    self.advance()
                  if self.cur_char == "{":
                    print("brace")
                    self.advance()
                    self.tokens.append(("Keyword", "{"))
                    if self.cur_char.isspace():
                      # print("space")
                      self.advance()
                    elif self.play_token():
                      print("play token") 
                    if self.cur_char == "}":
                      self.tokens.append(("Keyword", "}")) #
                      print("brace2") 
                      self.advance()
                      # This is an accept state
                # elif found variable:
    
      else:
        return
    return

        
  def get_tokens(self):
    return self.tokens
  def get_errors(self):
    return self.errors

# Test the lexer (5 sample input programs)
print("\n Test 1 \n\n")
# This test shows the errors in the input string, when the note is missing a duration
# Handles invalid octave number 9
lexer_Dfa1 = LexerDfa("""Espresso= A4w B9w C4
                        5times{play(Espresso A4w B3h G4w)}""") 
lexer_Dfa1.run()
tokens_1 = lexer_Dfa1.get_tokens()
errors_1 = lexer_Dfa1.get_errors()

for token in tokens_1:
  print(token)

if errors_1:
    print("Errors encountered:")
    for error in errors_1:
        print(error)

# Output: 
'''
('IDENTIFIER', 'Espresso')
('OPERATOR', '=')
('NOTE', 'A4w')
('NOTE', 'B4w')
('NOTE', 'C4w')
('INTEGER', '5')
('Keyword', 'times')
('Keyword', '{')
('Keyword', 'play')
('Delimiter', '(')
('IDENTIFIER', 'Espresso')
('NOTE', 'A4w')
('NOTE', 'B3h')
('NOTE', 'G4w')
('Delimiter', ')')
('Keyword', '}')
Errors encountered:
Error: Invalid octave number 9, default as octave 4.
Error: Invalid note token, missing duration w, h, q, e, s, default as w.
'''

print("\n\n Test 2 \n\n")
# No errors in this input string (add errors to test)
# Handles -add  lack of brace error 
lexer_DFA2 = LexerDfa("Is = A4w B3h It = B3h That= B3h G7h G4w Sweet= A4w B3h C4w 5times{play(Is It That Sweet)}")
lexer_DFA2.run()
tokens_2 = lexer_DFA2.get_tokens()
errors_2 = lexer_DFA2.get_errors()

for token in tokens_2:
  print(token)

if errors_2:
    print("Errors encountered:")
    for error in errors_2:
        print(error)

# Output:
'''
('IDENTIFIER', 'Is')
('OPERATOR', '=')
('NOTE', 'A4w')
('NOTE', 'B3h')
('IDENTIFIER', 'It')
('OPERATOR', '=')
('NOTE', 'B3h')
('IDENTIFIER', 'That')
('OPERATOR', '=')
('NOTE', 'B3h')
('NOTE', 'G7h')
('NOTE', 'G4w')
('IDENTIFIER', 'Sweet')
('OPERATOR', '=')
('NOTE', 'A4w')
('NOTE', 'B3h')
('NOTE', 'C4w')
('INTEGER', '5')
('Keyword', 'times')
('Keyword', '{')
('Keyword', 'play')
('Delimiter', '(')
('IDENTIFIER', 'Is')
('IDENTIFIER', 'It')
('IDENTIFIER', 'That')
('IDENTIFIER', 'Sweet')
('Delimiter', ')')
('Keyword', '}')
'''

print("\n\n Test 3 \n\n")
# can't handle new lines yet
lexer_DFA3 = LexerDfa("Birthday= A4w A4h B4w A4w D4h To = A4w A4h B4w A4w You = D4w 5times { play(Birthday To You) }")
lexer_DFA3.run()
tokens_3 = lexer_DFA3.get_tokens()

for token in tokens_3:
  print(token)

print("\n\n Test 4 \n\n")
# Tests playing before and after the Identifier assignment
lexer_DFA4 = LexerDfa("play(A4w B3h G4w C4w D4w) Someone= D3h To= A4w B3h G4w C4w D4w Love= F3q play(Someone To Love)")
lexer_DFA4.run()
tokens_4 = lexer_DFA4.get_tokens()
errors_4 = lexer_DFA4.get_errors()

for token in tokens_4:
  print(token)

if errors_4:
    print("Errors encountered:")
    for error in errors_4:
        print(error)

# Output:
'''
('Keyword', 'play')
('Delimiter', '(')
('NOTE', 'A4w')
('NOTE', 'B3h')
('NOTE', 'G4w')
('NOTE', 'C4w')
('NOTE', 'D4w')
('Delimiter', ')')
('IDENTIFIER', 'Someone')
('OPERATOR', '=')
('NOTE', 'D3h')
('IDENTIFIER', 'To')
('OPERATOR', '=')
('NOTE', 'A4w')
('NOTE', 'B3h')
('NOTE', 'G4w')
('NOTE', 'C4w')
('NOTE', 'D4w')
('IDENTIFIER', 'Love')
('OPERATOR', '=')
('NOTE', 'F3q')
('Keyword', 'play')
('Delimiter', '(')
('IDENTIFIER', 'Someone')
('IDENTIFIER', 'To')
('IDENTIFIER', 'Love')
('Delimiter', ')')
'''

print("\n\n Test 5 \n\n")

lexer_DFA5 = LexerDfa("")
lexer_DFA5.run()
tokens_5 = lexer_DFA5.get_tokens()
errors_5 = lexer_DFA5.get_errors()

for token in tokens_5:
  print(token)

if errors_5:
    print("Errors encountered:")
    for error in errors_5:
        print(error)

# Output:

'''

'''