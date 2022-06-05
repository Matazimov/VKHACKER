class VKTokenError(Exception):
    def __init__(self, text='Неправильный токен'):
        self._text = text
        super().__init__(self._text)
