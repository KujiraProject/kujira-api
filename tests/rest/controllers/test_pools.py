"""Pools controller test
   kujira-api must already be running
"""

import unittest
import requests
import common_test_methods



class PoolsTestCase(unittest.TestCase):

    clusters_id = None
    response = None
    data = None


    def setUp(self):
        clusters_data = requests.get("http://0.0.0.0:5000/kujira/api/v1/clusters").json()
        self.clusters_id = common_test_methods.get_clusters_id(clusters_data)
        self.response = requests.get("http://0.0.0.0:5000/kujira/api/v1/pools/" + str(self.clusters_id))
        self.data = self.response.json()

    def tearDown(self):
        self.clusters_id = None
        self.response = None
        self.data = None



    def test_expectedResponse(self):
        common_test_methods.test_expectedResponse(self, self.response, self.data)

    def test_consistDataKey(self):
        common_test_methods.test_consistDataKey(self, self.data)

    def test_expectedDataStructure(self):
        common_test_methods.test_expectedDataStructure(self, self.data)

    def test_KeysInDatalistOfDictionaries(self):
        common_test_methods.test_KeysInDatalistOfDictionaries(self, self.data)

    def test_type(self):
        common_test_methods.test_type(self, self.data, 'pools')

    def test_expectedAttributesKeys(self):
        list_of_expected_attributes = []
        list_of_expected_attributes.append('full')
        list_of_expected_attributes.append('name')
        list_of_expected_attributes.append('id')
        list_of_expected_attributes.append('crush-ruleset')
        list_of_expected_attributes.append('crash-replay-interval')
        list_of_expected_attributes.append('hashpspool')
        list_of_expected_attributes.append('pg-num')
        list_of_expected_attributes.append('quota-max-bytes')
        list_of_expected_attributes.append('size')
        list_of_expected_attributes.append('pgp-num')
        list_of_expected_attributes.append('min-size')
        list_of_expected_attributes.append('quota-max-objects')
        common_test_methods.test_expectedAttributesKeys(self, self.data, list_of_expected_attributes)

    def test_id_equals(self):
        for j in range(len(self.data['data'])):
            id = self.data['data'][j]['id']
            self.assertEqual(str(self.data['data'][j]['attributes']['id']), id)


if __name__ == '__main__':
    unittest.main()