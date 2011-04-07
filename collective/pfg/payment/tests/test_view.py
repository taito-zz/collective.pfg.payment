from mock import Mock, patch
try:
    import unittest2 as unittest
except ImportError:
    import unittest

from zope.component import provideAdapter
from zope.interface import implements, alsoProvides
from zope.publisher.browser import TestRequest

from Products.CMFCore.interfaces import ISiteRoot

from collective.pfg.payment.browser.template import (
    PaymentConfigView,
    PaymentSucceededView,
)


class Template(object):

    def __init__(self, template):
        self.template = template

    def __call__(self):
        return self.template

def template(temp):
    return temp

class ViewTest(unittest.TestCase):

#    @patch('collective.pfg.payment.browser.template.ViewPageTemplateFile', template)
#    def test_payment(self):
#        context = Mock()
#        request = TestRequest()
#        view = PaymentConfigView(context, request)
#        self.assertEqual('templates/payment_config.pt', view.template())

#    @patch('collective.pfg.payment.browser.template.ViewPageTemplateFile')
    def test_payment_config__view_template(self):
        context = Mock()
#        request = TestRequest()
        request = Mock()
        request.set.return_value = Mock()
        view = PaymentConfigView(context, request)
        view.template = Mock()
        self.failIf(view.template.called)
        view()
        self.failUnless(view.template.called)
#        self.assertEqual('templates/payment_config.pt', view.template())
#        self.assertEqual('templates/payment_config.pt', view.__call__())
#        self.assertEqual('template', view.template())
#        self.assertEqual('template', view.__call__())


#    def test_payment_config__view_template(self):
#        context = Mock()
#        request = TestRequest()
#        view = PaymentConfigView(context, request)
#        view.template = Mock(return_value='template')
#        self.assertEqual('template', view.template())

#    ## PaymentSuccessView
#    def test_payment_success_view(self):
#        context = Mock()
#        request = TestRequest()
#        view = PaymentSucceededView(context, request)
#        self.assertEqual('BoundPageTemplate', view.template.__class__.__name__)

#Viewlets
#--------
#    >>> from collective.pfg.payment.browser.viewlet import PaymentViewletBase
#    >>> viewlet = PaymentViewletBase(context, request, view)

#    >>> class getMultiAdapter(object):
#    ...     def __init__(self, **kwargs):
#    ...         for k, v in kwargs.items(): setattr(self, k, v)
#    ...     def current_page_url(self):
#    ...         return 'current_page_url'

#    >>> getMultiAdapter((context, request), name=u'plone_context_state') = Mock()
#    >>> @patch('zope.component.getMultiAdapter', getMultiAdapter())

#    >>> viewlet.current_url = Mock(return_value='current_url')
#    >>> viewlet.current_url
#    'current_url'


def test_suite():
    return unittest.TestSuite([
        unittest.makeSuite(ViewTest),
    ])
