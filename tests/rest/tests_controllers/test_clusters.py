"""Clusters controller test
   - kujira-api must already be running
"""

import unittest
import requests


class ClustersTestCase(unittest.TestCase):
    """Clusters controllers test case"""

    response = None
    data = None

    def setUp(self):
        self.response = requests.get("http://0.0.0.0:5000/kujira/api/v1/clusters")
        self.data = self.response.json()

    def tearDown(self):
        self.response = None
        self.data = None

    def test_expected_response(self):
        """Test for expected response:
              status code= 200,
              response is dictionary
        """
        self.assertEqual(self.response.status_code, 200)
        self.assertTrue(isinstance(self.data, dict))

    def test_consist_data_key(self):
        """Testing does response consist data key:
            {
                # DATA KEY - "data"
                "data":{
                    ...
                }
            }
        """
        self.assertIn('data', self.data)

    def test_expected_data_structure(self):
        """Testing does reponse structure is the same as expected:
           {
                "data":{
                    # IS DICTIONARY
                    "attributes":{
                        # IS DICTIONARY
                        ...
                    },
                    ...
                }
            }
        """
        self.assertTrue(isinstance(self.data['data'], dict))
        self.assertTrue(isinstance(self.data['data']['attributes'], dict))

    def test_keys_in_data_dictionary(self):
        """Testing keys in data dictionary:
            {
                "data":{
                    # RESPONSE CONSIST KEY "attributes"
                    "attributes":{
                        ...
                    },
                    # RESPONSE CONSIST KEY "type"
                    "type": "some value",
                    # RESPONSE CONSIST KEY "id"
                    "id": "some value"
                }
            }
        """
        self.assertIn('attributes', self.data['data'])
        self.assertIn('type', self.data['data'])
        self.assertIn('id', self.data['data'])

    def test_type(self):
        """ "type": "clusters" test:
            {
                "data":{
                    ...
                    # RESPONSE CONSIST KEY "type" WITH "clusters VALUE"
                    type": "clusters",
                    ...
                }
            }
        """
        self.assertEqual(self.data['data']['type'], 'clusters')

    def test_expected_attributes_keys(self):
        """ Testing keys in "attributes" dictionary:
            {
                "data":{
                    "attributes":{
                    # "attributes" KEY VALUE IS DICTIONARY WITH
                    # "epoch", "health", "id", "name" KEYS
                        "epoch": "some value",
                        "health": "some value",
                        "id": "some value",
                        "name": "some value"
                    },
                    ...
                }
            }
         """
        self.assertIn('epoch', self.data['data']['attributes'])
        self.assertIn('health', self.data['data']['attributes'])
        self.assertIn('id', self.data['data']['attributes'])
        self.assertIn('name', self.data['data']['attributes'])

    def test_name(self):
        """ "name": "ceph" test:
            {
                "data":{
                    "attributes":{
                        ...
                        # "ceph" IS EXPECTED VALUE OF "name" KEY
                        "name": "ceph"
                    },
                    ...
                }
            }
        """
        self.assertEqual(self.data['data']['attributes']['name'], 'ceph')


if __name__ == '__main__':
    unittest.main()



