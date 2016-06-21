"""Common testing methods"""

import unittest
import requests


class CommonTestinglMethods(unittest.TestCase):
    """Base class for mons, osds and pools controllers test cases"""

    clusters_data = None
    clusters_id = None
    response = None
    data = None
    type = None
    expected_attributes = None


    def setUp(self):
        self.clusters_data = requests.get("http://0.0.0.0:5000/kujira/api/v1/"+"clusters").json()
        self.clusters_id = self.get_clusters_id()
        self.response = requests.get("http://0.0.0.0:5000/kujira/api/v1/" + self.type + "/" + self.clusters_id)
        self.data = self.response.json()

    def tearDown(self):
        self.clusters_data = None
        self.clusters_id = None
        self.response = None
        self.data = None

    def get_clusters_id(self):
        """Using to get cluster id parameter
        which will be used later to request for mons, pools and osds
        :return: field id from clusters response
        """
        self.clusters_id = self.clusters_data['data']['id']
        return self.clusters_id

    def test_expected_response(self):
        """Test for expected response:
            status code= 200,
            response is dictionary."""
        self.assertEqual(self.response.status_code, 200)
        self.assertTrue(isinstance(self.data, dict))

    def test_consist_data_key(self):
        """Testing does response consist data key:
            {
                # DATA KEY - "data"
                "data": [
                    {
                        ...
                    },
                    ...
                ]
            }
        """
        self.assertIn('data', self.data)

    def test_expected_data_structure(self):
        """Testing does reponse structure is the same as expected:
           {
                "data": [
                    {
                        # IS DICTIONARY
                        "attributes":{
                            # IS DICTIONARY
                            ...
                        },
                        ...
                    },
                    ...
                ]
            }
        """
        self.assertTrue(isinstance(self.data['data'], list))
        for j in range(len(self.data['data'])):
            self.assertTrue(isinstance(self.data['data'][j], dict))
            self.assertTrue(isinstance(self.data['data'][j]['attributes'], dict))

    def test_keys_in__data_list(self):
        """Testing keys in data list of dictionaries:
            {
                "data": [
                    {
                        # RESPONSE CONSIST KEY "attributes"
                        "attributes":{
                         ...
                        },
                        # RESPONSE CONSIST KEY "type"
                        "type": "some value",
                        # RESPONSE CONSIST KEY "id"
                        "id": "some value"
                    },
                    ...
                ]
            }
        """
        for j in range(len(self.data['data'])):
            self.assertIn('attributes', self.data['data'][j])
            self.assertIn('type', self.data['data'][j])
            self.assertIn('id', self.data['data'][j])

    def test_type(self):
        """Testing response type"""
        for j in range(len(self.data['data'])):
            self.assertEqual(self.data['data'][j]['type'], self.type)

    def test_expected_attributes_keys(self):
        """ Testing keys in "attributes" dictionary"""
        if self.type == "mons":
            self.expected_attributes = []
            self.expected_attributes.append('name')
            self.expected_attributes.append('in-quorum')
            self.expected_attributes.append('addr')
            self.expected_attributes.append('rank')
            self.expected_attributes.append('server')
        elif self.type == "pools":
            self.expected_attributes = []
            self.expected_attributes.append('full')
            self.expected_attributes.append('name')
            self.expected_attributes.append('id')
            self.expected_attributes.append('crush-ruleset')
            self.expected_attributes.append('crash-replay-interval')
            self.expected_attributes.append('hashpspool')
            self.expected_attributes.append('pg-num')
            self.expected_attributes.append('quota-max-bytes')
            self.expected_attributes.append('size')
            self.expected_attributes.append('pgp-num')
            self.expected_attributes.append('min-size')
            self.expected_attributes.append('quota-max-objects')
        elif self.type == "osds":
            self.expected_attributes = []
            self.expected_attributes.append('crush-node-ancestry')
            self.expected_attributes.append('uuid')
            self.expected_attributes.append('public-addr')
            self.expected_attributes.append('reweight')
            self.expected_attributes.append('valid-commands')
            self.expected_attributes.append('up')
            self.expected_attributes.append('server')
            self.expected_attributes.append('cluster-addr')
            self.expected_attributes.append('in')
            self.expected_attributes.append('pools')
            self.expected_attributes.append('id')
        for j in range(len(self.data['data'])):
            for k in range(len(self.expected_attributes)):
                self.assertIn(self.expected_attributes[k], self.data['data'][j]['attributes'])

if __name__ == '__main__':
    unittest.main()
