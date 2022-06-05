from Exceptions.VKServerIsNotResponding import VKServerIsNotResponding
from Exceptions.UnknownError import UnknownError
from Exceptions.VKTokenError import VKTokenError
from config import url, version
from loguru import logger
import aiohttp


class GetRequests:
    """
    Возвращает информацию о полученных или отправленных заявках
    на добавление в друзья для текущего пользователя
    """

    @staticmethod
    async def get_one_with_need_viewed_false(access_token):
        """
        Получает список одного подписчика, который еще не просмотрен
        """
        async with aiohttp.ClientSession() as session:
            async with session.get(f'{url}friends.getRequests', params={
                'access_token': access_token,
                'count': 1,
                'need_viewed': 0,
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

    @staticmethod
    async def get_all_with_need_viewed_false(access_token, offset):
        """
        Получает список всех подписчиков, которые еще не просмотренные
        """
        async with aiohttp.ClientSession() as session:
            async with session.get(f'{url}friends.getRequests', params={
                'access_token': access_token,
                'count': 1000,
                'need_viewed': 0,
                'offset': offset,
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
