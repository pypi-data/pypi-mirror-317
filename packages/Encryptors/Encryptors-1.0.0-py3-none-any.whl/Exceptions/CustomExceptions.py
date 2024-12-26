

class CustomException(Exception):
    def __init__(self, *args):
        super().__init__(*args) 


class UnahorizatedException(CustomException):
    pass

class AESEncryptError(CustomException):
    pass