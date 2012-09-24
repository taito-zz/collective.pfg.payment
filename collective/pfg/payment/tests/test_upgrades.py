from Products.CMFCore.utils import getToolByName
from collective.pfg.payment.tests.base import TestCase


class TestSetup(TestCase):

    def test_upgrade_1000_to_1001(self):
        actions = getToolByName(self.portal, 'portal_actions')
        object_buttons = getattr(actions, 'object_buttons')
        action = getattr(object_buttons, 'make_order_number_aware')
        action.available_expr = 'AVAILABLE_EXPR'

        self.assertEqual(action.available_expr, 'AVAILABLE_EXPR')

        from collective.pfg.payment.upgrades import upgrade_1000_to_1001
        upgrade_1000_to_1001(self.portal)

        self.assertEqual(action.available_expr, 'python: object.restrictedTraverse("not-order-number-aware")()')
