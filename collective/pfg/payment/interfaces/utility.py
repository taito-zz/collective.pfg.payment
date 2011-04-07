from zope.interface import Interface


class IAuthCode(Interface):
    """Calculates auth code for payment html form."""

    def __call__(keys, code=None, separator=None, capital=False):
        """Returns result of calculation."""
