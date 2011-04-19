try:
    import unittest2 as unittest
except ImportError:
    import unittest
import doctest

from Acquisition import aq_base

from Testing import ZopeTestCase as ztc

from zope.component import getSiteManager

from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.tests.utils import MockMailHost
from Products.MailHost.interfaces import IMailHost

from collective.pfg.payment.tests import base
from collective.pfg.payment.interfaces import IProperties


class TestSetup(base.FunctionalTestCase):

    def afterSetUp(self):
        """After SetUp"""
        self.setRoles(('Manager',))
        ## Set up sessioning objects
        ztc.utils.setupCoreSessions(self.app)

        self.portal._original_MailHost = self.portal.MailHost
        self.portal.MailHost = mailhost = MockMailHost('MailHost')
        sm = getSiteManager(context=self.portal)
        sm.unregisterUtility(provided=IMailHost)
        sm.registerUtility(mailhost, provided=IMailHost)

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
#        IProperties(pp).session_fields = ['replyto', 'topic']
        ## Tools
        wftool = getToolByName(self.portal, 'portal_workflow')
        ## Create Starting Form Folder
        self.portal.invokeFactory(
            'FormFolder',
            'start_form',
            title="Start Form Folder",
        )
        start_form = self.portal.start_form
        start_form.setActionAdapter(())
        start_form.setThanksPageOverride('traverse_to:string:form')
        wftool.doActionFor(start_form, "publish")
        ## Add FormFixedPointField
        start_form.invokeFactory(
            'FormFixedPointField',
            'AMOUNT',
            title = 'Price',
            required = True,
        )
        ## Create Form Folder
        self.portal.invokeFactory(
            'FormFolder',
            'form',
            title="Form Folder",
        )
        form = self.portal.form
        form.setActionAdapter(())
        url = '%s/@@test-payment-interface' % self.portal.absolute_url()
        form.setFormActionOverride(url)
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
            fgTDefault = 'python:here.restrictedTraverse("number")()',
        )
        form.invokeFactory(
            'FormStringField',
            'REFERENCE_NUMBER',
            fgDefault = '',
        )
        form.invokeFactory(
            'FormStringField',
            'ORDER_DESCRIPTION',
            fgDefault = 'taito.horiuchi@gmail.com,t,t,1',
        )
        form.invokeFactory(
            'FormStringField',
            'CURRENCY',
            fgDefault = 'EUR',
        )
        form.invokeFactory(
            'FormStringField',
            'RETURN_ADDRESS',
            fgDefault = 'http://localhost:8080/Plone/form-folder/@@verkkomaksut-success',
        )
        form.invokeFactory(
            'FormStringField',
            'CANCEL_ADDRESS',
            fgDefault = 'http://localhost:8080/Plone/form-folder/verkkomakust/@@verkkomaksut-canceled',
        )
        form.invokeFactory(
            'FormStringField',
            'PENDING_ADDRESS',
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
            'PRESELECTED_METHOD',
            fgDefault = '',
        )
        form.invokeFactory(
            'FormStringField',
            'MODE',
            fgDefault = '1',
        )
        form.invokeFactory(
            'FormStringField',
            'VISIBLE_METHODS',
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
        ## Create script adapter to put fields to session.
        form.invokeFactory(
            'FormCustomScriptAdapter',
            'script_adapter',
            ScriptBody = 'items = dict(AMOUNT=request.form["AMOUNT"],)\nrequest.SESSION.set("collective.pfg.payment", items)'
        )
        ## Create Final Form Folder
        self.portal.invokeFactory(
            'FormFolder',
            'final_form',
            title="Final Form Folder",
        )
        final_form = self.portal.final_form
        wftool.doActionFor(final_form, "publish")
        mailer = final_form['mailer']
        mailer.setRecipient_email('info@portal.com')


    def beforeTearDown(self):
        portal = self.portal
        portal.MailHost = portal._original_MailHost
        sm = getSiteManager(context=portal)
        sm.unregisterUtility(provided=IMailHost)
        sm.registerUtility(aq_base(portal._original_MailHost), provided=IMailHost)


def test_suite():
    return unittest.TestSuite([

        ztc.FunctionalDocFileSuite(
            'tests/functional/verkkomaksut_s1.txt',
            package='collective.pfg.payment',
            test_class=TestSetup,
            optionflags=doctest.REPORT_ONLY_FIRST_FAILURE | doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS),

            ])

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
