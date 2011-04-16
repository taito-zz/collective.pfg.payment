from persistent import Persistent
from zope.interface import implements
from collective.pfg.payment.interfaces import INumbers


class Numbers(Persistent):

    implements(INumbers)

    def __init__(
        self,
        numbering_type = 'Incremental',
        next_incremental_number=1,
        random_number_digits=5,
        numbers =  [],
        mac = '',
        fields = [],
        separator = '',
        capital = False,
        local_payment = False,
    ):
        self.numbering_type = numbering_type
        self.next_incremental_number = next_incremental_number
        self.random_number_digits = random_number_digits
        self.numbers = numbers
        self.mac = mac
        self.fields = fields
        self.separator = separator
        self.capital = capital
        self.local_payment = local_payment
