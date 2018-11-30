from bda.empower.i18n import _
from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import model
from zope import schema
from zope.interface import provider


@provider(IFormFieldProvider)
class IBasicwWithoutDescription(model.Schema):

    # default fieldset
    title = schema.TextLine(
        title=_(u"Subject"), required=True
    )
