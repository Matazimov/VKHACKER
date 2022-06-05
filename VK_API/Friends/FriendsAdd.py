from Exceptions.CannotAddThisUserToFriendsAsTheyHavePutYouOnTheirBlacklist \
    import CannotAddThisUserToFriendsAsTheyHavePutYouOnTheirBlacklist
from Exceptions.CannotAddThisUserToFriendsAsYouPutHimOnBlacklist \
    import CannotAddThisUserToFriendsAsYouPutHimOnBlacklist
from Exceptions.CannotAddThisUserToFriendsAsUserNotFound \
    import CannotAddThisUserToFriendsAsUserNotFound
from Exceptions.VKServerIsNotResponding import VKServerIsNotResponding
from Exceptions.LimitOfFriendAdditions import LimitOfFriendAdditions
from Exceptions.CaptchaNeeded import CaptchaNeeded
from Exceptions.UnknownError import UnknownError
from Exceptions.VKTokenError import VKTokenError
from config import url, version
from loguru import logger
from File import File
import aiohttp


class FriendsAdd:
    """Одобряет или создаёт заявку на добавление в друзья"""

    @staticmethod
    async def add_without_captcha(access_token, user_id):
        """Добавляет пользователя"""

        file = File()
        async with aiohttp.ClientSession() as session:
            async with session.post(f'{url}friends.add', params={
                'access_token': access_token,
                'user_id': user_id,
                'v': version
            }) as resp:
                data = await resp.json()

                if 'response' in data:
                    return data
                elif 'error' in data:
                    if data['error']['error_code'] == 5:
                        raise VKTokenError
                    elif data['error']['error_code'] == 9:
                        raise LimitOfFriendAdditions
                    elif data['error']['error_code'] == 14:
                        await file.saver_captcha_sid(data['error']['captcha_sid'])
                        raise CaptchaNeeded
                    elif data['error']["error_code"] == 175:
                        raise CannotAddThisUserToFriendsAsTheyHavePutYouOnTheirBlacklist
                    elif data['error']["error_code"] == 176:
                        raise CannotAddThisUserToFriendsAsYouPutHimOnBlacklist
                    elif data['error']['error_code'] == 177:
                        raise CannotAddThisUserToFriendsAsUserNotFound
                    else:
                        logger.error(data['error'])
                        raise UnknownError
                else:
                    raise VKServerIsNotResponding

    @staticmethod
    async def add_with_captcha(access_token, user_id, captcha_sid, captcha_key):
        """Добавляет пользователя с вводом капчи"""

        file = File()
        async with aiohttp.ClientSession() as session:
            async with session.post(f'{url}friends.add', params={
                'access_token': access_token,
                'user_id': user_id,
                'v': version,
                'captcha_sid': captcha_sid,
                'captcha_key': captcha_key
            }) as resp:
                data = await resp.json()

                if 'response' in data:
                    return data
                elif 'error' in data:
                    if data['error']['error_code'] == 5:
                        raise VKTokenError
                    elif data['error']['error_code'] == 9:
                        raise LimitOfFriendAdditions
                    elif data['error']['error_code'] == 14:
                        await file.saver_captcha_sid(data['error']['captcha_sid'])
                        raise CaptchaNeeded
                    elif data['error']["error_code"] == 175:
                        raise CannotAddThisUserToFriendsAsTheyHavePutYouOnTheirBlacklist
                    elif data['error']["error_code"] == 176:
                        raise CannotAddThisUserToFriendsAsYouPutHimOnBlacklist
                    elif data['error']['error_code'] == 177:
                        raise CannotAddThisUserToFriendsAsUserNotFound
                    else:
                        logger.error(data['error'])
                        raise UnknownError
                else:
                    raise VKServerIsNotResponding
