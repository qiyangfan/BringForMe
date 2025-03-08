from rest_framework.test import (APITestCase)

from BringForMe import settings
from user.tests import setup_register, setup_login

base_url = '/api/{version}/'.format(version=settings.REST_FRAMEWORK['DEFAULT_VERSION'])
app_base_url = 'media-manager/'


def get_url(url):
    return base_url + app_base_url + url


class ImageTestCase(APITestCase):

    def setUp(self):
        setup_register(self)
        self.headers = setup_login(self)

    def test_image(self):
        with open('test/media/image1.png', 'rb') as f:
            response = self.client.post(get_url('image/'), {'images': f}, headers=self.headers)
            self.assertEqual(response.status_code, 200)
        with open('test/media/image2.png', 'rb') as f:
            response = self.client.post(get_url('image/'), {'images': f}, headers=self.headers)
            self.assertEqual(response.status_code, 200)
        response = self.client.get(get_url('image/'), headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['data']), 2)
        image_id_list = [image['id'] for image in response.data['data']]
        response = self.client.get(get_url('image/'), {'image_ids': image_id_list}, headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['data']), 2)
        response = self.client.delete(get_url('image/'), {'image_ids': image_id_list}, headers=self.headers)
        self.assertEqual(response.status_code, 200)
        response = self.client.get(get_url('image/'), headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['data']), 0)
