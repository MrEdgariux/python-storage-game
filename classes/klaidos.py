
class FileWriteError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class DiskFullError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class FileDublicateError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class FileReadError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class NotEnoughMoneyError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class ServerNoEmptyDiskSlots(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class ServerDiskAlreadyMounted(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class NASNoFreeServers(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class SaveVersionDismatch(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class SaveFileEncryptionError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class SaveFileDecryptionError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)