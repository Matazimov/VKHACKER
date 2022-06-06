from Exceptions.CannotAddThisUserToFriendsAsTheyHavePutYouOnTheirBlacklist import \
    CannotAddThisUserToFriendsAsTheyHavePutYouOnTheirBlacklist
from Exceptions.CannotAddThisUserToFriendsAsUserNotFound \
    import CannotAddThisUserToFriendsAsUserNotFound
from Exceptions.CannotAddThisUserToFriendsAsYouPutHimOnBlacklist import CannotAddThisUserToFriendsAsYouPutHimOnBlacklist
from Exceptions.CaptchaNeeded import CaptchaNeeded
from Exceptions.LimitOfFriendAdditions import LimitOfFriendAdditions
from Exceptions.ThereAreNoEntriesInThisPageOrGroup import ThereAreNoEntriesInThisPageOrGroup
from Exceptions.TooManyRequestsPerSecond import TooManyRequestsPerSecond
from Exceptions.VKServerIsNotResponding import VKServerIsNotResponding
from VK_API.Friends.DeleteAllRequests import DeleteAllRequests
from config import access_tokens, groups, records
from VK_API.Friends.GetRequests import GetRequests
from Exceptions.UnknownError import UnknownError
from Exceptions.VKTokenError import VKTokenError
from VK_API.Friends.FriendsAdd import FriendsAdd
from VK_API.Users.UsersGet import UsersGet
from VK_API.Wall.WallGet import WallGet
from clear_console import clear_console
from support_us import support_us
from rich import print
from File import File


class FirstMethod(GetRequests, FriendsAdd, WallGet, UsersGet, File):
    """
    Добавляет всех новых не просмотренных подписчиков и пользователей
    со стены пользователя или сообщества
    """
    
    @staticmethod
    async def run():
        clear_console()

        all_ids_from_wall = []
        account = 0
        for access_token in access_tokens:
            account += 1
            print(f'[purple]-------------------Аккаунт: {account}-------------------[/purple]')

            all_ids_from_get_requests = []
            all_ids_from_wall_filtered = []
            offset = 0

            get_request = GetRequests()
            friends_add = FriendsAdd()
            delete_all_requests = DeleteAllRequests()
            wall = WallGet()
            user = UsersGet()
            file = File()

            try:
                print('[yellow]Получаю список новых заявок в друзья...[/yellow]')

                one_request = await get_request.get_one_with_need_viewed_false(access_token)

                while offset < one_request['response']['count']:
                    all_requests = await get_request.get_all_with_need_viewed_false(access_token, offset)
                    for one_id in all_requests['response']['items']:
                        all_ids_from_get_requests.append(one_id)
                    offset += 1000

                if len(all_ids_from_get_requests) <= 0:
                    print('[red]Не найдено новых заявок в друзья[/red]')

                if len(all_ids_from_get_requests) > 0:
                    print(f'[yellow]Найдено {len(all_ids_from_get_requests)} новых заявок в друзья[/yellow]')
                    print('[yellow]Начинаю принимать...[/yellow]')

                    for one_id in all_ids_from_get_requests:
                        support_us()
                        try:
                            await friends_add.add_without_captcha(access_token, one_id)
                            print(f'[blue]id{one_id}[/blue]: принял')
                        except CannotAddThisUserToFriendsAsUserNotFound as e:
                            print(f'[red]id{one_id}[/red]: {e}')

                    await delete_all_requests.delete_all_requests(access_token)

                    print('[yellow]Закончил принимать[/yellow]')

                if len(all_ids_from_wall) == 0:
                    print(f'[yellow]Получаю список записей...[/yellow]')
                    for group in groups:
                        offset = 0
                        while offset < records:
                            records_from_wall = await wall.get(access_token, group, offset)
                            for one_id in records_from_wall['response']['items']:
                                all_ids_from_wall.append(one_id['from_id'])
                            offset += 100
                    all_ids_from_wall = list(set(all_ids_from_wall))

                if len(all_ids_from_wall) == 0:
                    raise ThereAreNoEntriesInThisPageOrGroup

                print('[yellow]Получил список записей[/yellow]')
                print('[yellow]Идет фильтрация...[/yellow]')

                for one_id in all_ids_from_wall:
                    try:
                        checking_for_friendship_status = await user.get_with_friend_status(access_token, one_id)
                        if checking_for_friendship_status['response'][0]['friend_status'] == 0:
                            all_ids_from_wall_filtered.append(one_id)
                    except TooManyRequestsPerSecond as e:
                        print(f'[red]{e}[/red]')

                print('[yellow]Фильтрация закончена[/yellow]')
                print('[yellow]Начинаю добавлять...[/yellow]')

                for one_id in all_ids_from_wall_filtered:
                    support_us()
                    try:
                        result = await friends_add.add_without_captcha(access_token, one_id)
                        if result['response'] == 1:
                            print(f'[blue]id{one_id}[/blue]: отправил заявку')
                        elif result['response'] == 2:
                            print(f'[blue]id{one_id}[/blue]: уже в друзьях')
                        else:
                            print(f'[blue]id{one_id}[/blue]: повторная отправка заявки')
                    except LimitOfFriendAdditions as e:
                        print(f'[green]id{one_id}: {e}[/green]')
                        break
                    except CaptchaNeeded:
                        captcha_sid = await file.reader_captcha_sid()
                        captcha_key = input(f'https://api.vk.com/captcha.php?sid={captcha_sid}\nВведите код с капчи: ')
                        result_with_captcha = await friends_add.add_with_captcha(access_token, one_id,
                                                                                 captcha_sid, captcha_key)
                        if result_with_captcha['response'] == 1:
                            print(f'[blue]id{one_id}[/blue]: отправил заявку')
                        elif result_with_captcha['response'] == 2:
                            print(f'[blue]id{one_id}[/blue]: уже в друзьях')
                        else:
                            print(f'[blue]id{one_id}[/blue]: повторная отправка заявки')
                    except CannotAddThisUserToFriendsAsTheyHavePutYouOnTheirBlacklist as e:
                        print(f'[red]id{one_id}: {e}[/red]')
                    except CannotAddThisUserToFriendsAsYouPutHimOnBlacklist as e:
                        print(f'[red]id{one_id}: {e}[/red]')
                    except CannotAddThisUserToFriendsAsUserNotFound as e:
                        print(f'[red]id{one_id}: {e}[/red]')

            except VKTokenError as e:
                print(f'[red]{e}[/red]')
            except ThereAreNoEntriesInThisPageOrGroup as e:
                print(f'[red]{e}[/red]')
            except UnknownError as e:
                print(f'[red]{e}[/red]')
            except VKServerIsNotResponding as e:
                print(f'[red]{e}[/red]')
