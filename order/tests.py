import json

from rest_framework.test import (APITestCase)

from BringForMe import settings
from user.tests import setup_register, setup_login,setup_register_second

base_url = '/api/{version}/'.format(version=settings.REST_FRAMEWORK['DEFAULT_VERSION'])
app_base_url = 'order/'


def get_url(url):
    return base_url + app_base_url + url


class OrderCreateReadTestCase(APITestCase):

    def setUp(self):
        setup_register(self)
        self.headers = setup_login(self)

    def test_create_order(self):
        request_data = {
            "destination": {
                "tag": "home",
                "country": "China",
                "province": "安徽省",
                "city": "武林市",
                "address": "河北省 海京市 西丰县 禄桥94432号 5号房间",
                "remark": "",
                "postcode": "720286",
                "contact_person": "Yangfan Qi",
                "country_code": "86",
                "phone": "77303461583",
            },
            "description": "buy a book",
            "commission": 5,
            "status": 0,
            "user_id": 1,
            "image_ids": []
        }
        response = self.client.post(get_url(''), json.dumps(request_data), content_type='application/json',
                                    headers=self.headers)
        self.assertEqual(response.status_code, 200)

    def test_query_order(self):
        response = self.client.get(get_url(''), headers=self.headers)
        self.assertEqual(response.status_code, 200)


def setup_create_order(cls):
    request_data = {
        "destination": {
            "tag": "home",
            "country": "China",
            "province": "安徽省",
            "city": "武林市",
            "address": "河北省 海京市 西丰县 禄桥94432号 5号房间",
            "remark": "",
            "postcode": "720286",
            "contact_person": "Yangfan Qi",
            "country_code": "86",
            "phone": "77303461583",
        },
        "description": "buy a book",
        "commission": 5,
        "status": 0,
        "user_id": 1,
        "image_ids": []
    }
    response = cls.client.post(get_url(''), json.dumps(request_data), content_type='application/json',
                               headers=cls.headers)
    cls.assertEqual(response.status_code, 200)


class OrderUpdateDeleteTestCase(APITestCase):

    def setUp(self):
        setup_register(self)
        setup_register_second(self)
        self.headers = setup_login(self)
        setup_create_order(self)

    def test_update_order(self):
        response = self.client.get(get_url(''.format()), headers=self.headers)
        print(response.data)
        order_id = response.data['data'][0]['id']
        request_data = {
            "commission": 10,
        }
        response = self.client.patch(get_url('{order_id}/'.format(order_id=order_id)), json.dumps(request_data),
                                     content_type='application/json',
                                     headers=self.headers)
        self.assertEqual(response.status_code, 200)
        response = self.client.get(get_url(''), headers=self.headers)
        commission = response.data['data'][0]['commission']
        self.assertEqual(commission, 10)

    def test_delete_order(self):
        response = self.client.get(get_url(''.format()), headers=self.headers)
        order_id = response.data['data'][0]['id']
        response = self.client.delete(get_url('{order_id}/'.format(order_id=order_id)), headers=self.headers)
        self.assertEqual(response.status_code, 200)
        response = self.client.get(get_url(""), {'order_id': order_id}, headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['data']), 0)

    def test_delete_accepted(self):
        response = self.client.get(get_url(''.format()), headers=self.headers)
        order_id = response.data['data'][0]['id']
        request_data = {
            "acceptor": 2,
            'status': 1
        }
        response = self.client.patch(get_url('{order_id}/'.format(order_id=order_id)), json.dumps(request_data),
                                     content_type='application/json',
                                     headers=self.headers)
        self.assertEqual(response.status_code, 200)
        response = self.client.delete(get_url('{order_id}/'.format(order_id=order_id)), headers=self.headers)
        self.assertEqual(response.status_code, 403)
        response = self.client.get(get_url(""), {'order_id': order_id}, headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['data']), 1)
