class ThereAreNoEntriesInThisPageOrGroup(Exception):
    def __init__(self, text='В этой странице/группе нету записей'):
        self._text = text
        super().__init__(self._text)
