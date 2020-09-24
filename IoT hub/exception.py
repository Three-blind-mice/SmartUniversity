class DriverError(Exception):
    pass

class ZoomError(DriverError):

    def __init__(self, text):
        self.txt = text

    def __str__(self):
        return self.txt

class LmsError(DriverError):

    def __init__(self, txt):
        self.txt = txt

    def __str__(self):
        return self.txt