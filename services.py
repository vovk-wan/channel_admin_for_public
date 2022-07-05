import requests
from models import DefaultTexts
PROTOCOL = 'http'
HOST_NAME = '127.0.0.1'
PORT = '8000'


class APITextInterface:
    api = f'{PROTOCOL}://{HOST_NAME}:{PORT}/api/'

    @classmethod
    def get_start_text(cls):
        data = requests.get(f'{cls.api}text/start')
        data = data.json()
        return data.get('text', DefaultTexts.start)

    @classmethod
    def get_about_text(cls):
        data = requests.get(f'{cls.api}text/about')
        data = data.json()
        return data.get('text', DefaultTexts.start)

    @classmethod
    def get_prices_text(cls):
        data = requests.get(f'{cls.api}text/prices/')
        data = data.json()
        return data.get('text', DefaultTexts.start)

    @classmethod
    def get_reviews_text(cls):
        data = requests.get(f'{cls.api}text/reviews/')
        data = data.json()
        return data.get('text', DefaultTexts.start)

    @classmethod
    def get_mailing_text(cls):
        data = requests.get(f'{cls.api}text/mailing/')
        data = data.json()
        return data.get('text', DefaultTexts.start)

    @classmethod
    def get_want_for_challenger_text(cls):
        data = requests.get(f'{cls.api}text/want_club_challenger/')
        data = data.json()
        return data.get('text', DefaultTexts.start)

    @classmethod
    def get_want_for_get_phone_text(cls):
        data = requests.get(f'{cls.api}text/contact/')
        data = data.json()
        return data.get('text', DefaultTexts.start)

    @classmethod
    def get_want_for_entered_text(cls):
        data = requests.get(f'{cls.api}text/want_club_for_entered/')
        data = data.json()
        return data.get('text', DefaultTexts.start)

    @classmethod
    def get_want_for_entered_got_link_text(cls):
        data = requests.get(f'{cls.api}text/want_club_for_got_link/')
        data = data.json()
        return data.get('text', DefaultTexts.start)

    @classmethod
    def get_want_for_excluded_text(cls):
        data = requests.get(f'{cls.api}text/want_club_for_excluded/')
        data = data.json()
        return data.get('text', DefaultTexts.start)

    @classmethod
    def get_want_for_waiting_list_text(cls):
        data = requests.get(f'{cls.api}text/waiting_list_link/')
        data = data.json()
        return data.get('text', DefaultTexts.start)

    @classmethod
    def get_for_invite_text(cls):
        data = requests.get(f'{cls.api}text/invite/')
        data = data.json()
        return data.get('text', DefaultTexts.start)


    # text/want_club/

    # text/pay_link/
