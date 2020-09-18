class ZoomError(Exception):
    def __init__(self, text):
        self.txt = text
    def __str__(self):
        return self.txt