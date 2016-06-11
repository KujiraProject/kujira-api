import unittest
import json

from kujira.blueprints import CLUSTER_BP
from kujira.rest.controllers import clusters
from kujira import create_app, SOCKETIO



class ClustersTestCase(unittest.TestCase):


   def setUp(self):


   response = clusters.cluster()
   data = json.loads(response.get_data())


   def test_expectedResponse(self):
       self.assertEqual(self.response.status_code, 200)
       self.assertTrue(isinstance(self.data, dict))


   def test_consistDataKey(self):
       self.assertIn('data', self.data)


   def test_expectedDataStructure(self):
       self.assertTrue(isinstance(self.data['data'], list))
       for i in range(len(self.data['data'])):
           self.assertTrue(isinstance(self.data['data'][i], dict))


   def test_KeysInDatalistOfDictionaries(self):
       for i in range(len(self.data['data'])):
           self.assertIn('attributes', self.data['data'][i])
           self.assertIn('type', self.data['data'][i])
           self.assertIn('id', self.data['data'][i])


   def test_type(self):
       for i in range(len(self.data['data'])):
           self.assertEqual(self.data['data'][i]['type'], 'clusters')


   def test_expectedAttributesKeys(self):
       for i in range(len(self.data['data'])):
           self.assertIn('update-time', self.data['data'][i]['attributes'])
           self.assertIn('id', self.data['data'][i]['attributes'])
           self.assertIn('name', self.data['data'][i]['attributes'])


   def test_name(self):
       for i in range(len(self.data['data'])):
           self.assertEqual(self.data['data'][i]['attributes']['name'], 'ceph')


if __name__ == '__main__':
    unittest.main()



