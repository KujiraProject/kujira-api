"""Osds controller tests
   kujira-api must already be running
"""

import common_testing_methods


class OsdsTestCase(common_testing_methods.CommonTestinglMethods):
    """Osds controllers test case,
     inherits testing methods from CommonTestingMethods"""

    type = "osds"


    def test_osds_specific_structure(self):
        """Testing does the response attributes dictionary
         structure is the same as expected"""
        for i in range(len(self.data['data'])):
            self.assertTrue(isinstance(self.data['data'][i]['attributes']['crush-node-ancestry'], list))
            self.assertTrue(isinstance(self.data['data'][i]['attributes']['valid-commands'], list))
            self.assertTrue(isinstance(self.data['data'][i]['attributes']['pools'], list))



if __name__ == '__main__':
    common_testing_methods.main()
