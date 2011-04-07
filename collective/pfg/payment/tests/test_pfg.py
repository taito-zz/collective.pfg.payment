try:
    import unittest2 as unittest
except ImportError:
    import unittest
import doctest

from Testing import ZopeTestCase as ztc

from Products.CMFCore.utils import getToolByName

from collective.pfg.payment.tests import base
from collective.pfg.payment.interfaces import IProperties


class TestSetup(base.FunctionalTestCase):

    def afterSetUp(self):
        """After SetUp"""
        self.setRoles(('Manager',))
        ## Set up sessioning objects
        ztc.utils.setupCoreSessions(self.app)
        properties = getToolByName(self.portal, 'portal_properties')
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
        wftool = getToolByName(self.portal, 'portal_workflow')
        ## Create Starting Form Folder
        self.portal.invokeFactory(
            'FormFolder',
            'start_form',
            title="Start Form Folder",
        )
        start_form = self.portal.start_form
        wftool.doActionFor(start_form, "publish")
        ## Create Form Folder
        self.portal.invokeFactory(
            'FormFolder',
            'form',
            title="Form Folder",
        )
        form = self.portal.form
        wftool.doActionFor(form, "publish")
        ## Add FormFixedPointField
        form.invokeFactory(
            'FormStringField',
            'MERCHANT_ID',
            fgDefault = '13466',
        )
        form.invokeFactory(
            'FormStringField',
            'AMOUNT',
            fgDefault = '1',
        )
        form.invokeFactory(
            'FormStringField',
            'ORDER_NUMBER',
            fgDefault = '1',
        )
        form.invokeFactory(
            'FormStringField',
            'REFERENCE_NUMBER',
            fgDefault = '',
        )
        form.invokeFactory(
            'FormStringField',
            'ORDER_DESCRIPTION ',
            fgDefault = 'taito.horiuchi@gmail.com,t,t,1',
        )
        form.invokeFactory(
            'FormStringField',
            'CURRENCY ',
            fgDefault = 'EUR',
        )
        form.invokeFactory(
            'FormStringField',
            'RETURN_ADDRESS',
            fgDefault = 'http://localhost:8080/Plone/form-folder/@@verkkomaksut-success',
        )
        form.invokeFactory(
            'FormStringField',
            'CANCEL_ADDRESS ',
            fgDefault = 'http://localhost:8080/Plone/form-folder/verkkomakust/@@verkkomaksut-canceled',
        )
        form.invokeFactory(
            'FormStringField',
            'PENDING_ADDRESS ',
            fgDefault = '',
        )
        form.invokeFactory(
            'FormStringField',
            'NOTIFY_ADDRESS',
            fgDefault = 'http://localhost:8080/Plone/form-folder/verkkomakust/@@verkkomaksut-notify',
        )
        form.invokeFactory(
            'FormStringField',
            'TYPE',
            fgDefault = 'S1',
        )
        form.invokeFactory(
            'FormStringField',
            'CULTURE',
            fgDefault = 'fi_FI',
        )
        form.invokeFactory(
            'FormStringField',
            'PRESELECTED_METHOD ',
            fgDefault = '',
        )
        form.invokeFactory(
            'FormStringField',
            'MODE',
            fgDefault = '1',
        )
        form.invokeFactory(
            'FormStringField',
            'VISIBLE_METHODS ',
            fgDefault = '',
        )
        form.invokeFactory(
            'FormStringField',
            'GROUP',
            fgDefault = '',
        )
        form.invokeFactory(
            'FormStringField',
            'AUTHCODE',
            fgTDefault = 'python:here.restrictedTraverse("auth-code")',
        )


def test_suite():
    return unittest.TestSuite([

        ztc.FunctionalDocFileSuite(
            'tests/functional/pfg.txt',
            package='collective.pfg.payment',
            test_class=TestSetup,
            optionflags=doctest.REPORT_ONLY_FIRST_FAILURE | doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS),

            ])

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
