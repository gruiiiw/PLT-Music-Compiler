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

  def parse_note_token(self):
      Token = []
      Token.append(self.cur_char)
      self.advance()
      if self.cur_char.isdigit() and int(self.cur_char) in range(1, 9):
          Token.append(self.cur_char)
          self.advance()
          if self.cur_char in "whqes":
              Token.append(self.cur_char)
              self.tokens.append(("NOTE", ''.join(Token)))  # End of Note Token
              self.advance()
              return True  # Note parsed
      return False  # Note not parsed * maybe print an error message
 
  def run(self):
    while self.cur_char is not None:
      if self.cur_char.isspace():
        self.advance() # might go inside the note loop
        continue 
      if self.cur_char in "ABCDEFG":
        if self.parse_note_token():
          continue
        elif self.cur_char in "abcdefghijklmnopqrstuvwxyz": # then its part of a variable 
          # Variable Token, there can be multiple notes in a variable token. 
          var_token = [self.prev_char]
          while self.cur_char is not None and self.cur_char in "abcdefghijklmnopqrstuvwxyz":
            var_token.append(self.cur_char)
            self.advance()
          self.tokens.append(("VARIABLE", ''.join(var_token)))
          if self.cur_char.isspace():
            self.advance()
          if self.cur_char == "=":
            self.tokens.append(("OPERATOR", "="))
            self.advance()
          if self.cur_char.isspace():
            self.advance()
          if self.cur_char in "ABCDEFG":
            if self.cur_char.isspace():
              self.advance()
              continue
            if self.parse_note_token():
              continue
            self.advance()   
      elif self.cur_char in "HIJKLMNOPQRSTUVWXYZ":
        #This means its a variable token
        self.advance()
      
      elif self.cur_char == 'p': # Play KeywordToken - play ( A4w ) followed by note or iD 
        self.advance()
      
      elif self.cur_char == 't': # 5 Times KeywordToken /Integer
        self.advance()


        
  def get_tokens(self):
    return self.tokens

# Test the lexer
lexer_Dfa = LexerDfa("Aariable= A4w B4h C4q") 
lexer_Dfa.run()
tokens = lexer_Dfa.get_tokens()

for token in tokens:
  print(token)