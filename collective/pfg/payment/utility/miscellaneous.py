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

    def __call__(self, code='', separator='', capital=False, keys):
        st = code
        try:
            m = hashlib.md5()
        except ImportError:
            m = md5.new()
        m.update(code)
        for key in keys:
            scode = separator + key
            st += scode
            m.update(st)
        hexdigest = m.hexdigest()
        if capital is True:
            hexdigest.upper()
        return hexdigest
