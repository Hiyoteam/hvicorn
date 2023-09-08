class MissingArgumentException(Exception):
    def __init__(self, message=None):
        self.message = "Missing argument"
        if message:
            self.message += ": "+message
        super().__init__(self.message)