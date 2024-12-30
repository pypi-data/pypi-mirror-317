class Base:

    def __init__(self):
        self.exp_admitted = False
        self.eventHistory = {}
    
    def get_exp_status(self) -> bool:
        return self.exp_admitted