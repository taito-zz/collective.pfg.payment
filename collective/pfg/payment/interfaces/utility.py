from zope.interface import Interface

class IAuthCode(Interface):
    """Calculates auth code for payment html form."""

    def __call__(code=None, separator=None, capital=False, *keys):
        """Returns result of calculation."""
