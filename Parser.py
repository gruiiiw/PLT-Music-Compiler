class Parser:
    def __init__(self) -> None:
        self.current_state = 0 #start]
        self.stateMachine = self.buildStateMachine()
        
    def buildStateMachine(self):
        state_machine = [
            # A-G, 1-8,   whqes,   whitespace\n, delimiter, operator, identifier [A-Z], keyword,  [H-Z], identifier [a-z] 
            [8,     18, 21,     0,          21,     21,      21         10,     5,        21],#start do nothing Accept state 
            [21,     21, 2,     21,          21,     21,      21         21,     21,        21],#q1 NOTE
            [3,     21, 21,     0,          21,     21,      21         21,     21,        21],#q2 accept state (program can terminate if here)
            [21,     1, 21,     21,          21,     21,      21         21,     21,        21],#q3 start of note
            [4,     21, 21,     21,          21,     6,      4         21,     21,        21],#q4 identifier
            [21,     21, 21,     21,          21,     21,      21         21,     21,        4],#q5
            [3,      21, 21,     21,          21,     21,      21         21,     21,        21],#q6
            [21,     21, 21,     21,          21,     21,      21         21,     21,        21],#q7 i didnt include q7 on my state machine my b
            [21,     1, 21,     21,          21,     21,      21         21,     21,        4],#q8
            [21,     21, 21,     21,          21,     21,      21         21,     21,        21],#q9 no q9 either
            [21,     21, 21,     21,          21,     21,      21         21,     21,        21],#q10 if we get p->l->a->y we go stay here, then when we get ( we go to q11
            
            [21,     21, 21,     21,          21,     21,      21         21,     21,        21],#q11
            [21,     21, 21,     21,          21,     21,      21         21,     21,        21],#q12
            [21,     21, 21,     21,          21,     21,      21         21,     21,        21],#q13
            [21,     21, 21,     21,          21,     21,      21         21,     21,        21],#q14
            [21,     21, 21,     21,          21,     21,      21         21,     21,        21],#q15
            [21,     21, 21,     21,          21,     21,      21         21,     21,        21],#q16
            [21,     21, 21,     21,          21,     21,      21         21,     21,        21],#q17
            [21,     21, 21,     21,          21,     21,      21         21,     21,        21],#q18
            [21,     21, 21,     21,          21,     21,      21         21,     21,        21],#q19
            [21,     21, 21,     21,          21,     21,      21         21,     21,        21],#q20
            [21,     21, 21,     21,          21,     21,      21         21,     21,        21]#q21
        ]
        
        
        
    def get_next_state(self):
        pass
    
