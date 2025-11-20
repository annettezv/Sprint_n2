import allure
import requests

from configs.urls import Urls
from requests_toolbelt.multipart.encoder import MultipartEncoder

from test_data.test_data_generator import CreateAnnouncement


class AnnouncementMethods:

    @allure.step('Успешное создание объявления')
    def create_new_announcement(self, token):
        payload = MultipartEncoder(
            fields={
                'name': CreateAnnouncement.get_name(),
                'category': 'Вещи',
                'condition': 'Б/у',
                'city': 'Санкт-Петербург',
                'description': CreateAnnouncement.get_description(),
                'price': CreateAnnouncement.get_price()
            }
        )

        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": payload.content_type
        }

        response = requests.post(f'{Urls.BASE}{Urls.NEW_ANNOUNCEMENT}', headers=headers, data=payload)
        return response.status_code, response.json()

    @allure.step('Создание объявления без авторизации')
    def create_new_announcement_failed(self):
        payload = MultipartEncoder(
            fields={
                'name': CreateAnnouncement.get_name(),
                'category': 'Вещи',
                'condition': 'Б/у',
                'city': 'Санкт-Петербург',
                'description': CreateAnnouncement.get_description(),
                'price': CreateAnnouncement.get_price()
            }
        )
        response = requests.post(f'{Urls.BASE}{Urls.NEW_ANNOUNCEMENT}', data=payload)
        return response.status_code, response.json()


    @allure.step('Редактирование созданного объявления')
    def edit_announcement(self, token, id_add, payload):
        headers = {
            "Authorization": f"Bearer {token}"
        }
        response = requests.patch(f'{Urls.BASE}{Urls.ANNOUNCEMENT_EDIT}{id_add}', headers=headers, json=payload)
        return response.status_code, response.json()


    @allure.step('Редактирование объявления другого пользователя')
    def edit_announcement_of_another_user(self, token, payload):
        response = requests.get(f'{Urls.BASE}{Urls.ALL_ANNOUNCEMENTS}')
        data = response.json()
        id_add = data['offers'][0]['id']
        headers = {
            "Authorization": f"Bearer {token}"
        }
        response = requests.patch(f'{Urls.BASE}{Urls.ANNOUNCEMENT_EDIT}{id_add}', headers=headers, json=payload)
        return response.status_code, response.json()


    @allure.step('Удаление созданного объявления')
    def delete_announcement(self, token, id):
        headers = {
            "Authorization": f"Bearer {token}"
        }
        response = requests.delete(f'{Urls.BASE}{Urls.ANNOUNCEMENT_DEL}{id}', headers=headers)
        # Обработка случая, когда ответ не содержит JSON
        try:
            response_json = response.json()
        except ValueError:
            response_json = response.text if response.text else {}
        return response.status_code, response_json
