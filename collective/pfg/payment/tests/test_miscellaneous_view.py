from mock import Mock, patch
try:
    import unittest2 as unittest
except ImportError:
    import unittest

from zope.component import provideAdapter
from zope.interface import implements, alsoProvides, noLongerProvides
from zope.publisher.browser import TestRequest

from Products.CMFCore.interfaces import ISiteRoot

from Products.PloneFormGen.interfaces import IPloneFormGenForm

from collective.pfg.payment.browser.miscellaneous import (
    Miscellaneous,
)
from collective.pfg.payment.interfaces import (
    IOrderNumberAware,
)

def create_annotations(annotations=None):
    if annotations is None:
        annotations = {}
    IAnnotations = Mock()
    IAnnotations.return_value = annotations
    return IAnnotations

def annotations():
    IAnnotations = Mock()
    IAnnotations.return_value = {'collective.pfg.payment': 'something'}
    return IAnnotations

class ViewTest(unittest.TestCase):

    @patch('collective.pfg.payment.browser.miscellaneous.IAnnotations', create_annotations())
    def test_make_order_number_aware(self):
        context = Mock()
        self.assertEqual(False, IOrderNumberAware.providedBy(context))
        request = Mock()
        view = Miscellaneous(context, request)
        view.make_order_number_aware()
        self.assertEqual(True, IOrderNumberAware.providedBy(context))

    @patch('collective.pfg.payment.browser.miscellaneous.IAnnotations', annotations())
    def test_make_order_number_unaware(self):
        context = Mock()
        alsoProvides(context, IOrderNumberAware)
        self.assertEqual(True, IOrderNumberAware.providedBy(context))
        request = Mock()
        view = Miscellaneous(context, request)
        view.make_order_number_unaware()
        self.assertEqual(False, IOrderNumberAware.providedBy(context))

    def test_is_order_number_aware(self):
        context = Mock()
        self.assertEqual(False, IOrderNumberAware.providedBy(context))
        request = Mock()
        view = Miscellaneous(context, request)
        self.assertEqual(False, view.is_order_number_aware())
        alsoProvides(context, IOrderNumberAware)
        self.assertEqual(False, view.is_order_number_aware())
        alsoProvides(context, IPloneFormGenForm)
        self.assertEqual(True, view.is_order_number_aware())
        noLongerProvides(context, IOrderNumberAware)
        self.assertEqual(False, view.is_order_number_aware())


def test_suite():
    return unittest.TestSuite([
        unittest.makeSuite(ViewTest),
    ])
