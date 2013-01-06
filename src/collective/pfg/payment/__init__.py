from zope.i18nmessageid import MessageFactory

PaymentMessageFactory = MessageFactory('collective.pfg.payment')


def initialize(context):
    """Initializer called when used as a Zope 2 product."""
