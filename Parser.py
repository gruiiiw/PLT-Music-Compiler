class Parser:
    def __init__(self) -> None:
        self.current_state = 0 #start]
        self.stateMachine = self.buildStateMachine()
     
    # the main issue with our state machine is that there are a couple of states that require more specific inputs i.e. state 10 requires us to check for p then l then a then y
    # so we have to add that functionality but that might blow up the state machine a bit.     
    def buildStateMachine(self):
        state_machine = [
            # A-G 0,  1-8 1, whqes 2, whitespace\n 3, delimiter 4, operator 5, identifier 6  [H-Z] 7 , keyword 8,   id[a-z] 9   ( 10   0 11   [0-9] 12    p 13, l 14, a 15, y16, t17, i18, m19, e20, s21   
             
            [8,     18,        33,     0,                 33,         33,          33,           5,        33,          33,       33,     33,      18,      33,    33,  33,   33,  33,   33,  33, 33, 33],#start do nothing Accept state 
            [33,     33,        2,     33,                33,         33,          33,           33,        33,          33,       33,     33,      33,      33,    33,  33,   33,  33,   33,  33, 33, 33],#q1 
            [3,     33,        33,     0,                 33,         33,          33,           33,        33,          33,       33,     33,      33,      33,    33,  33,   33,  33,   33,  33, 33, 33],#q2 NOTE accept state (program can terminate if here)
            [33,     1,        33,     33,                33,         33,          33,           33,        33,          33,       33,     33,      33,      33,    33,  33,   33,  33,   33,  33, 33, 33],#q3 start of note
            [33,     33,        33,     33,                33,         6,          33,           33,        33,          4,       33,     33,      33,      33,    33,  33,   33,  33,   33,  33, 33, 33],#q4 identifier
            [33,     33,        33,     33,                33,         33,          33,           33,        33,          4,       33,     33,      33,      33,    33,  33,   33,  33,   33,  33, 33, 33],#q5
            [3,      33,        33,     33,                33,         33,          33,           33,        33,          33,       33,     33,      33,      33,    33,  33,   33,  33,   33,  33, 33, 33],#q6 operator 
            [33,     33,        33,     33,                33,         33,          33,           33,        33,          33,       33,     33,      33,      33,    33,  33,   33,  33,   33,  33, 33, 33],#q7 i didnt include q7 on my state machine my b
            [33,     1,        33,     33,                33,         33,          33,           33,        33,          4,       33,     33,      33,      33,    33,  33,   33,  33,   33,  33, 33, 33],#q8
            [33,     33,        33,     33,                33,         33,          33,           33,        33,          33,       33,     33,      33,      33,    33,  33,   33,  33,   33,  33, 33, 33],#q9 no q9 either
            [33,     33,        33,     33,                33,         33,          33,           33,        33,          33,       33,     33,      33,      33,    22,  33,   33,  33,   33,  33, 33, 33],#q10 KEYWORD if we get p->l->a->y we go stay here, then when we get ( we go to q11 not sure how to code this
            [12,     33,        33,     33,                33,         33,          33,           17,        33,          33,       33,     33,      33,      33,    33,  33,   33,  33,   33,  33, 33, 33],#q11 Dilimiter (
            [33,     13,        33,     33,                33,         33,          33,           33,        33,          16,       33,     33,      33,      33,    33,  33,   33,  33,   33,  33, 33, 33],#q12
            [33,     33,        14,     33,                33,         33,          33,           33,        33,          33,       33,     33,      33,      33,    33,  33,   33,  33,   33,  33, 33, 33],#q13
            [33,     33,        33,     33,                33,         33,          33,           33,        33,          33,       15,     33,      33,      33,    33,  33,   33,  33,   33,  33, 33, 33],#q14 NOTE close bracket go 15
            [8,     18,        33,     0,                 33,         33,          33,           5,        33,          33,       33,     33,      18,      33,    33,  33,   33,  33,   33,  33, 33, 33],#q15 Delimitter and go to start (Accept state)
            [33,     33,        33,     33,                33,         33,          33,           33,        33,          33,       33,     15,      33,      33,    33,  33,   33,  33,   33,  33, 33, 33],#q16 IDENTIFIER, stays here on a-z, moves to 15 on ) and sets to ID
            [33,     33,        33,     33,                33,         33,          33,           33,        33,          16,       33,     33,      33,      33,    33,  33,   33,  33,   33,  33, 33, 33],#q17 in an identifier 
            [33,     18,        33,     33,                33,         33,          33,           33,        33,          33,       33,     33,      18,      33,    33,  33,   33,  19,   33,  33, 33, 33],#q18 INT, if we get a t go to q25
            [33,     33,        33,     33,                33,         33,          33,           33,        33,          33,       33,     33,      33,      33,    33,  33,   33,  33,   25,  33, 33, 33],#q19 Whitespace
            [88,     18,        33,     0,                 33,         33,          33,           5,        33,          33,       33,     33,      18,      33,    33,  33,   33,  33,   33,  33, 33, 33],#q20 go back to start state (not accept) 
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
            [33,     33,        33,     33,                33,         33,          33            33,        33,           33,       33,     33,     33,      33,    33,  33,   33,  33,   33,  33, 33, 33]#q33 Error state. Return lexical error if we get here
        ]
        
        
        
    def get_next_state(self):
        pass
    
