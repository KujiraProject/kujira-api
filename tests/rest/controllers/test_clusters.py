"""Clusters controller test
   kujira-api must already be running
"""

import unittest
import requests



class ClustersTestCase(unittest.TestCase):

    response = None
    data = None

    def setUp(self):
        self.response = requests.get("http://0.0.0.0:5000/kujira/api/v1/clusters")
        self.data = self.response.json()

    def tearDown(self):
        self.response = None
        self.data = None


    def test_expectedResponse(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertTrue(isinstance(self.data, dict))

    def test_consistDataKey(self):
        self.assertIn('data', self.data)

    def test_expectedDataStructure(self):
        self.assertTrue(isinstance(self.data['data'], dict))
        self.assertTrue(isinstance(self.data['data']['attributes'], dict))

    def test_KeysInDataDictionary(self):
        self.assertIn('attributes', self.data['data'])
        self.assertIn('type', self.data['data'])
        self.assertIn('id', self.data['data'])

    def test_type(self):
        self.assertEqual(self.data['data']['type'], 'clusters')

    def test_expectedAttributesKeys(self):
        self.assertIn('epoch', self.data['data']['attributes'])
        self.assertIn('health', self.data['data']['attributes'])
        self.assertIn('id', self.data['data']['attributes'])
        self.assertIn('name', self.data['data']['attributes'])

    def test_name(self):
        self.assertEqual(self.data['data']['attributes']['name'], 'ceph')

if __name__ == '__main__':
    unittest.main()



