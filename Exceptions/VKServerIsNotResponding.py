class VKServerIsNotResponding(Exception):
    def __init__(self, text='Сервер ВКонтакте не отвечает'):
        self._text = text
        super().__init__(self._text)
