import aiofiles


class File:
    """Записывает и читает sid капчи"""

    @staticmethod
    async def saver_captcha_sid(text):
        async with aiofiles.open(f'captcha.txt', 'w+') as file:
            await file.write(f'{text}')

    @staticmethod
    async def reader_captcha_sid():
        async with aiofiles.open(f'captcha.txt', 'r') as file:
            return await file.read()
