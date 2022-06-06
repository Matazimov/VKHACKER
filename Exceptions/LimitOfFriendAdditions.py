class LimitOfFriendAdditions(Exception):
    def __init__(self, text='лимит на добавление в друзья'):
        self._text = text
        super().__init__(self._text)
