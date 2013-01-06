from zope.interface import Interface


class IOrderNumberAware(Interface):
    """Marker interface to be applied to FormFolder
    which will be order numbr aware."""
