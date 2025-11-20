import allure
import requests

from configs.urls import Urls
from test_data.test_data_generator import CreateUsers


class UsersMethods:


    @allure.step('Регистрация нового пользователя')
    def new_registration_user(self, email=None, password=None):
        if email is None:
            email = CreateUsers.get_email()
        if password is None:
            password = CreateUsers.get_password()
        payload = {
            'email': email,
            'password': password,
            'submitPassword': password
        }
        response = requests.post(f'{Urls.BASE}{Urls.REGISTRATION}', json=payload)
        return response.status_code, response.json()


    @allure.step('Регистрация нового пользователя с не полными данными')
    def registration_user_fail(self, payload):
        response = requests.post(f'{Urls.BASE}{Urls.REGISTRATION}', json=payload)
        return response.status_code, response.json()


    @allure.step('Авторизация пользователя')
    def auth_user(self, email=None, password=None):
        if email is None:
            email = CreateUsers.get_email()
        if password is None:
            password = CreateUsers.get_password()
        payload = {
            'email': email,
            'password': password
        }
        response = requests.post(f'{Urls.BASE}{Urls.AUTHORIZATION}', json=payload)
        return response.status_code, response.json()


    @allure.step('Авторизация пользователя с не полными данными')
    def auth_user_failed(self, payload):
        response = requests.post(f'{Urls.BASE}{Urls.AUTHORIZATION}', json=payload)
        return response.status_code, response.json()

