class Parser:
    def __init__(self) -> None:
        self.current_state = 0 #start]
        self.stateMachine = self.buildStateMachine()
     
    # the main issue with our state machine is that there are a couple of states that require more specific inputs i.e. state 10 requires us to check for p then l then a then y
    # so we have to add that functionality but that might blow up the state machine a bit.     
    def buildStateMachine(self):
        state_machine = [
            # A-G,  1-8, whqes,   whitespace\n, delimiter, operator, identifier [A-Z], keyword,  [H-Z], id[a-z] 
            [8,     18, 21,     0,          21,     21,      21         10,     5,        21,       21,     21],#start do nothing Accept state 
            [21,     21, 2,     21,          21,     21,      21         21,     21,        21,       21,     21],#q1 
            [3,     21, 21,     0,          21,     21,      21         21,     21,        21,       21,     21],#q2 NOTE accept state (program can terminate if here)
            [21,     1, 21,     21,          21,     21,      21         21,     21,        21,       21,     21],#q3 start of note
            [4,     21, 21,     21,          21,     6,      4         21,     21,        21,       21,     21],#q4 identifier
            [21,     21, 21,     21,          21,     21,      21         21,     21,        4,       21,     21],#q5
            [3,      21, 21,     21,          21,     21,      21         21,     21,        21,       21,     21],#q6 operator 
            [21,     21, 21,     21,          21,     21,      21         21,     21,        21,       21,     21],#q7 i didnt include q7 on my state machine my b
            [21,     1, 21,     21,          21,     21,      21         21,     21,        4,       21,     21],#q8
            [21,     21, 21,     21,          21,     21,      21         21,     21,        21,       21,     21],#q9 no q9 either
            [21,     21, 21,     21,          21,     21,      21         21,     21,        21,       21,     21],#q10 KEYWORD if we get p->l->a->y we go stay here, then when we get ( we go to q11 not sure how to code this
            [12,     21, 21,     21,          21,     11,      21         21,     17,        21,       21,     21],#q11 Dilimiter (
            [21,     13, 21,     21,          21,     21,      21         21,     21,        21,       21,     16],#q12
            [21,     21, 14,     21,          21,     21,      21         21,     21,        21,       21,     21],#q13
            
            [21,     21, 21,     21,          21,     15,      21         21,     21,        21,       21,     21],#q14 NOTE close bracket go 15
            [8,     18, 21,     0,          21,     21,      21         10,     5,        21,       21,     21],#q15 Delimitter and go to start (Accept state)
            [21,     21, 21,     21,          21,     15,      21         21,     21,        21,       21,     16],#q16 IDENTIFIER, stays here on a-z, moves to 15 on ) and sets to ID
            [21,     21, 21,     21,          21,     21,      21         21,     21,        21,       21,     16],#q17 in an identifier 
            [21,     18, 21,     21,          21,     21,      21         21,     21,        21,       21,     21],#q18 INT 0-9 times -> 19
            
            [21,     21, 21,     21,          20,     21,      21         21,     21,        21,       21,     21],#q19 Whitespace
            [8,     18, 21,     0,          21,     21,      21         10,     5,        21,       21,     21],#q20 go back to start state (not accept)
            [21,     21, 21,     21,          21,     21,      21         21,     21,        21,       21,     21]#q21 Error state. Return lexical error if we get here
        ]
        
        
        
    def get_next_state(self):
        pass
    
