from zope.interface import Interface, Attribute


class IProperties(Interface):
    """Adapts properties to make properties attributes,
easy to get and set vlues."""

    fields = Attribute('Fields to be used for auth code calculation.')
    mac = Attribute('Auth Mac provided by payment provider.')
    separator = Attribute('Separator used for auth code calculation.')
    capital = Attribute('If the calculated auth code must be capital or not.')

    def input_field(attr, size):
        """Returns input string for html."""

    def boolean_field(attr):
        """Returns html boolean field. """

    def textarea_field(attr, rows, cols):
        """Returns html textarea field."""

    def fields():
        """Returns html fields for all the field."""
