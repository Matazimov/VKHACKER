from Exceptions.VKServerIsNotResponding import VKServerIsNotResponding
from Exceptions.VKTokenError import VKTokenError
from Exceptions.UnknownError import UnknownError
from config import url, version
from loguru import logger
import aiohttp


class WallGet:
    """Возвращает список записей со стены пользователя или сообщества"""

    @staticmethod
    async def get(access_token, identifier, offset):
        async with aiohttp.ClientSession() as session:
            async with session.get(f'{url}wall.get', params={
                'access_token': access_token,
                f"{'owner_id' if '-' in identifier else 'domain'}": identifier,
                'offset': offset,
                'count': 100,
                'filter': 'others',
                'v': version
            }) as resp:
                data = await resp.json()

                if 'response' in data:
                    return data
                elif 'error' in data:
                    if data['error']['error_code'] == 5:
                        raise VKTokenError
                    else:
                        logger.error(data['error'])
                        raise UnknownError
                else:
                    raise VKServerIsNotResponding
