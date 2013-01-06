from zope.interface import Interface


class IAuthCode(Interface):
    """Calculates auth code for payment html form."""

    def __call__(keys, code=None, separator=None, capital=False):
        """Returns result of calculation."""


class IRandomDigits(Interface):

    def __call__(number, ids):
        """Returns randome digits which is not in ids."""


class IRegularExpression(Interface):

    def email(string):
        """Returns True if the string is valid e-mail address else False."""

    def integer(string):
        """Returns True if the string can be converted into integer else False."""

    def float(string):
        """Returns True if the string can be converted into float else False."""
