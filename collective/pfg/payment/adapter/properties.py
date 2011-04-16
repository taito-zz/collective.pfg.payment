from zope.component import adapts
from zope.interface import implements
from OFS.interfaces import IItem
#from Products.CMFPlone.interfaces.properties import ISimpleItemWithProperties
from collective.pfg.payment.interfaces import IProperties


class Properties(object):
#    adapts(ISimpleItemWithProperties)
    adapts(IItem)
    implements(IProperties)

    def __init__(self, context):
        self.context = context

    def __getattr__(self, attr):
        if attr == 'context':
            return self.context
        else:
            if hasattr(self.context, 'getProperty'):
                return self.context.getProperty(attr)
            else:
                return getattr(self.context, attr)

    def __setattr__(self, attr, value):
        if attr == 'context':
            self.__dict__[attr] = value
        else:
            if hasattr(self.context, '_updateProperty'):
                self.context._updateProperty(attr, value)
            else:
                setattr(self.context, attr, value)

    def input_field(self, attr, size):
#        return '<input type="text" name="%s"\
#             id="%s" value="%s" size="%s" />' % (
#            attr, attr, self.context.getProperty(attr), size)
        return '<input type="text" name="%s"\
             id="%s" value="%s" size="%s" />' % (
            attr, attr, getattr(self.context, attr), size)


    def boolean_field(self, attr):
#        if self.context.getProperty(attr) == True:
        if getattr(self.context, attr) == True or getattr(self.context, attr) == 'on':
            return '<input type="checkbox" id="%s" name="%s" value="on" checked="checked" />' % (attr, attr)
        else:
            return '<input type="checkbox" name="%s" id="%s" value="on" />' % (
                attr, attr)

    def textarea_field(self, attr, rows, cols):
        html = '<textarea name="%s" id="%s" rows="%s" cols="%s">' % (
            attr, attr, rows, cols)
#        for field in self.context.getProperty(attr):
        for field in getattr(self.context, attr):
            html += '%s\r\n' % field
        html += '</textarea>'
        return html
