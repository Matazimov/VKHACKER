import os


class UnknownError(Exception):
    text = [
        'Произошла неизвестная ошибка.',
        'Если хотите посодействовать развитию '
        'отправьте лог ошибок по пути: ',
        f'{os.path.abspath("logs.log")}',
        'разработчику в телеграм: https://t.me/mr_qpdb'
    ]

    def __init__(self, text='\n'.join(text)):
        self.text = text
        super().__init__(self.text)
