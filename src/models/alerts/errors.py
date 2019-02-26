class AlertError(Exception):
    def __init__(self, message):
        self.message = message


class AlertNotExistError(AlertError):
    pass

