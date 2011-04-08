from Acquisition import aq_inner
from Products.Five.browser import BrowserView
from Products.CMFPlone.utils import getToolByName


class TestPaymentInterfaceView(BrowserView):

    def test_payment_interface(self):
        context = aq_inner(self.context)
        portal = getToolByName(context, 'portal_url').getPortalObject()
        url = '%s/final_form/thank-you/@@payment-succeeded' % portal.absolute_url()
        self.request.response.redirect(url)
