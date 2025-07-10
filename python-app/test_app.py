import unittest
from unittest.mock import patch
from app import app

class SecretEndpointTest(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    @patch('app.table.get_item')
    def test_secret_found(self, mock_get_item):
        mock_get_item.return_value = {
            'Item': {
                'codeName': 'thedoctor',
                'secret_code': 'TOP_SECRET'
            }
        }

        response = self.client.get('/secret')
        self.assertEqual(response.status_code, 200)
        self.assertIn('secret_code', response.get_json())

    @patch('app.table.get_item')
    def test_secret_not_found(self, mock_get_item):
        mock_get_item.return_value = {}

        response = self.client.get('/secret')
        self.assertEqual(response.status_code, 404)
        self.assertIn('error', response.get_json())

    @patch('app.table.get_item', side_effect=Exception('DynamoDB error'))
    def test_dynamodb_failure(self, mock_get_item):
        response = self.client.get('/secret')
        self.assertEqual(response.status_code, 500)
        self.assertIn('error', response.get_json())

    def test_health_endpoint(self):
        response = self.client.get('/health')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['status'], 'healthy')
        self.assertEqual(data['container'], 'https://hub.docker.com/r/aradgonen98/zenity-devops-challenge')
        self.assertEqual(data['project'], 'https://github.com/aradgonen/devops-challenge-25')

if __name__ == '__main__':
    unittest.main()