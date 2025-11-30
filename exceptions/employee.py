class EmployeeNotFound(Exception):
    def __init__(self, message="Employee not found"):
        self.message = message
        super().__init__(self.message)

class IncorrectPassword(Exception):
    def __init__(self, message="Incorrect password"):
        self.message = message
        super().__init__(self.message)

class IncorrectRole(Exception):
    def __init__(self, message="Incorrect role"):
        self.message = message
        super().__init__(self.message)
