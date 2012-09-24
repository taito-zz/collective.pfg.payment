from Acquisition import aq_inner, aq_parent
from zope.annotation import IAnnotations
from zope.component import getUtility
from zope.interface import alsoProvides, noLongerProvides
from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView
from Products.PloneFormGen.interfaces import IPloneFormGenForm
from collective.pfg.payment.content.number import Numbers
from collective.pfg.payment.interfaces import IAuthCode
from collective.pfg.payment.interfaces import (
    IOrderNumberAware,
    IProperties,
    IRandomDigits,
)


class Miscellaneous(BrowserView):

    def auth_code(self):
        context = aq_inner(self.context)
        properties = getToolByName(context, 'portal_properties')
        prop = getattr(properties, 'collective_pfg_payment_properties')
        parent = aq_parent(context)
        numbers = IAnnotations(parent).get('collective.pfg.payment')
        if numbers and numbers.local_payment:
            prop = numbers
        keys = IProperties(prop).fields
        names = [key.replace(' ', '') for key in keys]
        code = IProperties(prop).mac
        separator = IProperties(prop).separator
        capital = IProperties(prop).capital
        ac = getUtility(IAuthCode)
        form = self.request.form.copy()
        form_tuples = form.items()
        form = [(ft[0].replace(' ', ''), ft[1]) for ft in form_tuples]
        form = dict(form)
        keys = [form.get(name, '') for name in names]
        return ac(keys, code=code, separator=separator, capital=capital)

    def make_order_number_aware(self):
        context = aq_inner(self.context)
        alsoProvides(context, IOrderNumberAware)
        IAnnotations(context)['collective.pfg.payment'] = Numbers()
        url = '%s/@@edit-order-number' % context.absolute_url()
        return self.request.response.redirect(url)

    def make_order_number_unaware(self):
        context = aq_inner(self.context)
        noLongerProvides(context, IOrderNumberAware)
        del IAnnotations(context)['collective.pfg.payment']
        return self.request.response.redirect(context.absolute_url())

    def is_order_number_aware(self):
        context = aq_inner(self.context)
        return IOrderNumberAware.providedBy(context) and IPloneFormGenForm.providedBy(context)

    def not_order_number_aware(self):
        context = aq_inner(self.context)
        return not IOrderNumberAware.providedBy(context) and IPloneFormGenForm.providedBy(context)

    def number(self):
        context = aq_inner(self.context)
        parent = aq_parent(context)
        if IAnnotations(parent).get('collective.pfg.payment') is not None:
            annotations = IAnnotations(parent)['collective.pfg.payment']
            sdm = getToolByName(context, 'session_data_manager')
            session = sdm.getSessionData(create=True)
            number = session.get('collective.pfg.payment.number', None)
            if number is None:
                if annotations.numbering_type == 'Incremental':
                    number = annotations.next_incremental_number
                    new_number = number + 1
                    annotations.next_incremental_number = new_number
                    number = str(number)
                if annotations.numbering_type == 'Random':
                    digits = annotations.random_number_digits
                    ids = annotations.numbers
                    rd = getUtility(IRandomDigits)
                    number = rd(digits, ids)
                annotations.numbers.append(number)
                session.set('collective.pfg.payment.number', number)
            return number
