from Products.CMFCore.utils import getToolByName
from StringIO import StringIO


def uninstall(self):
    out = StringIO()
    print >> out, "Removing collective.pfg.payment"

    controlpanel = getToolByName(self, 'portal_controlpanel')
    actids = [o.id for o in controlpanel.listActions()]
    controlpanel.deleteActions([actids.index('collective_pfg_payment_config')])

    return out.getvalue()
