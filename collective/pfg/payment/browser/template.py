from Acquisition import aq_inner, aq_parent
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
#from Products.CMFPlone.utils import safe_hasattr
#from Products.CMFCore.Expression import getExprContext
from Products.CMFCore.utils import getToolByName
#from Products.Archetypes.interfaces.field import IField
#from Products.PloneFormGen import implementedOrProvidedBy
#from collective.pfg.payment import CartMessageFactory as _
from collective.pfg.payment.interfaces import IProperties


class PaymentConfigView(BrowserView):

    template = ViewPageTemplateFile('templates/payment_config.pt')

    def __call__(self):
        self.request.set('disable_border', True)
        return self.template()

class PaymentSucceededView(BrowserView):

    template = ViewPageTemplateFile('templates/payment_succeeded.pt')

    def __call__(self):
        self.request.set('disable_border', True)
        context = aq_inner(self.context)
        sdm = getToolByName(context, 'session_data_manager')
        session = sdm.getSessionData(create="False")
#        properties = getToolByName(context, 'portal_properties')
#        cppp = getattr(properties, 'collective_pfg_payment_properties')
#        tuples = [(field, session.get(field)) for field in IProperties(cppp).session_fields]
#        items = dict(tuples)
        items = session.get('collective.pfg.payment', {})
        self.request.form = items
        parent = aq_parent(context)
        parent.fgProcessActionAdapters(None, fields=None, REQUEST=self.request)
        self.items = context.displayInputs(self.request)
        return self.template()
