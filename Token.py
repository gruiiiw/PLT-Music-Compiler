class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value  
        
    def toString(self):
        return f"<{self.type}, {self.value}>"
    
    def type_key(self):
        if self.type == "KEYWORD":
            return 0    
        
        if self.type == "IDENTIFIER":
            return 1
        
        if self.type == "OPERATOR":
            return 2
        
        if self.type == "NUMBER":
            return 3
        
        if self.type == "NOTE":
            return 4
        
        if self.type == "WHITESPACE":
            return 5
        
        if self.type == "DELIMITER":
            return 6
        
    