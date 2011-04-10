from zope.component import getMultiAdapter#, getUtility
from Acquisition import aq_inner
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.viewlets.common import ViewletBase
from Products.CMFCore.utils import getToolByName
from collective.pfg.payment.interfaces import (
    IProperties,
)


class PaymentViewletBase(ViewletBase):

    @property
    def current_url(self):
        """Returns current url"""
        context_state = getMultiAdapter((self.context, self.request),
                                            name=u'plone_context_state')
        return context_state.current_page_url()


class PaymentConfigPropertiesViewlet(PaymentViewletBase):
    """Properties Viewlet for Payment Config."""

    index = render = ViewPageTemplateFile("viewlets/payment_properties.pt")

    def update(self):
        form = self.request.form
        if form.get('form.button.UpdatePaymentProperties', None) is not None:
            mac = form.get('mac', None)
            if mac is not None:
                self.payment_properties.mac = mac
            separator = form.get('separator', None)
            if separator is not None:
                self.payment_properties.separator = separator
            capital = form.get('capital', None)
            if capital is not None:
                self.payment_properties.capital = capital
            fields = form.get('fields', None)
            if fields is not None:
                values = [field for field in fields.split('\r\n') if field != '']
                self.payment_properties.fields = values

    @property
    def payment_properties(self):
        context = aq_inner(self.context)
        properties = getToolByName(context, 'portal_properties')
        prop = getattr(properties, 'collective_pfg_payment_properties')
        return IProperties(prop)

    def fields_field(self):
        return self.payment_properties.textarea_field(
            'fields', 10, 20)

    def mac_field(self):
        return self.payment_properties.input_field('mac', 30)

    def separator_field(self):
        return self.payment_properties.input_field('separator', 1)

    def capital_field(self):
        return self.payment_properties.boolean_field('capital')
