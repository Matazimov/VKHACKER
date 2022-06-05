class CannotAddThisUserToFriendsAsUserNotFound(Exception):
    def __init__(self, text='заблокирован/заморожен'):
        self._text = text
        super().__init__(self._text)
