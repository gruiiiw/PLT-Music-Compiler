import sys

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
      while self.cur_char == '\n':
          self.position += 1
          if self.position >= len(self.input_str):
              self.cur_char = None
              break
          self.cur_char = self.input_str[self.position]

  def note_token(self):
      # Handles DFA State for recognizing a note Token
      Token = []
      Token.append(self.cur_char)
      self.advance()
      if self.cur_char.isdigit() and int(self.cur_char) in range(1, 9):
          #print(self.cur_char + "_22") 
          Token.append(self.cur_char)
          self.advance()
          if self.cur_char in "whqes":
              Token.append(self.cur_char)
              self.tokens.append(("NOTE", ''.join(Token)))  # End of Note Token
              self.advance() # maybe leave the advance outside of the def 
              # print("note_token_31")
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
          # print(self.cur_char + "42")
          if self.cur_char in "whqes":
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
        if self.variable_token():
            return True
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
    if self.cur_char is not None and self.cur_char.isspace():
        self.advance()
    if self.cur_char == "=": # then its being assigned to a note split this out
        #print("equals")
        self.tokens.append(("OPERATOR", "="))
        self.advance()
        if self.cur_char is not None and self.cur_char.isspace():
          self.advance()  
          while self.cur_char is not None and self.cur_char in "ABCDEFG ": # this should be calling note_token i think
              if self.cur_char is not None and self.cur_char.isspace():
                  self.advance()
                  continue
              elif self.note_token():
                  #print("variable note token")
                  continue
    else:
        return False

  def play_token(self): 
    # Handles DFA State for recognizing a Play Token
    #print(self.cur_char)
    if self.cur_char == "p":
    #   print("p")
      self.advance()
      if self.cur_char == "l":
        self.advance()
        if self.cur_char == "a":
          self.advance()
          if self.cur_char == "y":
            self.advance()
            self.tokens.append(("Keyword", "play"))
            if self.parenthesis_token():
              return True
          else:
            self.errors.append("Error: Missing y in play token.")
            self.tokens.append(("Keyword", "play"))
            if self.parenthesis_token():
              return True
    return False
  
  def parenthesis_token(self):
     # Handles DFA State for recognizing a Parenthesis Token
    if self.cur_char == "(":
      # print("parenthesis")
      self.advance()
      self.tokens.append(("Delimiter", "("))
      # print(self.cur_char)  # it will either be variable starting with ABCDEFG variable with H-Z or a note
      
      if self.note_or_variable():
         if self.cur_char == ")":
            self.tokens.append(("Delimiter", ")"))
            self.advance()
            # print("parenthesis2")
            return True
         else:
            # print(self.cur_char + "130")
            self.errors.append("Error: Missing ) in play token.")
            return False
    else:   
      self.errors.append("Error: Missing ( in play token.")
      if self.note_or_variable():
         if self.cur_char == ")":
            self.tokens.append(("Delimiter", ")"))
            self.advance()
            return True
         else:
            # print(self.cur_char + "141")
            self.errors.append("Error: Missing ) in play token.")
            return False
      
    return False
     
  def note_or_variable(self):
    # Handles DFA State for recognizing a Note or Variable Token
    while self.cur_char is not None:
      if self.cur_char is not None and self.cur_char.isspace():
          self.advance()
          continue
      elif self.cur_char in "ABCDEFG":  # Notes or variable starting with A-G
          # print("note or variable")
          if self.note_token():  # Handle note
              continue
          elif self.cur_char in "abcdefghijklmnopqrstuvwxyz":  # Variable 
              # print("variable")
              if self.variable_token():
                  continue
      elif self.cur_char in "HIJKLMNOPQRSTUVWXYZ":  # Variable starting with H-Z
          # print("variable token")
          self.advance()
          if self.variable_token():
              continue
      else:
         # self.advance()
         return True

  
  # Ignore white space, but remember for variables, they should be on a new line when declared?
  def run(self):
    while self.cur_char is not None:
      if self.cur_char is not None and self.cur_char.isspace():
        self.advance() # might go inside the note loop
        continue 
      while self.cur_char is not None and self.cur_char in "ABCDEFGHIJKLMNOPQRSTUVWXYZ ": # 
        if self.cur_char is not None and self.cur_char.isspace():
            self.advance()
            continue
        elif self.note_token(): # note 
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
        # print(f"Found digit: {self.cur_char}")
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
                  if self.cur_char is not None and self.cur_char.isspace():
                    self.advance()
                  if self.cur_char == "{":
                    # print("brace")
                    self.advance()
                    self.tokens.append(("Keyword", "{"))
                    if self.cur_char is not None and self.cur_char.isspace():
                      # print("space")
                      self.advance()
                    elif self.play_token():
                      # print("play token") 
                      if self.cur_char == "}":
                        self.tokens.append(("Keyword", "}")) #
                        #print("brace2") 
                        self.advance()
                        # This is an accept state
                      else:
                        self.errors.append("Error: Missing } in times token.")
                        # error state
                  else:
                    self.errors.append("Error: Invalid token, missing { in times token.")
                    self.tokens.append(("Keyword", "{"))
                    if self.cur_char is not None and self.cur_char.isspace():
                      # print("space")
                      self.advance()
                    elif self.play_token():
                      #print("play token") 
                      if self.cur_char == "}":
                        self.tokens.append(("Keyword", "}")) #
                        #print("brace2") 
                        self.advance()
                        # This is an accept state
                      else: 
                        self.errors.append("Error: Missing } in times token.")
                        # error state
                else:
                    self.errors.append("Error: Invalid token, missing s in times token.")
                    self.advance()
                    self.tokens.append(("Keyword", "times"))
                    if self.cur_char is not None and self.cur_char.isspace():
                      self.advance()
                    elif self.cur_char == "{":
                      # print("brace")
                      self.advance()
                      self.tokens.append(("Keyword", "{"))
                      if self.cur_char is not None and self.cur_char.isspace():
                        # print("space")
                        self.advance()
                      elif self.play_token():
                        if self.cur_char == "}":
                          self.tokens.append(("Keyword", "}")) #
                          #print("brace2") 
                          self.advance()
                        else:
                          self.errors.append("Error: Missing } in times token.")
                    else:
                        self.errors.append("Error: Invalid token, missing { in times token.")
                        self.tokens.append(("Keyword", "{"))
                        #print("brace")
                        if self.cur_char is not None and self.cur_char.isspace():
                          # print("space")
                          self.advance()
                        elif self.play_token(): 
                          if self.cur_char == "}":
                            self.tokens.append(("Keyword", "}")) #
                            #print("brace2") 
                            self.advance()
                            # This is an accept state
                          else:
                            self.errors.append("Error: Missing } in times token.")

      else:
        return
    return

        
  def get_tokens(self):
    return self.tokens
  def get_errors(self):
    return self.errors


if len(sys.argv) != 2:
    print("Usage: python3 Music_Parser.py 0 or python3 Music_Parser.py 1" )
    sys.exit(1)
    
type = sys.argv[1]
if type == "1":
    # run scanner and then run code
    data = sys.stdin.readlines()
    data_string = "".join(data)
    runParser = LexerDfa(data_string) 
    runParser.run()
    tokens = runParser.get_tokens()
    errors = runParser.get_errors()

    for token in tokens:
        print(token)

    if errors:
        print("Errors encountered:")
        for error in errors:
            print(error)
    
else:
    print("\n Test 1 \n\n")
    # This test shows multiple Identifiers being assigned to notes, and then played 5times in a play token
    # No errors in this first test case
    # Test shows play accepts both variables and notes
    lexer_Dfa1 = LexerDfa("""Thats= G4w That= G4h Me= B4h Espresso= C4q B4q B4w A4q
                            5times{play(Thats That Me Espresso A4w B3h G4w)}""") 
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
    ('IDENTIFIER', 'Thats')
    ('OPERATOR', '=')
    ('NOTE', 'G4w')
    ('IDENTIFIER', 'That')
    ('OPERATOR', '=')
    ('NOTE', 'G4h')
    ('IDENTIFIER', 'Me')
    ('OPERATOR', '=')
    ('NOTE', 'B4h')
    ('IDENTIFIER', 'Espresso')
    ('OPERATOR', '=')
    ('NOTE', 'C4q')
    ('NOTE', 'B4q')
    ('NOTE', 'B4w')
    ('NOTE', 'A4q')
    ('INTEGER', '5')
    ('Keyword', 'times')
    ('Keyword', '{')
    ('Keyword', 'play')
    ('Delimiter', '(')
    ('IDENTIFIER', 'Thats')
    ('IDENTIFIER', 'That')
    ('IDENTIFIER', 'Me')
    ('IDENTIFIER', 'Espresso')
    ('NOTE', 'A4w')
    ('NOTE', 'B3h')
    ('NOTE', 'G4w')
    ('Delimiter', ')')
    ('Keyword', '}')
    '''

    print("\n\n Test 2 \n\n")
    # Handles assigning multiple Identifiers, in different octaves and durations
    # Handles missing y in play token
    # Handes missing note duration, defaults to whole note (G4)
    # Handles different spacing and new lines
    # Handles missing { in times token
    lexer_DFA2 = LexerDfa("""Is = A4w B3h It = B3h That= B3h G7h 
                              G4 
                              Sweet= A4w B3h C4w 5timespla(Is It That Sweet)}""")
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
    Errors encountered:
    Error: Invalid note token, missing duration w, h, q, e, s, default as w.
    Error: Invalid token, missing { in times token.
    Error: Missing ( in play token.
    '''

    print("\n\n Test 3 \n\n")
    # Tests 5 notes to a single Identifier
    # Handles octave number error, 9 defaults to octave 4
    # Handles variables in [H-Z] then [A-G] then [H-Z]
    lexer_DFA3 = LexerDfa("Happy= A4w Birthday= A4w A9h B4w A4w D4h To = A4w A4h B4w A4w You = D4w 5times {play(Birthday To You)}")
    lexer_DFA3.run()
    tokens_3 = lexer_DFA3.get_tokens()
    errors_3 = lexer_DFA3.get_errors()

    for token in tokens_3:
        print(token)
    
    if errors_3:
        print("Errors encountered:")
        for error in errors_3:
            print(error)

    # Output:
    '''
    ('IDENTIFIER', 'Happy')
    ('OPERATOR', '=')
    ('NOTE', 'A4w')
    ('IDENTIFIER', 'Birthday')
    ('OPERATOR', '=')
    ('NOTE', 'A4w')
    ('NOTE', 'A4h')
    ('NOTE', 'B4w')
    ('NOTE', 'A4w')
    ('NOTE', 'D4h')
    ('IDENTIFIER', 'To')
    ('OPERATOR', '=')
    ('NOTE', 'A4w')
    ('NOTE', 'A4h')
    ('NOTE', 'B4w')
    ('NOTE', 'A4w')
    ('IDENTIFIER', 'You')
    ('OPERATOR', '=')
    ('NOTE', 'D4w')
    ('INTEGER', '5')
    ('Keyword', 'times')
    ('Keyword', '{')
    ('Keyword', 'play')
    ('Delimiter', '(')
    ('IDENTIFIER', 'Birthday')
    ('IDENTIFIER', 'To')
    ('IDENTIFIER', 'You')
    ('Delimiter', ')')
    ('Keyword', '}')
    Errors encountered:
    Error: Invalid octave number 9, default as octave 4.
    '''

    print("\n\n Test 4 \n\n")
    # Tests playing before and after the Identifier assignment
    # Testing multiple lines of notes
    # Handles missing ( in play token
    lexer_DFA4 = LexerDfa("play(A4w B3h G4w C4w D4w) Someone= D3h To= A4w B3h G4w C4w D4w Love= F3q playSomeone To Love)")
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
    ('IDENTIFIER', 'Someone')
    ('IDENTIFIER', 'To')
    ('IDENTIFIER', 'Love')
    ('Delimiter', ')')
    Errors encountered:
    Error: Missing ( in play token.
    '''

    print("\n\n Test 5 \n\n")
    # Tests multiple lines of input
    # Tests missing s in times token
    # Missing { in times token
    lexer_DFA5 = LexerDfa("""White= D4h Lips=D4h Pale= A4w Face= B4s
                            Breathin= B4s C3q In= C3q The= D4q Snowflakes= C4q D4q
                            Burnt= E4s F3s Lungs= F3s Sour= G3s Taste= G3s
                            2time play(White Lips Pale Face
                            Breathin In The Snowflakes
                            Burnt Lungs Sour Taste)""")
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
    ('IDENTIFIER', 'White')
    ('OPERATOR', '=')
    ('NOTE', 'D4h')
    ('IDENTIFIER', 'Lips')
    ('OPERATOR', '=')
    ('NOTE', 'D4h')
    ('IDENTIFIER', 'Pale')
    ('OPERATOR', '=')
    ('NOTE', 'A4w')
    ('IDENTIFIER', 'Face')
    ('OPERATOR', '=')
    ('NOTE', 'B4s')
    ('IDENTIFIER', 'Breathin')
    ('OPERATOR', '=')
    ('NOTE', 'B4s')
    ('NOTE', 'C3q')
    ('IDENTIFIER', 'In')
    ('OPERATOR', '=')
    ('NOTE', 'C3q')
    ('IDENTIFIER', 'The')
    ('OPERATOR', '=')
    ('NOTE', 'D4q')
    ('IDENTIFIER', 'Snowflakes')
    ('OPERATOR', '=')
    ('NOTE', 'C4q')
    ('NOTE', 'D4q')
    ('IDENTIFIER', 'Burnt')
    ('OPERATOR', '=')
    ('NOTE', 'E4s')
    ('NOTE', 'F3s')
    ('IDENTIFIER', 'Lungs')
    ('OPERATOR', '=')
    ('NOTE', 'F3s')
    ('IDENTIFIER', 'Sour')
    ('OPERATOR', '=')
    ('NOTE', 'G3s')
    ('IDENTIFIER', 'Taste')
    ('OPERATOR', '=')
    ('NOTE', 'G3s')
    ('INTEGER', '2')
    ('Keyword', 'times')
    ('Keyword', '{')
    ('Keyword', 'play')
    ('Delimiter', '(')
    ('IDENTIFIER', 'White')
    ('IDENTIFIER', 'Lips')
    ('IDENTIFIER', 'Pale')
    ('IDENTIFIER', 'Face')
    ('IDENTIFIER', 'Breathin')
    ('IDENTIFIER', 'In')
    ('IDENTIFIER', 'The')
    ('IDENTIFIER', 'Snowflakes')
    ('IDENTIFIER', 'Burnt')
    ('IDENTIFIER', 'Lungs')
    ('IDENTIFIER', 'Sour')
    ('IDENTIFIER', 'Taste')
    ('Delimiter', ')')
    ('Keyword', '}')
    Errors encountered:
    Error: Invalid token, missing s in times token.
    Error: Invalid token, missing { in times token.
    Error: Missing } in times token.
    '''

    
