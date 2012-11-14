from Products.PloneFormGen.interfaces import IPloneFormGenForm
from collective.pfg.payment.browser.miscellaneous import Miscellaneous
from collective.pfg.payment.interfaces import IOrderNumberAware
from zope.interface import alsoProvides
from zope.interface import noLongerProvides

import mock
import unittest


def create_annotations(annotations=None):
    if annotations is None:
        annotations = {}
    IAnnotations = mock.Mock()
    IAnnotations.return_value = annotations
    return IAnnotations


def annotations():
    IAnnotations = mock.Mock()
    IAnnotations.return_value = {'collective.pfg.payment': 'something'}
    return IAnnotations


class ViewTest(unittest.TestCase):

    @mock.patch('collective.pfg.payment.browser.miscellaneous.IAnnotations', create_annotations())
    def test_make_order_number_aware(self):
        context = mock.Mock()
        self.assertEqual(False, IOrderNumberAware.providedBy(context))
        request = mock.Mock()
        view = Miscellaneous(context, request)
        view.make_order_number_aware()
        self.assertEqual(True, IOrderNumberAware.providedBy(context))

    @mock.patch('collective.pfg.payment.browser.miscellaneous.IAnnotations', annotations())
    def test_make_order_number_unaware(self):
        context = mock.Mock()
        alsoProvides(context, IOrderNumberAware)
        self.assertEqual(True, IOrderNumberAware.providedBy(context))
        request = mock.Mock()
        view = Miscellaneous(context, request)
        view.make_order_number_unaware()
        self.assertEqual(False, IOrderNumberAware.providedBy(context))

    def test_is_order_number_aware(self):
        context = mock.Mock()
        self.assertEqual(False, IOrderNumberAware.providedBy(context))
        request = mock.Mock()
        view = Miscellaneous(context, request)
        self.assertEqual(False, view.is_order_number_aware())
        alsoProvides(context, IOrderNumberAware)
        self.assertEqual(False, view.is_order_number_aware())
        alsoProvides(context, IPloneFormGenForm)
        self.assertEqual(True, view.is_order_number_aware())
        noLongerProvides(context, IOrderNumberAware)
        self.assertEqual(False, view.is_order_number_aware())
