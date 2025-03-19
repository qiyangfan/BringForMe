import json

from rest_framework.test import (APITestCase)

from BringForMe import settings
from .models import User

base_url = '/api/{version}/'.format(version=settings.REST_FRAMEWORK['DEFAULT_VERSION'])
app_base_url = 'user/'


def get_url(url):
    return base_url + app_base_url + url


class RegisterTestCase(APITestCase):

    def setUp(self):
        pass

    def test_register(self):
        request_data = {
            "username": "qiyangfan",
            "password": "Password@123",
            "confirm_password": "Password@123",
            "nickname": "qiyangfan",
        }
        response = self.client.post(get_url("register/"), json.dumps(request_data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        user = User.objects.get(username='qiyangfan')
        self.assertIsNotNone(user)
        response = self.client.post(get_url("register/"), json.dumps(request_data), content_type='application/json')
        self.assertEqual(response.status_code, 422)

    def test_register_inconsistent(self):
        request_data = {
            "username": "qiyangfan",
            "password": "Password@123",
            "confirm_password": "Password@456",
            "nickname": "qiyangfan",
        }
        response = self.client.post(get_url("register/"), json.dumps(request_data), content_type='application/json')
        self.assertEqual(response.status_code, 422)

    def test_register_simple_password(self):
        request_data = {
            "username": "qiyangfan",
            "password": "123456",
            "confirm_password": "123456",
            "nickname": "qiyangfan"
        }
        response = self.client.post(get_url("register/"), json.dumps(request_data), content_type='application/json')
        self.assertEqual(response.status_code, 422)


def setup_register(cls):
    request_data = {
        "username": "qiyangfan",
        "password": "Password@123",
        "confirm_password": "Password@123",
        "nickname": "qiyangfan",
    }
    response = cls.client.post(get_url("register/"), json.dumps(request_data), content_type='application/json')
    cls.assertEqual(response.status_code, 200)
    user = User.objects.get(username='qiyangfan')
    cls.assertIsNotNone(user)


class LoginTestCase(APITestCase):

    def setUp(self):
        setup_register(self)

    def test_login(self):
        request_data = {
            "username": "qiyangfan",
            "password": "Password@123",
        }
        response = self.client.post(get_url("token/"), json.dumps(request_data), content_type='application/json')
        self.assertEqual(response.status_code, 200)


def setup_login(cls):
    request_data = {
        "username": "qiyangfan",
        "password": "Password@123",
    }
    response = cls.client.post(get_url("token/"), json.dumps(request_data), content_type='application/json')
    cls.assertEqual(response.status_code, 200)
    return {'Authorization': 'Bearer {}'.format(response.data['access'])}


class ChangePasswordTestCase(APITestCase):

    def setUp(self):
        setup_register(self)
        self.headers = setup_login(self)

    def test_change_password(self):
        request_data = {
            "old_password": "Password@123",
            "new_password": "Password@456",
            "confirm_new_password": "Password@456"
        }
        response = self.client.patch(get_url("password/"), json.dumps(request_data), content_type='application/json',
                                     headers=self.headers)
        self.assertEqual(response.status_code, 200)

    def test_change_password_wrong_old_password(self):
        request_data = {
            "old_password": "Password@456",
            "new_password": "Password@123",
            "confirm_new_password": "Password@123"
        }
        response = self.client.patch(get_url("password/"), json.dumps(request_data), content_type='application/json',
                                     headers=self.headers)
        self.assertEqual(response.status_code, 422)

    def test_change_password_inconsistent(self):
        request_data = {
            "old_password": "Password@123",
            "new_password": "Password@456",
            "confirm_new_password": "Password@789"
        }
        response = self.client.patch(get_url("password/"), json.dumps(request_data), content_type='application/json',
                                     headers=self.headers)
        self.assertEqual(response.status_code, 422)

    def test_change_password_simple_new_password(self):
        request_data = {
            "old_password": "Password@123",
            "new_password": "123456",
            "confirm_new_password": "123456"
        }
        response = self.client.patch(get_url("password/"), json.dumps(request_data), content_type='application/json',
                                     headers=self.headers)
        self.assertEqual(response.status_code, 422)


class AddressCreateReadTestCase(APITestCase):

    def setUp(self):
        setup_register(self)
        self.headers = setup_login(self)

    def test_address_create_and_read(self):
        request_data = {
            "tag": "home",
            "country": "China",
            "province": "Shanghai",
            "city": "Shanghai",
            "address": "No. 800 Dongchuan Road, Minhang District",
            "remark": "Near Dongchuan Road Station",
            "postcode": "200240",
            "contact_person": "Qiyang Fan",
            "country_code": "+86",
            "phone": "13900000000",
            "is_default": True
        }
        response = self.client.post(get_url("address/"), json.dumps(request_data), content_type='application/json',
                                    headers=self.headers)
        self.assertEqual(response.status_code, 200)
        response = self.client.get(get_url("address/"), headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['data']), 1)


def setup_create_and_read_address(cls):
    request_data = {
        "tag": "home",
        "country": "China",
        "province": "Shanghai",
        "city": "Shanghai",
        "address": "No. 800 Dongchuan Road, Minhang District",
        "remark": "Near Dongchuan Road Station",
        "postcode": "200240",
        "contact_person": "Qiyang Fan",
        "country_code": "+86",
        "phone": "13900000000",
        "is_default": True
    }
    response = cls.client.post(get_url("address/"), json.dumps(request_data), content_type='application/json',
                               headers=cls.headers)
    cls.assertEqual(response.status_code, 200)
    response = cls.client.get(get_url("address/"), headers=cls.headers)
    cls.assertEqual(response.status_code, 200)
    cls.assertEqual(len(response.data['data']), 1)
    return response.data['data'][0]['id']


class AddressUpdateAndDeleteTestCase(APITestCase):

    def setUp(self):
        setup_register(self)
        self.headers = setup_login(self)
        self.address_id = setup_create_and_read_address(self)

    def test_address_update(self):
        request_data = {
            "id": 1,
            "tag": "school",
            "country": "China",
            "province": "Shanghai",
            "city": "Shanghai",
            "address": "No. 800 Dongchuan Road, Minhang District",
            "remark": "Near Dongchuan Road Station",
            "postcode": "200240",
            "contact_person": "Qiyang Fan",
            "country_code": "+86",
            "phone": "13900000000",
            "is_default": True
        }
        response = self.client.patch(get_url("address/{address_id}/".format(address_id=self.address_id)),
                                     json.dumps(request_data),
                                     content_type='application/json',
                                     headers=self.headers)
        self.assertEqual(response.status_code, 200)
        response = self.client.get(get_url("address/?address_id=1"),
                                   headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['data'][0]['tag'], 'school')

    def test_address_delete(self):
        response = self.client.delete(get_url("address/{address_id}/".format(address_id=self.address_id)),
                                      content_type='application/json',
                                      headers=self.headers)
        self.assertEqual(response.status_code, 200)
        response = self.client.get(get_url("address/"), headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['data']), 0)


class ProfileTestCase(APITestCase):
    def setUp(self):
        setup_register(self)
        self.headers = setup_login(self)

    def test_get_current_user_profile(self):
        response = self.client.get(get_url("profile/"), headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['data']['username'], 'qiyangfan')

    def test_change_profile(self):
        request_data = {
            "nickname": "Yangfan Qi",
        }
        response = self.client.patch(get_url("profile/"), json.dumps(request_data), content_type='application/json',
                                     headers=self.headers)
        self.assertEqual(response.status_code, 200)
        response = self.client.get(get_url("profile/"), headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['data']['nickname'], 'Yangfan Qi')


def setup_register_second(cls):
    request_data = {
        "username": "zhangruixiang",
        "password": "Password@123",
        "confirm_password": "Password@123",
        "nickname": "zhangruixiang",
    }
    response = cls.client.post(get_url("register/"), json.dumps(request_data), content_type='application/json')
    cls.assertEqual(response.status_code, 200)
    user = User.objects.get(username='zhangruixiang')
    cls.assertIsNotNone(user)


class OtherUserProfileTestCase(APITestCase):
    def setUp(self):
        setup_register(self)
        setup_register_second(self)
        self.headers = setup_login(self)

    def test_get_other_user_profile(self):
        response = self.client.get(get_url("profile/{user_id}/".format(user_id=2)),
                                   headers=self.headers)
        print(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['data']['nickname'], 'zhangruixiang')


class BatchUserProfileTestCase(APITestCase):
    def setUp(self):
        setup_register(self)
        setup_register_second(self)
        self.headers = setup_login(self)

    def test_get_other_user_profile(self):
        request_data = {
            "user_ids": [1, 2],
        }
        response = self.client.post(get_url("batch-profile/"), json.dumps(request_data),
                                    content_type='application/json', headers=self.headers)
        print(response.data)
        self.assertEqual(response.status_code, 200)
