from Acquisition import aq_inner
from zope.component import getUtility
from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView
from collective.pfg.payment.interfaces import IAuthCode
from collective.pfg.payment.interfaces import (
    IProperties,
)


class Miscellaneous(BrowserView):

    def auth_code(self):
        context = aq_inner(self.context)
        properties = getToolByName(context, 'portal_properties')
        prop = getattr(properties, 'collective_pfg_payment_properties')
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
