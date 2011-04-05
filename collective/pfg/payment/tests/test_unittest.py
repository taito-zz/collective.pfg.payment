import unittest
import doctest
from doctest import DocFileSuite
from zope.component import testing

def test_suite():
    return unittest.TestSuite([

        DocFileSuite(
            'tests/unittest/utility.txt', package='collective.pfg.payment',
            setUp=testing.setUp, tearDown=testing.tearDown,
            optionflags=doctest.REPORT_ONLY_FIRST_FAILURE | doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS),

            ])

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
