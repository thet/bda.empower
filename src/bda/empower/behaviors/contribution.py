# -*- coding: utf-8 -*-
from bda.empower import _
from plone.app.textfield import RichText
from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import model
from zope import schema
from zope.interface import provider
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary

workspace_vocabulary = SimpleVocabulary(
    [
        SimpleTerm("case", title=u"Case"),
        SimpleTerm("inherited", title=u"Inherited"),
        SimpleTerm("analyse", title=u"Analyse"),
        SimpleTerm("strategie", title=u"Strategie"),
        SimpleTerm("action", title=u"Action"),
    ]
)


@provider(IFormFieldProvider)
class IContributionBehavior(model.Schema):
    """ Schema Only Behavior Contribution
    """

    text = RichText(title=_(u"Text"), required=False)

    workspace = schema.Choice(
        title=u"Workspace",
        required=True,
        vocabulary=workspace_vocabulary,
        default="inherited",
    )
