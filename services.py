from typing import Any

import requests

from models import DefaultTexts
from config import logger

PROTOCOL = 'http'
HOST_NAME = '127.0.0.1'
PORT = '8000'


class APITextInterface:
    api = f'{PROTOCOL}://{HOST_NAME}:{PORT}/api/text/'

    @classmethod
    @logger.catch
    def get_start_text(cls):
        data = requests.get(f'{cls.api}start')
        data = data.json()
        return data.get('text', DefaultTexts.start)

    @classmethod
    @logger.catch
    def get_about_text(cls):
        data = requests.get(f'{cls.api}about')
        data = data.json()
        return data.get('text', DefaultTexts.about)

    @classmethod
    @logger.catch
    def get_prices_text(cls):
        data = requests.get(f'{cls.api}prices/')
        data = data.json()
        return data.get('text', DefaultTexts.prices)

    @classmethod
    @logger.catch
    def get_reviews_text(cls):
        data = requests.get(f'{cls.api}reviews/')
        data = data.json()
        return data.get('text', DefaultTexts.reviews)

    @classmethod
    @logger.catch
    def get_for_mailing_text(cls):
        data = requests.get(f'{cls.api}mailing/')
        data = data.json()
        return data.get('text', DefaultTexts.for_mailing)

    @classmethod
    @logger.catch
    def get_want_for_challenger_text(cls):
        data = requests.get(f'{cls.api}want_club_challenger/')
        data = data.json()
        return data.get('text', DefaultTexts.start)

    @classmethod
    @logger.catch
    def get_want_for_get_phone_text(cls):
        data = requests.get(f'{cls.api}contact/')
        data = data.json()
        return data.get('text', DefaultTexts.for_get_phone)

    @classmethod
    @logger.catch
    def get_want_for_entered_text(cls):
        data = requests.get(f'{cls.api}want_club_for_entered/')
        data = data.json()
        return data.get('text', DefaultTexts.for_entered)

    @classmethod
    @logger.catch
    def get_want_for_entered_got_link_text(cls):
        data = requests.get(f'{cls.api}want_club_for_got_link/')
        data = data.json()
        return data.get('text', DefaultTexts.for_entered_got_link)

    @classmethod
    @logger.catch
    def get_want_for_excluded_text(cls):
        data = requests.get(f'{cls.api}want_club_for_excluded/')
        data = data.json()
        return data.get('text', DefaultTexts.for_excluded)

    @classmethod
    @logger.catch
    def get_want_for_waiting_list_text(cls):
        data = requests.get(f'{cls.api}want_club_for_waiting_list/')
        data = data.json()

    @classmethod
    @logger.catch
    def get_link_waiting_list_text(cls):
        data = requests.get(f'{cls.api}waiting_list_link/')
        data = data.json()
        return data.get('text', DefaultTexts.for_waiting_list)

    @classmethod
    @logger.catch
    def get_for_invite_text(cls):
        data = requests.get(f'{cls.api}invite/')
        data = data.json()
        return data.get('text', DefaultTexts.for_invite)

    @classmethod
    @logger.catch
    def get_link_to_pay(cls):
        data = requests.get(f'{cls.api}pay_link/')
        data = data.json()
        return data.get('text', DefaultTexts.for_invite)
    # text/want_club/


class APIGetcourseGroupInterface:
    api = f'{PROTOCOL}://{HOST_NAME}:{PORT}/api/getcourse_group/'

    @classmethod
    @logger.catch
    def get_getcourse_groups(cls) -> dict:
        data = requests.get(f'{cls.api}get')
        data = data.json()
        return data


class APIMessageNewStatusInterface:
    api = f'{PROTOCOL}://{HOST_NAME}:{PORT}/api/message_new_status/'

    @classmethod
    @logger.catch
    def get_messages(cls) -> dict:
        data = requests.get(f'{cls.api}get')
        data = data.json()
        return data

    @classmethod
    @logger.catch
    def set_getcourse_group(cls, group_name: str, group_id: int) -> bool:
        data = {"group_id": group_id}
        result = requests.post(f'{cls.api}set/{group_name}', json=data)
        if result.status_code == 201:
            return True
        logger.error(f'{result.text}')
        return result.json()


class APIChannelsInterface:
    api = f'{PROTOCOL}://{HOST_NAME}:{PORT}/api/channels/'

    @classmethod
    @logger.catch
    def get_channels(cls) -> dict:
        data = requests.get(f'{cls.api}get/')
        data = data.json()
        return data

    @classmethod
    @logger.catch
    def add_channel(cls, name: str, channel_id: int) -> Any:
        data = {name: name, channel_id: channel_id}
        result = requests.post(f'{cls.api}add_channel/', data=data)
        reslut = result.json()
        return reslut

    @classmethod
    @logger.catch
    def delete_channel(cls, channel_id: int) -> Any:
        data = {channel_id: channel_id}
        result = requests.post(f'{cls.api}delete/', data=data)
        if result.status_code == 204:
            return True
        logger.error(f'{result.text}')
        return False


class APIUsersInterface:
    api = f'{PROTOCOL}://{HOST_NAME}:{PORT}/api/users/'

    @classmethod
    @logger.catch
    def get_users_by_telegram_id(cls, telegram_id: int) -> dict:
        data = requests.get(f'{cls.api}get_users_by_telegram_id/{telegram_id}')
        data = data.json()
        return data

    @classmethod
    @logger.catch
    def get_users_from_waiting_list(cls) -> dict:
        data = requests.get(f'{cls.api}get_users_from_waiting_list/')
        data = data.json()
        return data

    @classmethod
    @logger.catch
    def add_challenger(cls, phone: str, telegram_id: int) -> dict:
        data = {"phone": phone, "telegram_id": telegram_id}
        result = requests.post(f'{cls.api}add_challenger/', json=data)
        result = result.json()
        return result

    @classmethod
    @logger.catch
    def got_invited(cls, telegram_id: int) -> dict:
        result = requests.put(f'{cls.api}got_invited/{telegram_id}')
        result = result.json()
        return result


class APIGroupInterface:
    api = f'{PROTOCOL}://{HOST_NAME}:{PORT}/api/groups/'

    @classmethod
    @logger.catch
    def get_all_group_channel(cls) -> dict:
        data = requests.get(f'{cls.api}get')
        data = data.json()
        return data

    @classmethod
    def set_getcourse_group(cls, getcourse_group: str) -> bool:
        data = requests.post(f'{cls.api}set/{getcourse_group}')
        data = data.json()
        return data
