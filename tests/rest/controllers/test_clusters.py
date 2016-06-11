import eventlet
import json
import unittest
import requests
from flask import Flask
from kujira.blueprints import CLUSTER_BP, SERVER_BP, OSD_BP, POOL_BP, MON_BP
from kujira.rest.controllers import clusters, osds, pools, servers, mons


from flask_socketio import SocketIO


eventlet.monkey_patch()
SOCKETIO = SocketIO()



"""
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

"""

constr = CalamariClient(api_url="http://0.0.0.0:8080/api/v2/", username=CALAMARI_API_USER,
                        password=CALAMARI_API_PWD, timeout=CALAMARI_API_TIMEOUT)
client = constr.authenticate()
response = client.get(constr._api_url, timeout=constr._timeout)
print response.status_code


