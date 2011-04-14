from Acquisition import aq_inner, aq_parent

from zope.annotation import IAnnotations
from zope.component import getMultiAdapter, getUtility

from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from Products.CMFCore.utils import getToolByName
from Products.CMFCore.Expression import getExprContext
from Products.CMFPlone.utils import safe_hasattr
from Products.statusmessages.interfaces import IStatusMessage

from collective.pfg.payment import PaymentMessageFactory as _
from collective.pfg.payment.interfaces import IRegularExpression


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
        items = session.get('collective.pfg.payment', {})
        self.request.form = items
        parent = aq_parent(context)
        try:
            # PloneFormGen-1.6.0
            parent.fgProcessActionAdapters(None, fields=None, REQUEST=self.request)
        except AttributeError:
            # PloneFormGen-1.2.7
            adapters = parent.getRawActionAdapter()
            for adapter in adapters:
                actionAdapter = getattr(parent.aq_explicit, adapter, None)
                if actionAdapter is None:
                    pass
                else:
                    # Now, see if we should execute it.
                    # Check to see if execCondition exists and has contents
                    if safe_hasattr(actionAdapter, 'execCondition') and \
                      len(actionAdapter.getRawExecCondition()):
                        # evaluate the execCondition.
                        # create a context for expression evaluation
                        context = getExprContext(parent, actionAdapter)
                        doit = actionAdapter.getExecCondition(expression_context=context)
                    else:
                        # no reason not to go ahead
                        doit = True

                    if doit:
                        import pdb; pdb.set_trace()
                        names = items.keys()
                        fields = [parent[name] for name in names]
                        result = actionAdapter.onSuccess(fields, REQUEST=self.request)
                        if type(result) is type({}) and len(result):
                            # return the dict, which hopefully uses
                            # field ids or FORM_ERROR_MARKER for keys
                            return result






        self.items = context.displayInputs(self.request)
        if session.get('collective.pfg.payment.number'):
            del session['collective.pfg.payment.number']
        return self.template()

class EditOrderNumberView(BrowserView):

    template = ViewPageTemplateFile('templates/edit_order_number.pt')

    def __call__(self):
        form = self.request.form
        context = aq_inner(self.context)
        annotations = IAnnotations(context)['collective.pfg.payment']
        if form.get("form.button.UpdateNumber", None) is not None:
            sdm = getToolByName(context, 'session_data_manager')
            session = sdm.getSessionData(create=False)
            if session is not None:
                if session.get('collective.pfg.payment.number', None) is not None:
                    del session['collective.pfg.payment.number']
            re = getUtility(IRegularExpression)
            numbering_type = form.get('numbering_type')
            if numbering_type == 'Incremental':
                annotations.numbering_type = 'Incremental'
                next_incremental_number = form.get('next_incremental_number', None)
                if re.integer(next_incremental_number):
                    annotations.next_incremental_number = int(next_incremental_number)
                else:
                    message = _(u"Please input integer number for the incremental number.")
                    IStatusMessage(self.request).addStatusMessage(message, type='warn')
            elif numbering_type == 'Random':
                annotations.numbering_type = 'Random'
                random_number_digits = form.get('random_number_digits', None)
                if re.integer(random_number_digits):
                    annotations.random_number_digits = int(random_number_digits)
                else:
                    message = _(u"Please input integer number for the randome digits.")
                    IStatusMessage(self.request).addStatusMessage(message, type='warn')
        return self.template()

    def current_url(self):
        """Returns current url"""
        context_state = getMultiAdapter((self.context, self.request),
                                            name=u'plone_context_state')
        return context_state.current_page_url()

    def select_numbering_type(self):
        types = ['Incremental', 'Random']
        context = aq_inner(self.context)
        annotations = IAnnotations(context)['collective.pfg.payment']
        numbering_type = annotations.numbering_type
        html = '<select name="numbering_type" id="numbering_type">'
        for typ in types:
            if typ == numbering_type:
                html += '<option value="%s" selected="selected">%s</option>' % (typ, typ)
            else:
                html += '<option value="%s">%s</option>' % (typ, typ)
        html += '</select>'
        return html

    def next_incremental_number(self):
        context = aq_inner(self.context)
        return IAnnotations(context)['collective.pfg.payment'].next_incremental_number

    def random_number_digits(self):
        context = aq_inner(self.context)
        return IAnnotations(context)['collective.pfg.payment'].random_number_digits
