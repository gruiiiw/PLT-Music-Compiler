class Parser:
    def __init__(self) -> None:
        self.current_state = 0 #start]
        self.stateMachine = self.buildStateMachine()
        
    def buildStateMachine(self):
        state_machine = [
            # A-G, 1-8,   whqes,   whitespace\n, delimiter, operator, identifier, keyword,  [H-Z],  
            [8],     [18], [21],     [0],          [21],     [21],      [21]         [10],     [5],   #start do nothing
            [21],     [21], [2],     [21],          [21],     [21],      [21]         [21],     [21],   #q1 NOTE
            [8],     [18], [21],     [0],          [21],     [21],      [21]         [10],     [5],   #q2
            [8],     [18], [21],     [0],          [21],     [21],      [21]         [10],     [5],   #q3
            [8],     [18], [21],     [0],          [21],     [21],      [21]         [10],     [5],   #q4
            [8],     [18], [21],     [0],          [21],     [21],      [21]         [10],     [5],   #q5
            [8],     [18], [21],     [0],          [21],     [21],      [21]         [10],     [5],   #q6
            [8],     [18], [21],     [0],          [21],     [21],      [21]         [10],     [5],   #q7
            [8],     [18], [21],     [0],          [21],     [21],      [21]         [10],     [5],   #q8
            [8],     [18], [21],     [0],          [21],     [21],      [21]         [10],     [5],   #q9
            [8],     [18], [21],     [0],          [21],     [21],      [21]         [10],     [5],   #q10
            [8],     [18], [21],     [0],          [21],     [21],      [21]         [10],     [5],   #q11
            [8],     [18], [21],     [0],          [21],     [21],      [21]         [10],     [5],   #q12
            [8],     [18], [21],     [0],          [21],     [21],      [21]         [10],     [5],   #q13
            [8],     [18], [21],     [0],          [21],     [21],      [21]         [10],     [5],   #q14
            [8],     [18], [21],     [0],          [21],     [21],      [21]         [10],     [5],   #q15
            [8],     [18], [21],     [0],          [21],     [21],      [21]         [10],     [5],   #q16
            [8],     [18], [21],     [0],          [21],     [21],      [21]         [10],     [5],   #q17
            [8],     [18], [21],     [0],          [21],     [21],      [21]         [10],     [5],   #q18
            [8],     [18], [21],     [0],          [21],     [21],      [21]         [10],     [5],   #q19
            [8],     [18], [21],     [0],          [21],     [21],      [21]         [10],     [5],   #q20
            [21],     [21], [21],     [21],          [21],     [21],      [21]         [21],     [21],   #q21
        ]
        
        
        
    def get_next_state(self):
        pass
    
