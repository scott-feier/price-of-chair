class ItemError(Exception):
    def __init__(self, message):
        self.message = message


class ItemNotExistError(ItemError):
    pass

