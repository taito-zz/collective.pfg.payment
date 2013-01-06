from collective.pfg.payment.browser.template import PaymentConfigView

import mock
import unittest


class Template(object):

    def __init__(self, template):
        self.template = template

    def __call__(self):
        return self.template


def template(temp):
    return temp


class ViewTest(unittest.TestCase):

    def test_payment_config__view_template(self):
        context = mock.Mock()
        request = mock.Mock()
        request.set.return_value = mock.Mock()
        view = PaymentConfigView(context, request)
        view.template = mock.Mock()
        self.failIf(view.template.called)
        view()
        self.failUnless(view.template.called)
