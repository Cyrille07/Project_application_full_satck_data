class TaskNotFound(Exception):
    def __init__(self, message="The task doen't exist"):
        self.message = message
        super().__init__(self.message)


class TaskAlreadyExists(Exception):
    def __init__(self, message="The task already exists"):
        self.message = message
        super().__init__(self.message)


class WrongAuthor(Exception):
    def __init__(self, message="Wrong Author"):
        self.message = message
        super().__init__(self.message)
