import allure
import pytest

from test_data.test_data_generator import CreateAnnouncement

from methods.announcement_method import AnnouncementMethods


class TestAd:

    @allure.title('Проверка успешного создания объявления')
    def test_create_new_announcement(self, log_user):
        status_code, response = log_user
        token = response['token']['access_token']
        am = AnnouncementMethods()
        status_code, response = am.create_new_announcement(token)
        assert status_code == 201 and response['id']


    @allure.title('Проверка создания объявления без авторизации')
    def test_create_new_announcement_without_authorization(self):
        am = AnnouncementMethods()
        status_code, response = am.create_new_announcement_failed()
        assert status_code == 401


    @pytest.mark.parametrize(
        "payload", [
            {'name': CreateAnnouncement.get_name(),
             'category': 'Вещи',
             'condition': 'Б/у',
             'city': 'Санкт-Петербург',
             'description': CreateAnnouncement.get_description(),
             'price': CreateAnnouncement.get_price()
             }
        ]
    )

    @allure.title('Проверка редактирования объявления')
    def test_edit_ad(self, payload, log_user):
        _, response = log_user
        token = response['token']['access_token']
        am = AnnouncementMethods()
        _, response = am.create_new_announcement(token)
        id_add = response['id']
        status_code, response = am.edit_announcement(token, id_add, payload)
        assert status_code == 200


    @pytest.mark.parametrize(
        "payload", [
            {'name': CreateAnnouncement.get_name(),
             'category': 'Вещи',
             'condition': 'Б/у',
             'city': 'Санкт-Петербург',
             'description': CreateAnnouncement.get_description(),
             'price': CreateAnnouncement.get_price()
             }
        ]
    )
    @allure.title('Проверка редактирования объявления другого пользователя')
    def test_edit_announcement_of_another_user(self, payload, log_user):
        _, response = log_user
        token = response['token']['access_token']
        am = AnnouncementMethods()
        status_code, response = am.edit_announcement_of_another_user(token, payload)
        assert status_code == 401 and response == {"message": "Оффер не найден или у вас нет прав на его редактирование",
                                                   "error": "Unauthorized", "statusCode": 401}


    @allure.title('Проверка удаления объявления')
    def test_delete_ad(self, log_user):
        _, response = log_user
        token = response['token']['access_token']
        am = AnnouncementMethods()
        _, response = am.create_new_announcement(token)
        id_add = response['id']
        status_code, response = am.delete_announcement(token, id_add)
        assert status_code == 200 and response == {'message': 'Объявление удалено успешно'}
