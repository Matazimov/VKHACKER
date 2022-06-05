class CaptchaNeeded(Exception):
    def __init__(self, text='Требуется ввод кода с картинки (Captcha)'):
        self._text = text
        super().__init__(self._text)
