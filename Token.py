class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value  
        
    def toString(self):
        return f"<{self.type}, {self.value}>"
        