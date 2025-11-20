import allure
import pytest

from test_data.test_data_generator import CreateUsers
from methods.user_method import UsersMethods


class TestUserMethods:

    @allure.title('Проверка успешной регистрации нового пользователя')
    def test_registration_new_user(self):
        um = UsersMethods()
        status_code, response = um.new_registration_user()
        assert status_code == 201 and response['access_token']

    @allure.title('Проверка регистрации дубля нового пользователя')
    def test_re_registration_user(self):
        um = UsersMethods()
        # Используем один и тот же email и password для всех регистраций
        email = CreateUsers.get_email()
        password = CreateUsers.get_password()
        um.new_registration_user(email=email, password=password)
        um.new_registration_user(email=email, password=password)
        status_code, response = um.new_registration_user(email=email, password=password)
        assert status_code == 400 and response == {'message': 'Почта уже используется',
                                                   'statusCode': 400}

    @pytest.mark.parametrize(
        "payload", [
            {'email': '', 'password': '', 'submitPassword': ''},
            {'email': '', 'password': CreateUsers.get_password(), 'submitPassword': CreateUsers.get_password()},
            {'email': '', 'password': CreateUsers.get_password(), 'submitPassword': ''}
        ]
    )

    @allure.title('Проверка неуспешной регистрации нового пользователя')
    def test_registration_new_user_failed(self, payload):
        um = UsersMethods()
        status_code, response = um.registration_user_fail(payload)
        assert status_code == 400 and response == {'message': ['error: Не валидный Email'],
                                                   'statusCode': 400}


    @allure.title('Проверка успешной авторизации пользователя')
    def test_authorization_user(self):
        um = UsersMethods()
        # Используем одни и те же email и password для регистрации и авторизации
        email = CreateUsers.get_email()
        password = CreateUsers.get_password()
        um.new_registration_user(email=email, password=password)
        status_code, response = um.auth_user(email=email, password=password)
        assert status_code == 201 and response['token']


    @pytest.mark.parametrize(
        "payload", [
            {'email': CreateUsers.get_email(), 'password': ''},
            {'email': '', 'password': CreateUsers.get_password()}
        ]
    )

    @allure.title('Проверка неуспешной авторизации пользователя')
    def test_authorization_user_failed(self, payload):
        um = UsersMethods()
        um.new_registration_user()
        status_code, response = um.auth_user_failed(payload)
        assert status_code == 404 and response == {'message': 'Логин или пароль неверны',
                                                   'statusCode': 404}
