class LexerDfa:
  def __init__(self, input_str):
    self.input_str = input_str
    self.position = 0
    self.cur_char = input_str[self.position] if input_str else None
    self.tokens = []
    self.prev_char = None  


  def advance(self):
    self.prev_char = self.cur_char
    self.position += 1
    if self.position >= len(self.input_str):
      self.cur_char = None
    else:
      self.cur_char = self.input_str[self.position]

  def note_token(self):
      Token = []
      Token.append(self.cur_char)
      self.advance()
      if self.cur_char.isdigit() and int(self.cur_char) in range(1, 9):
          Token.append(self.cur_char)
          self.advance()
          if self.cur_char in "whqes":
              Token.append(self.cur_char)
              self.tokens.append(("NOTE", ''.join(Token)))  # End of Note Token
              self.advance() # maybe leave the advance outside of the def
              return True  # Note parsed
      return False  # Note not parsed * maybe print an error message
    
  def variable_token(self):
    var_token = [self.prev_char]  # Initialize var_token with the previous character
    # you can variable with assignment and variable without assignment 
    while self.cur_char is not None and self.cur_char in "abcdefghijklmnopqrstuvwxyz":
        var_token.append(self.cur_char)
        self.advance()
    self.tokens.append(("IDENTIFIER", ''.join(var_token)))
    if self.cur_char.isspace():
        self.advance()
    if self.cur_char == "=":
        self.tokens.append(("OPERATOR", "="))
        self.advance()
    if self.cur_char.isspace():
        self.advance()
    while self.cur_char is not None and self.cur_char in "ABCDEFG": # this should be calling note_token i think
        if self.cur_char.isspace():
            self.advance()
            continue
        if self.note_token():
            continue
        self.advance() # maybe leave the advance outside of the def

 
  def run(self):
    while self.cur_char is not None:
      if self.cur_char.isspace():
        self.advance() # might go inside the note loop
        continue 
      while self.cur_char is not None and self.cur_char in "ABCDEFG": # 
        if self.cur_char.isspace():
            self.advance()
            continue
        if self.note_token(): # note 
          continue
        elif self.cur_char in "abcdefghijklmnopqrstuvwxyz": # then its part of a variable 
          if self.variable_token():
            continue

      if self.cur_char in "HIJKLMNOPQRSTUVWXYZ": 
        #This means its a variable token
        self.advance()
        if self.cur_char in "abcdefghijklmnopqrstuvwxyz": # then its part of a variable 
          if self.variable_token(): # theres a bug here
            continue
    
      elif self.cur_char == 'p': # Play KeywordToken - play ( A4w ) followed by note or iD 
        self.advance()
        if self.cur_char == "l":
          self.advance()
          if self.cur_char == "a":
            self.advance()
            if self.cur_char == "y":
              self.advance()
              if self.cur_char == "(":
                self.advance()
                if self.cur_char in "ABCDEFG":
                  if self.note_token(): # note add variable 
                    continue
                  self.advance()
                if self.cur_char == ")": 
                  self.advance()
                  self.tokens.append(("Keyword", "play"))
                  continue
      
      elif self.cur_char.isdigit(): # 5 Times KeywordToken /Integer 5 times { play (A4w) }
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
                    # print("brace")
                    self.advance()
                    self.tokens.append(("Keyword", "{"))
                    if self.cur_char.isspace():
                      self.advance()
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
                              self.advance()
                              self.tokens.append(("Delimiter", "(")) # if found two in a row, can print ignored error?
                              if self.cur_char in "ABCDEFG": # Found note 
                                if self.note_token():
                                  print("note")
                                
                                if self.cur_char == ")": 
                                  self.advance()
                                  self.tokens.append(("Delimiter", ")"))
                                  if self.cur_char == "}":
                                    self.advance()
                                    self.tokens.append(("Keyword", "}")) # 
                                    continue # This is an accept state
                              # elif found variable:


        
  def get_tokens(self):
    return self.tokens

# Test the lexer (5 sample input programs)
lexer_Dfa1 = LexerDfa("""Variable= A4w B3h C3q
                        5times{play(A4w)}""")  # B3h is being stopped, can't play more than 1 note rn
lexer_Dfa1.run()
tokens_1 = lexer_Dfa1.get_tokens()

for token in tokens_1:
  print(token)

lexer_DFA2 = LexerDfa("""Happy= A4w
                         Birthday= B3h""")
lexer_DFA2.run()
tokens_2 = lexer_DFA2.get_tokens()

for token in tokens_2:
  print(token)
