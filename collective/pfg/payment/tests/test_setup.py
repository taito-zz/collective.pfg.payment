from Products.CMFCore.utils import getToolByName
from collective.pfg.payment.tests.base import TestCase

import unittest


class TestSetup(TestCase):

    def afterSetUp(self):
        self.controlpanel = getToolByName(self.portal, 'portal_controlpanel')
        self.installer = getToolByName(self.portal, 'portal_quickinstaller')
        self.properties = getToolByName(self.portal, 'portal_properties')
        self.ccp = getattr(self.properties, 'collective_pfg_payment_properties')
        self.actions = getToolByName(self.portal, 'portal_actions')

    def test_is_pfg_installed(self):
        self.failUnless(self.installer.isProductInstalled('PloneFormGen'))

    def test_is_pfg_payment_installed(self):
        self.failUnless(self.installer.isProductInstalled('collective.pfg.payment'))

    ## controlpanel.xml
    def test_configlet(self):
        act = [action for action in self.controlpanel.listActions() if action.id == 'collective_pfg_payment_config'][0]
        self.assertEquals(u'Payment Config', act.title)
        self.assertEquals("collective.pfg.payment", act.appId)

        self.assertEquals("string:$portal_url/maintenance_icon.png", act.icon_expr.text)
        self.assertEquals("string:${portal_url}/@@payment-config", act.action.text)

    ## propertiestool.xml
    def test_collective_cart_properties(self):
        self.assertEquals('Payment Properties', self.ccp.getProperty('title'))
        self.assertEquals((), self.ccp.getProperty('fields'))
        self.assertEquals('', self.ccp.getProperty('mac'))
        self.assertEquals('', self.ccp.getProperty('separator'))
        self.assertEquals(True, self.ccp.getProperty('capital'))

    def test_collective_cart_property_types(self):
        self.assertEquals('string', self.ccp.getPropertyType('title'))
        self.assertEquals('lines', self.ccp.getPropertyType('fields'))
        self.assertEquals('string', self.ccp.getPropertyType('mac'))
        self.assertEquals('string', self.ccp.getPropertyType('separator'))
        self.assertEquals('boolean', self.ccp.getPropertyType('capital'))

    ## actions.xml
    def test_make_order_number_aware(self):
        matc = self.actions.object_buttons.make_order_number_aware
        self.assertEqual('Make Order Number Aware', matc.getProperty('title'))
        self.assertEqual('string:${globals_view/getCurrentObjectUrl}/@@make-order-number-aware', matc.getProperty('url_expr'))
        self.assertEqual('python: object.restrictedTraverse("not-order-number-aware")()', matc.getProperty('available_expr'))
        self.assertEqual(('Modify portal content',), matc.getProperty('permissions'))
        self.assertEqual(True, matc.getProperty('visible'))

    def test_make_order_number_unaware(self):
        matc = self.actions.object_buttons.make_order_number_unaware
        self.assertEqual('Make Order Number Unaware', matc.getProperty('title'))
        self.assertEqual('string:${globals_view/getCurrentObjectUrl}/@@make-order-number-unaware', matc.getProperty('url_expr'))
        self.assertEqual('python: object.restrictedTraverse("is-order-number-aware")()', matc.getProperty('available_expr'))
        self.assertEqual(('Modify portal content',), matc.getProperty('permissions'))
        self.assertEqual(True, matc.getProperty('visible'))

    def test_editProduct(self):
        matc = self.actions.object.edit_order_number
        self.assertEqual('Edit Order Number', matc.getProperty('title'))
        self.assertEqual('string:${object_url}/@@edit-order-number', matc.getProperty('url_expr'))
        self.assertEqual('python: object.restrictedTraverse("is-order-number-aware")()', matc.getProperty('available_expr'))
        self.assertEqual(('Modify portal content',), matc.getProperty('permissions'))
        self.assertEqual(True, matc.getProperty('visible'))

    ## Uninstalling
    def test_uninstall(self):
        self.installer.uninstallProducts(['collective.pfg.payment'])
        self.failUnless(not self.installer.isProductInstalled('collective.pfg.payment'))
        ids = [action.id for action in self.controlpanel.listActions()]
        self.failUnless('collective_pfg_payment_config' not in ids)
        self.failIf(hasattr(self.actions.object_buttons, 'make_order_number_aware'))
        self.failIf(hasattr(self.actions.object_buttons, 'make_order_number_unaware'))
        self.failIf(hasattr(self.actions.object, 'edit_order_number'))


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestSetup))
    return suite
