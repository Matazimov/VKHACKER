from Exceptions.VKServerIsNotResponding import VKServerIsNotResponding
from Exceptions.VKTokenError import VKTokenError
from Exceptions.UnknownError import UnknownError
from config import url, version
from loguru import logger
import aiohttp


class UsersGet:
    """"Возвращает расширенную информацию о пользователях"""

    @staticmethod
    async def get_self(access_token):
        """Возвращает о себе информацию"""
        async with aiohttp.ClientSession() as session:
            async with session.get(f'{url}users.get', params={
                'access_token': access_token,
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
    async def get_with_friend_status(access_token, user_ids):
        """Возвращает о любом пользователе информацию с friend_status"""
        async with aiohttp.ClientSession() as session:
            async with session.get(f'{url}users.get', params={
                'access_token': access_token,
                'user_ids': user_ids,
                'fields': 'friend_status',
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
