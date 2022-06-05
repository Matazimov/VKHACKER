class CannotAddThisUserToFriendsAsTheyHavePutYouOnTheirBlacklist(Exception):
    def __init__(self, text='он(а) занес(ла) вас в черный список'):
        self._text = text
        super().__init__(self._text)
