import datetime
import time
import asyncio
from typing import Tuple, Dict
import json

import requests

from config import ACCOUNT_NAME, SECRET_KEY, logger

PERSONS_FILE = 'person_save.json'
GROUPS_FILE = 'group_save.json'


def make_groups_list() -> Tuple:
    """
    Функция получает список групп с API
    :return:
    """
    headers = {'content-type': 'multipart/form-data'}
    url = f'https://{ACCOUNT_NAME}.getcourse.ru/pl/api/account/groups?key={SECRET_KEY}'
    try:
        response = requests.get(url=url, headers=headers, timeout=30)
        if response.status_code != 200:
            logger.error(f'module: getsource_requests {response.text} requests/group')
            return tuple()
        data = response.json()

        # записываем в json
        # TODO или добавить параметр, или удалить
        # with open(GROUPS_FILE, 'w', encoding='utf8') as file_save:
        #     json.dump(data, file_save, ensure_ascii=False, indent=4)
        # # TODO end или добавить параметр, или удалить
    except Exception as exc:
        logger.error(f'{exc.__traceback__.tb_frame}\n{exc}')
        return tuple()

    if data.get('error'):
        return tuple()

    return tuple(data.get('info', []))


def make_user_list_by_group(group_id) -> Tuple:
    """
    Функция отправляет запрос на создание списка активных пользователей определенной группы API
    :param group_id: идентификатор нужной группы.
    :return:
    """

    headers = {'content-type': 'multipart/form-data'}
    filter_name = 'status'
    filter_value = 'active'
    url = f'https://{ACCOUNT_NAME}.getcourse.ru' \
          f'/pl/api/account/groups/{group_id}/users?key={SECRET_KEY}&{filter_name}={filter_value}'
    export_id = None
    try:
        response = requests.get(url=url, headers=headers, timeout=30)
        if response.status_code != 200:
            logger.error(f'module: getcourse_requests requests/user filter {filter_name}:{filter_value}')
            return tuple()
        data = response.json()
    except Exception as exc:
        logger.error(f'{exc.__traceback__.tb_frame}\n{exc}')
        return tuple()
    if not data.get('error'):
        export_id = data.get('info', {}).get('export_id')

    return export_id, datetime.datetime.utcnow()


@logger.catch
async def get_data(export_id: int, count_limit: int, group_name: str) -> Dict:
    """
    Функция получает список пользователей по id созданного на сервере файла экспорта
    :param export_id:
    :param count_limit:
    :param group_name:
    :return:
    """

    headers = {'content-type': 'multipart/form-data'}

    url = f'https://{ACCOUNT_NAME}.getcourse.ru/pl/api/account/exports/{export_id}?key={SECRET_KEY}'
    count = 0
    error = True
    start = time.time()
    while error:
        await asyncio.sleep(120)
        count += 1

        try:
            response = requests.get(url=url, headers=headers, timeout=30)
            if response.status_code != 200 or count >= count_limit:
                logger.error(f'module: getcourse_requests requests/get_data {export_id}')
                return {
                    'count_requests': count,
                    'time': time.time() - start,
                    'data': tuple(),
                    'error': True
                }
            data = response.json()

            # записываем в json
            # TODO или добавить параметр, или удалить
            with open(f'{group_name}{PERSONS_FILE}', 'w', encoding='utf8') as file_save:
                json.dump(data, file_save, ensure_ascii=False, indent=4)
            # TODO end или добавить параметр, или удалить
        except Exception as exc:
            logger.error(f'{exc.__traceback__.tb_frame}\n{exc}')

            return {
                'count_requests': count, 'time': time.time() - start, 'data': tuple(), 'error': True
            }

        error = data.get('error')
        logger.info(f'response: {response}\n count: {count}', )
        if error:
            return {
                'count_requests': count,
                'time': time.time() - start,
                'data': tuple(),
                'error': True
            }
        logger.info(f'time for request get data: {time.time() - start}')

        persons = data.get('info', {}).get('items', [])
        user_data = []
        unique = []
        for person in persons:
            if person[7] and person[7][-10:] not in unique:
                user_data.append({'getcourse_id': person[0], 'phone': person[7]})
                unique.append(person[7][-10:])

        return {'count_requests': count, 'time': time.time() - start, 'data': user_data, 'error': False}


#  ########################## fake func for test ################################  #
def make_user_list_test(x=1) -> Tuple:
    if x:
        return x, datetime.datetime.utcnow()
    return tuple()
