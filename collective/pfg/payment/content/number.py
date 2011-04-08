from persistent import Persistent
#from BTrees.OOBTree import OOBTree

from zope.interface import implements
from persistent.list import PersistentList

from collective.pfg.payment.interfaces import INumbers


class Numbers(Persistent):

    implements(INumbers)

    def __init__(
        self,
        numbering_type = 'Incremental',
        next_incremental_number=1,
        random_number_digits=5,
#        numbers =  PersistentList()
        numbers =  []
    ):
        self.numbering_type = numbering_type
        self.next_incremental_number = next_incremental_number
        self.random_number_digits = random_number_digits
        self.numbers = numbers


#class Number(Persistent):

#    implements(INumber)

#    def __init__(self, number):
#        self.number = number

#    def __call__(self):
#        pass
