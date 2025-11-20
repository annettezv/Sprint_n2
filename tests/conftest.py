import pytest
import allure

from test_data.test_data_generator import CreateUsers
from methods.user_method import UsersMethods


@pytest.fixture
def user_credentials():
    """Фикстура для генерации учетных данных пользователя (один раз на тест)"""
    return {
        'email': CreateUsers.get_email(),
        'password': CreateUsers.get_password()
    }


@pytest.fixture
@allure.step('Регистрация пользователя')
def user_registration(user_credentials):
    """Фикстура для регистрации нового пользователя"""
    um = UsersMethods()
    status_code, response = um.new_registration_user(
        email=user_credentials['email'],
        password=user_credentials['password']
    )
    return status_code, response


@pytest.fixture
@allure.step('Регистрация и авторизация пользователя')
def log_user(user_credentials):
    """Фикстура для регистрации и авторизации пользователя"""
    um = UsersMethods()
    # Сначала регистрируем пользователя
    um.new_registration_user(
        email=user_credentials['email'],
        password=user_credentials['password']
    )
    # Затем авторизуем
    status_code, response = um.auth_user(
        email=user_credentials['email'],
        password=user_credentials['password']
    )
    return status_code, response

