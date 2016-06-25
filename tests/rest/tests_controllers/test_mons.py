"""Mons controller tests
   kujira-api must already be running
"""

import common_testing_methods


class MonsTestCase(common_testing_methods.CommonTestinglMethods):
    """Mons controllers test case,
     inherits testing methods from CommonTestingMethods"""

    type = "mons"

    def test_server_name(self):
        """Testing does response server name equals to response id"""
        for j in range(len(self.data['data'])):
            data_id = self.data['data'][j]['id']
            self.assertEqual(self.data['data'][j]['attributes']['name'], data_id)
            self.assertEqual(self.data['data'][j]['attributes']['server'], data_id)


if __name__ == '__main__':
    common_testing_methods.main()
