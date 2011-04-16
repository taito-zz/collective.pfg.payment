from zope.interface import Interface
from OFS.interfaces import IItem

#class INumbers(Interface):
class INumbers(IItem):
    """Folder which holds numbers"""

class INumber(Interface):
    """Number itself."""
