class Parser:
    def __init__(self) -> None:
        self.current_state = 0 #start]
        self.stateMachine = self.buildStateMachine()
        self.token_states_arrive = {2: "Note", 6: "Operator", 27: "Keyword", 14: "Note", 15: "Delimitter", 20: "Whitespace"}
        self.token_states_leave = {4: "Identifier", 2: "Whitespace", 10: "Delimitter", 16: "Identifier", 18: "Integer", 24: "Keyword"}
        self.final_states = {0, 2,15}
     
    # the main issue with our state machine is that there are a couple of states that require more specific inputs i.e. state 10 requires us to check for p then l then a then y
    # so we have to add that functionality but that might blow up the state machine a bit.     
    def buildStateMachine(self):
        state_machine = [
            # A-G 0,  1-8 1, whqes 2, whitespace\n 3, delimiter 4, operator 5, identifier 6  [H-Z] 7 , keyword 8,   id[a-z] 9   ( 10   0 11   [0-9] 12    p 13, l 14, a 15, y16, t17, i18, m19, e20, s21   # unused col 6 and 8 row 7 and 9
             
            [8,     18,        33,     0,                 33,         33,          33,           5,        33,          33,       33,     33,      18,      22,    33,  33,   33,  33,   33,  33, 33, 33],#start do nothing Accept state 
            [33,     33,        2,     33,                33,         33,          33,           33,        33,          33,       33,     33,      33,      33,    33,  33,   33,  33,   33,  33, 33, 33],#q1 
            [3,     33,        33,     0,                 33,         33,          33,           33,        33,          33,       33,     33,      33,      33,    33,  33,   33,  33,   33,  33, 33, 33],#q2 NOTE accept state (program can terminate if here)
            [33,     1,        33,     33,                33,         33,          33,           33,        33,          33,       33,     33,      33,      33,    33,  33,   33,  33,   33,  33, 33, 33],#q3 start of note
            [33,     33,        33,     33,                33,         6,          33,           33,        33,          4,       33,     33,      33,      4,    4,  4,   4,  4,   4,  4, 4, 4],#q4 identifier
            [33,     33,        33,     33,                33,         33,          33,           33,        33,          4,       33,     33,      33,      4,    4,  4,   4,  4,   4,  4, 4, 4],#q5
            [3,      33,        33,     33,                33,         33,          33,           33,        33,          33,       33,     33,      33,      33,    33,  33,   33,  33,   33,  33, 33, 33],#q6 operator 
            [33,     33,        33,     33,                33,         33,          33,           33,        33,          33,       33,     33,      33,      33,    33,  33,   33,  33,   33,  33, 33, 33],#q7 i didnt include q7 on my state machine my b
            [33,     1,        33,     33,                33,         33,          33,           33,        33,          4,       33,     33,      33,      4,    4,  4,   4,  4,   4,  4, 4, 4],#q8
            [33,     33,        33,     33,                33,         33,          33,           33,        33,          33,       33,     33,      33,      33,    33,  33,   33,  33,   33,  33, 33, 33],#q9 no q9 either
            [33,     33,        33,     33,                33,         33,          33,           33,        33,          33,       33,     33,      33,      33,    22,  33,   33,  33,   33,  33, 33, 33],#q10 KEYWORD if we get p->l->a->y we go stay here, then when we get ( we go to q11 not sure how to code this
            [12,     33,        33,     33,                33,         33,          33,           17,        33,          33,       33,     33,      33,      33,    33,  33,   33,  33,   33,  33, 33, 33],#q11 Dilimiter (
            [33,     13,        33,     33,                33,         33,          33,           33,        33,          16,       33,     33,      33,      16,    16,  16,   16,  16,   16,  16, 16, 16],#q12
            [33,     33,        14,     33,                33,         33,          33,           33,        33,          33,       33,     33,      33,      33,    33,  33,   33,  33,   33,  33, 33, 33],#q13
            [33,     33,        33,     33,                33,         33,          33,           33,        33,          33,       15,     33,      33,      33,    33,  33,   33,  33,   33,  33, 33, 33],#q14 NOTE close bracket go 15
            [8,     18,        33,     0,                 33,         33,          33,           5,        33,          33,       33,     33,      18,      22,    33,  33,   33,  33,   33,  33, 33, 33],#q15 Delimitter and go to start (Accept state)
            [33,     33,        33,     33,                33,         33,          33,           33,        33,          33,       33,     15,      33,      33,    33,  33,   33,  33,   33,  33, 33, 33],#q16 IDENTIFIER, stays here on a-z, moves to 15 on ) and sets to ID
            [33,     33,        33,     33,                33,         33,          33,           33,        33,          16,       33,     33,      33,      16,    16,  16,   16,  16,   16,  16, 16, 16],#q17 in an identifier 
            [33,     18,        33,     33,                33,         33,          33,           33,        33,          33,       33,     33,      18,      33,    33,  33,   33,  19,   33,  33, 33, 33],#q18 INT, if we get a t go to q25
            [33,     33,        33,     33,                33,         33,          33,           33,        33,          33,       33,     33,      33,      33,    33,  33,   33,  33,   25,  33, 33, 33],#q19 Whitespace
            [88,     18,        33,     0,                 33,         33,          33,           5,        33,          33,       33,     33,      18,      22,    33,  33,   33,  33,   33,  33, 33, 33],#q20 go back to start state (not accept) 
            [33,     33,        33,     33,                33,         33,          33,           33,        33,          33,       33,     33,      33,      33,    33,  23,   33,  33,   33,  33, 33, 33],#q22l->a
            [33,     33,        33,     33,                33,         33,          33,           33,        33,          33,       33,     33,      33,      33,    33,  33,   24,  33,   33,  33, 33, 33],#q23a->y
            [33,     33,        33,     33,                33,         33,          33,           33,        33,          33,       33,     33,      33,      33,    33,  33,   33,  11,   33,  33, 33, 33],#q24y->11
            [33,     33,        33,     33,                33,         33,          33,           33,        33,          33,       33,     33,      33,      33,    33,  33,   33,  33,   33,  26, 33, 33],#q25 i->m
            [33,     33,        33,     33,                33,         33,          33,           33,        33,          33,       33,     33,      33,      33,    33,  33,   33,  33,   33,  33, 27, 33],#q26 m->e
            [33,     33,        33,     33,                33,         33,          33,           33,        33,          33,       33,     33,      33,      33,    33,  33,   33,  33,   33,  33, 33, 28],#q27 e->s
            [33,     33,        33,     20,                33,         33,          33,           33,        33,          33,       33,     33,      33,      33,    33,  33,   33,  33,   33,  33, 33, 33],#q28
            [33,     33,        33,     33,                33,         33,          33,           33,        33,          33,       33,     33,      33,      33,    33,  33,   33,  33,   33,  33, 33, 33],#q29
            [33,     33,        33,     33,                33,         33,          33,           33,        33,          33,       33,     33,      33,      33,    33,  33,   33,  33,   33,  33, 33, 33],#q30
            [33,     33,        33,     33,                33,         33,          33,           33,        33,          33,       33,     33,      33,      33,    33,  33,   33,  33,   33,  33, 33, 33],#q31
            [33,     33,        33,     33,                33,         33,          33,           33,        33,          33,       33,     33,      33,      33,    33,  33,   33,  33,   33,  33, 33, 33],#q32
            [33,     33,        33,     33,                33,         33,          33,            33,        33,           33,       33,     33,     33,      33,    33,  33,   33,  33,   33,  33, 33, 33]#q33 Error state. Return lexical error if we get here
        ]
        return state_machine
        
    # TODO build state machine matrix
    def getStateCode(self, value):
          # p 13, 
        if value == "p":
            return 13
        
        if value == "l":
            return 14
        if value == "a":
            return 15
        if value == "y":
            return 16
        if value == "t":
            return 17
        if value == "i":
            return 18
        if value == "m":
            return 19
        if value == "e":
            return 20
        if value == "s":
            return 21
        
        
        if value in "ABCDEFG":
            return 0
        
        if value.isdigit() and int(value) in range(1, 9):
            return 1
        
        #whqes 2
        if value in "whqes":
            return 2
        
        # , whitespace\n 
        if value in "\n\t ":
            return 3
        
        # 4, delimiter 
        if value in ":(){}":
            return 4
        
        # 5, operator 
        if value == "=":
            return 5
        
        # identifier 6 skip 
        
        # [H-Z] 7 
        if value in "HIJKLMNOPQRSTUVWXYZ":
            return 7
        
        # , keyword 8,  skip 
        
        # id[a-z] 9   
        if value in "abcdefghijklmnopqrstuvwxyz":
            return 9
        
        
        # ( 10   
        if value == '(':
            return 10
        
        
        # 0 11   
        if value == "(":
            return 11 
        
        
        # [0-9] 12    
        if value.isdigit():
            return 12
        
        return 33
        
    def scan(self, string):
        prev_state = 0
        lexical_analysis = []
        cur_seq = []
        cur_state = 0
        for char in string:
            if char == ' ':
                continue
            
            if cur_state in self.token_states_arrive:
                lexical_analysis.append((self.token_states_arrive[cur_state], "".join(cur_seq)))
                cur_seq = []
            
            cur_seq.append(char)
            
            # print(cur_state, char)
            prev_state = cur_state
            cur_state = self.stateMachine[cur_state][self.getStateCode(char)]
            
            if cur_state == 33:
                print(prev_state)
                return self.handleErrors(f"Invalid character {char}")
            
            if cur_state in self.token_states_leave:
                lexical_analysis.append((self.token_states_leave[cur_state], "".join(cur_seq)))
                cur_seq = []

            
        if cur_state in self.final_states:
            return lexical_analysis
        
        return self.handleErrors("Not in a ending final state")
            
                
                
    
    def handleErrors(self, err):
        return [err]