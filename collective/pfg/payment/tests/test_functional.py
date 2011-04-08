try:
    import unittest2 as unittest
except ImportError:
    import unittest
import doctest
from Testing import ZopeTestCase as ztc
from collective.pfg.payment.tests import base


class TestSetup(base.FunctionalTestCase):

    def afterSetUp(self):
        """After SetUp"""
        self.setRoles(('Manager',))
        ## Set up sessioning objects
        ztc.utils.setupCoreSessions(self.app)
        self.portal.invokeFactory(
            'FormFolder',
            'form',
            title="Form Folder",
        )
        form = self.portal.form



def test_suite():
    return unittest.TestSuite([

        ztc.FunctionalDocFileSuite(
            'tests/functional/setup.txt',
            package='collective.pfg.payment',
            test_class=TestSetup,
            optionflags=doctest.REPORT_ONLY_FIRST_FAILURE | doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS),

            ])

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
