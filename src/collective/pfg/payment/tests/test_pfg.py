from Products.CMFCore.utils import getToolByName
from Testing import ZopeTestCase as ztc
from collective.pfg.payment.interfaces import IProperties
from collective.pfg.payment.tests.base import FUNCTIONAL_TESTING
from hexagonit.testing.browser import Browser
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import TEST_USER_PASSWORD
from plone.app.testing import setRoles
from plone.testing import layered
from zope.testing import renormalizing

import doctest
import manuel.codeblock
import manuel.doctest
import manuel.testing
import re
import transaction
import unittest

FLAGS = doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS | doctest.REPORT_NDIFF | doctest.REPORT_ONLY_FIRST_FAILURE

CHECKER = renormalizing.RENormalizing([
    # Normalize the generated UUID values to always compare equal.
    (re.compile(r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}'), '<UUID>'),
])


def setUp(self):
    layer = self.globs['layer']
    app = layer['app']
    browser = Browser(app)
    portal = layer['portal']

    self.globs.update({
        'TEST_USER_NAME': TEST_USER_NAME,
        'TEST_USER_PASSWORD': TEST_USER_PASSWORD,
        'browser': browser,
        'portal': portal,
    })

    browser.setBaseUrl(portal.absolute_url())
    browser.handleErrors = True
    portal.error_log._ignored_exceptions = ()
    setRoles(portal, TEST_USER_ID, ['Manager'])

    ztc.utils.setupCoreSessions(app)
    properties = getToolByName(portal, 'portal_properties')
    pp = getattr(properties, 'collective_pfg_payment_properties')
    IProperties(pp).mac = '6pKF4jkv97zmqBJ3ZL8gUw5DfT2NMQ'
    IProperties(pp).fields = [
        'MERCHANT_ID',
        'AMOUNT',
        'ORDER_NUMBER',
        'REFERENCE_NUMBER',
        'ORDER_DESCRIPTION',
        'CURRENCY',
        'RETURN_ADDRESS',
        'CANCEL_ADDRESS',
        'PENDING_ADDRESS',
        'NOTIFY_ADDRESS',
        'TYPE',
        'CULTURE',
        'PRESELECTED_METHOD',
        'MODE',
        'VISIBLE_METHODS',
        'GROUP',
    ]
    IProperties(pp).separator = '|'
    IProperties(pp).capital = True
    ## Tools
    wftool = getToolByName(portal, 'portal_workflow')
    ## Create Starting Form Folder
    portal.invokeFactory(
        'FormFolder',
        'start_form',
        title="Start Form Folder",
    )
    start_form = portal.start_form
    wftool.doActionFor(start_form, "publish")
    ## Create Form Folder
    portal.invokeFactory(
        'FormFolder',
        'form',
        title="Form Folder",
    )
    form = portal.form
    wftool.doActionFor(form, "publish")
    ## Add FormFixedPointField
    form.invokeFactory(
        'FormStringField',
        'MERCHANT_ID',
        fgDefault='13466',
    )
    form.invokeFactory(
        'FormStringField',
        'AMOUNT',
        fgDefault='1',
    )
    form.invokeFactory(
        'FormStringField',
        'ORDER_NUMBER',
        fgDefault='1',
    )
    form.invokeFactory(
        'FormStringField',
        'REFERENCE_NUMBER',
        fgDefault='',
    )
    form.invokeFactory(
        'FormStringField',
        'ORDER_DESCRIPTION ',
        fgDefault='taito.horiuchi@gmail.com,t,t,1',
    )
    form.invokeFactory(
        'FormStringField',
        'CURRENCY ',
        fgDefault='EUR',
    )
    form.invokeFactory(
        'FormStringField',
        'RETURN_ADDRESS',
        fgDefault='http://localhost:8080/Plone/form-folder/@@verkkomaksut-success',
    )
    form.invokeFactory(
        'FormStringField',
        'CANCEL_ADDRESS ',
        fgDefault='http://localhost:8080/Plone/form-folder/verkkomakust/@@verkkomaksut-canceled',
    )
    form.invokeFactory(
        'FormStringField',
        'PENDING_ADDRESS ',
        fgDefault='',
    )
    form.invokeFactory(
        'FormStringField',
        'NOTIFY_ADDRESS',
        fgDefault='http://localhost:8080/Plone/form-folder/verkkomakust/@@verkkomaksut-notify',
    )
    form.invokeFactory(
        'FormStringField',
        'TYPE',
        fgDefault='S1',
    )
    form.invokeFactory(
        'FormStringField',
        'CULTURE',
        fgDefault='fi_FI',
    )
    form.invokeFactory(
        'FormStringField',
        'PRESELECTED_METHOD ',
        fgDefault='',
    )
    form.invokeFactory(
        'FormStringField',
        'MODE',
        fgDefault='1',
    )
    form.invokeFactory(
        'FormStringField',
        'VISIBLE_METHODS ',
        fgDefault='',
    )
    form.invokeFactory(
        'FormStringField',
        'GROUP',
        fgDefault='',
    )
    form.invokeFactory(
        'FormStringField',
        'AUTHCODE',
        fgTDefault='python:here.restrictedTraverse("auth-code")',
    )

    transaction.commit()


def DocFileSuite(testfile, flags=FLAGS, setUp=setUp, layer=FUNCTIONAL_TESTING):
    """Returns a test suite configured with a test layer.

    :param testfile: Path to a doctest file.
    :type testfile: str

    :param flags: Doctest test flags.
    :type flags: int

    :param setUp: Test set up function.
    :type setUp: callable

    :param layer: Test layer
    :type layer: object

    :rtype: `manuel.testing.TestSuite`
    """
    m = manuel.doctest.Manuel(optionflags=flags, checker=CHECKER)
    m += manuel.codeblock.Manuel()

    return layered(
        manuel.testing.TestSuite(m, testfile, setUp=setUp, globs=dict(layer=layer)),
        layer=layer)


def test_suite():
    return unittest.TestSuite([DocFileSuite('functional/pfg.txt')])
