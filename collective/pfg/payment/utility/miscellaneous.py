import re
try:
    import hashlib
except ImportError:
    import md5
from random import choice
from string import digits
from zope.interface import implements
from collective.pfg.payment.error import InfiniteLoopError
from collective.pfg.payment.interfaces import (
    IAuthCode,
    IRandomDigits,
    IRegularExpression,
)


class AuthCode(object):
    implements(IAuthCode)

    def __call__(self, keys=None, code='', separator='', capital=False):
        try:
            m = hashlib.md5()
        except NameError:
            m = md5.new()
        scode = code
        if keys is not None:
            for key in keys:
                scode += separator + key
        m.update(scode)
        hexdigest = m.hexdigest()
        if capital is True:
            return hexdigest.upper()
        return hexdigest

class RandomDigits(object):
    implements(IRandomDigits)

    def random_number(self, number):
        return "".join(choice(digits) for d in xrange(number))

    def loop(self, number, ids):
        digits = self.random_number(number)
        if digits not in ids:
            return digits

    def __call__(self, number, ids):
        if ids is None:
            return self.random_number(number)
        if len(ids) == 10 ** number:
            raise InfiniteLoopError(number)
        digits = self.random_number(number)
        while digits in ids:
            digits = self.random_number(number)
        else:
            return digits

class RegularExpression(object):

    implements(IRegularExpression)

    def email(self, string):
        check = re.compile(
            r"[a-zA-Z0-9._%-]+@([a-zA-Z0-9-]+\.)*[a-zA-Z]{2,4}"
        ).match
        if check(string):
            return True
        else:
            return False

    def integer(self, string):
        check = re.compile(
            r"^[0-9]+$"
        ).match
        if check(string):
            return True
        else:
            return False

    def float(self, string):
        if ',' in string:
            string = string.replace(',', '.')
        try:
            float(string)
            return True
        except ValueError:
            return False
