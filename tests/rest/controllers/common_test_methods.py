"""Common test methods"""


def get_clusters_id(clusters_data):
    clusters_id = clusters_data['data']['id']
    return clusters_id




def test_expectedResponse(self, response, data):
    self.assertEqual(response.status_code, 200)
    self.assertTrue(isinstance(data, dict))

def test_consistDataKey(self, data):
    self.assertIn('data', data)

def test_expectedDataStructure(self, data):
    self.assertTrue(isinstance(data['data'], list))
    for j in range(len(data['data'])):
        self.assertTrue(isinstance(data['data'][j], dict))
        self.assertTrue(isinstance(data['data'][j]['attributes'], dict))

def test_KeysInDatalistOfDictionaries(self, data):
    for j in range(len(data['data'])):
        self.assertIn('attributes', data['data'][j])
        self.assertIn('type', data['data'][j])
        self.assertIn('id', data['data'][j])

def test_type(self, data, type):
    for j in range(len(data['data'])):
        self.assertEqual(data['data'][j]['type'], type)


def test_expectedAttributesKeys(self, data, list_of_expected_attributes):
    for j in range(len(data['data'])):
        for k in range(len(list_of_expected_attributes)):
            self.assertIn(list_of_expected_attributes[k], data['data'][j]['attributes'])