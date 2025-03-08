import json

from rest_framework.test import (APITestCase)

from BringForMe import settings
from user.tests import setup_register, setup_login, setup_register_second

base_url = '/api/{version}/'.format(version=settings.REST_FRAMEWORK['DEFAULT_VERSION'])
app_base_url = 'message/'


def get_url(url):
    return base_url + app_base_url + url


class MessageReceiverTestCase(APITestCase):

    def setUp(self):
        setup_register(self)
        self.headers = setup_login(self)
        setup_register_second(self)

    def test_post_message(self):
        request_data = {
            "content": "Hello"
        }
        response = self.client.post(get_url('receiver/{receiver_id}/'.format(receiver_id=2)), json.dumps(request_data),
                                    content_type='application/json',
                                    headers=self.headers)
        self.assertEqual(response.status_code, 200)
        response = self.client.get(get_url('receiver/{receiver_id}/'.format(receiver_id=2)), headers=self.headers)
        self.assertEqual(response.status_code, 200)
        content = response.data['data'][0]['content']
        self.assertEqual(content, 'Hello')
        response = self.client.get(get_url('receiver/'), headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['data']), 1)
        self.assertEqual(response.data['data'][0]['id'], 2)
