class TooManyRequestsPerSecond(Exception):
    def __init__(self, text='Слишком много запросов в секунду'):
        self._text = text
        super().__init__(self._text)
