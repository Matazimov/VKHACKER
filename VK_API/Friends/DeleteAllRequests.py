from Exceptions.VKServerIsNotResponding import VKServerIsNotResponding
from Exceptions.UnknownError import UnknownError
from Exceptions.VKTokenError import VKTokenError
from config import url, version
from loguru import logger
import aiohttp


class DeleteAllRequests:
    """
    Отмечает все входящие заявки на добавление в друзья как просмотренные
    """

    @staticmethod
    async def delete_all_requests(access_token):
        async with aiohttp.ClientSession() as session:
            async with session.post(f'{url}friends.deleteAllRequests', params={
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
