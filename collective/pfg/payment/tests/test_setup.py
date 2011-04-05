import unittest
from Products.CMFCore.utils import getToolByName
from collective.pfg.payment.tests.base import TestCase

class TestSetup(TestCase):

    def afterSetUp(self):
#        self.catalog = getToolByName(self.portal, 'portal_catalog')
#        self.wftool = getToolByName(self.portal, 'portal_workflow')
        self.controlpanel = getToolByName(self.portal, 'portal_controlpanel')
        self.installer = getToolByName(self.portal, 'portal_quickinstaller')
#        self.skins      = getToolByName(self.portal, 'portal_skins')
        self.properties = getToolByName(self.portal, 'portal_properties')
#        self.site_properties = getattr(self.properties, 'site_properties')
#        self.navtree_properties = getattr(self.properties, 'navtree_properties')
        self.ccp = getattr(self.properties, 'collective_pfg_payment_properties')

    def test_is_pfg_installed(self):
        self.failUnless(self.installer.isProductInstalled('PloneFormGen'))

    def test_is_pfg_payment_installed(self):
        self.failUnless(self.installer.isProductInstalled('collective.pfg.payment'))

    ## controlpanel.xml
    def test_configlet(self):
        act = [action for action in self.controlpanel.listActions() if action.id == 'collective_pfg_payment_config'][0]
        self.assertEquals(u'Payment Config', act.title)
        self.assertEquals("collective.pfg.payment", act.appId)

        try:
            ## Plone4
            self.assertEquals("string:$portal_url/maintenance_icon.png", act.icon_expr.text)
        except AttributeError:
            ## Plone3
            pass

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


    ## Uninstalling
    def test_uninstall(self):
        self.installer.uninstallProducts(['collective.pfg.payment'])
        self.failUnless(not self.installer.isProductInstalled('collective.pfg.payment'))
        ids = [action.id for action in self.controlpanel.listActions()]
        self.failUnless('collective_pfg_payment_config' not in ids)
#        self.failUnless(not hasattr(self.properties, 'collective_cart_properties'))

def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestSetup))
    return suite
