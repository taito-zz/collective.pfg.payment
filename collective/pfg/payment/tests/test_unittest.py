from doctest import DocFileSuite
from doctest import ELLIPSIS
from doctest import NORMALIZE_WHITESPACE
from doctest import REPORT_ONLY_FIRST_FAILURE
from zope.component import testing

import unittest


OF = REPORT_ONLY_FIRST_FAILURE | NORMALIZE_WHITESPACE | ELLIPSIS


def test_suite():
    return unittest.TestSuite([

        DocFileSuite(
            'tests/unittest/adapter.txt', package='collective.pfg.payment',
            setUp=testing.setUp, tearDown=testing.tearDown,
            optionflags=OF),

        DocFileSuite(
            'tests/unittest/utility.txt', package='collective.pfg.payment',
            setUp=testing.setUp, tearDown=testing.tearDown,
            optionflags=OF), ])
