"""Pools controller tests
   kujira-api must already be running
"""

import common_testing_methods


class PoolsTestCase(common_testing_methods.CommonTestinglMethods):
    """Pools controllers test case,
     inherits testing methods from CommonTestingMethods"""

    type = "pools"


    def test_id_equals(self):
        """Testing does data id equals to data atrributes id"""
        for j in range(len(self.data['data'])):
            data_id = self.data['data'][j]['id']
            self.assertEqual(str(self.data['data'][j]['attributes']['id']), data_id)


if __name__ == '__main__':
    common_testing_methods.main()
