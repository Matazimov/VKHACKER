class TooManyRequestsPerSecond(Exception):
    def __init__(self, text='Too many'):
        self._text = text
        super().__init__(self._text)
