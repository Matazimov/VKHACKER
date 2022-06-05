class CannotAddThisUserToFriendsAsYouPutHimOnBlacklist(Exception):
    def __init__(self, text='вы занесли его в черный список'):
        self._text = text
        super().__init__(self._text)
