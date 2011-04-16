from zope.annotation import IAnnotations
from zope.component import getMultiAdapter
from Acquisition import aq_inner
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.viewlets.common import ViewletBase
from Products.CMFCore.utils import getToolByName
from Products.CMFCore.interfaces import ISiteRoot
from Products.PloneFormGen.interfaces.form import IPloneFormGenForm
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
            capital = form.get('capital', False)
            self.payment_properties.capital = capital
            if capital is True or capital == 'on':
                self.payment_properties.capital = True
            fields = form.get('fields', None)
            if fields is not None:
                values = [field for field in fields.split('\r\n') if field != '']
                self.payment_properties.fields = values

    @property
    def payment_properties(self):
        context = aq_inner(self.context)
        if ISiteRoot.providedBy(context):
            properties = getToolByName(context, 'portal_properties')
            prop = getattr(properties, 'collective_pfg_payment_properties')
#            return IProperties(prop)
        if IPloneFormGenForm.providedBy(context):
            prop = IAnnotations(context)['collective.pfg.payment']
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

class LocalPaymentViewlet(PaymentViewletBase):

    index = render = ViewPageTemplateFile("viewlets/local_payment.pt")

    def update(self):
        form = self.request.form
        if form.get("form.button.UseLocalPayment" ,None) is not None:
            res = form.get("local_payment")
            numbers = IAnnotations(self.context)['collective.pfg.payment']
            if res is True or res == 'on':
                numbers.local_payment = True
            else:
                numbers.local_payment = False
            self.request.response.redirect(self.current_url)

    def local_payment(self):
        numbers = IAnnotations(self.context)['collective.pfg.payment']
        if numbers.local_payment is True:
            html = '<input type="checkbox" id="local_payment"\
                name="local_payment" value="on" checked="checked" />'
        else:
            html = '<input type="checkbox" id="local_payment"\
                name="local_payment" value="on" />'
        return html

#class LocalPaymentConfigPropertiesViewlet(PaymentConfigPropertiesViewlet):
#    """Properties Viewlet for Local Payment Config."""

#    @property
#    def payment_properties(self):
#        context = aq_inner(self.context)
#        return IAnnotations(context)['collective.pfg.payment']
#        properties = getToolByName(context, 'portal_properties')
#        prop = getattr(properties, 'collective_pfg_payment_properties')
#        return IProperties(prop)
