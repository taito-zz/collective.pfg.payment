try:
    import hashlib
except ImportError:
    import md5
from zope.interface import implements
from collective.pfg.payment.interfaces import (
    IAuthCode,
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
