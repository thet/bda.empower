# -*- coding: utf-8 -*-
from bda.empower import discourse
from bda.empower.i18n import _
from bda.empower.interfaces import IWorkspaceAware
from plone.app.textfield import RichText
from plone.app.z3cform.widget import AjaxSelectFieldWidget
from plone.autoform.directives import widget
from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import model
from zope import schema
from zope.interface import provider
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary

import logging


logger = logging.getLogger(__name__)


@provider(IVocabularyFactory)
def workspace_next_vocabulary_factory(context):
    return SimpleVocabulary(
        [
            SimpleTerm(term_id, title=title)
            for term_id, title in discourse.get_allowed_workspaces(context)
        ]
    )


@provider(IFormFieldProvider)
class IContributionBehavior(model.Schema, IWorkspaceAware):
    """ Schema Only Behavior Contribution
    """

    text = RichText(title=_(u"Text"), required=False)

    workspace = schema.Choice(
        title=u"Workspace", required=True, vocabulary="empower.next_workspaces"
    )

    assigned_experts = schema.TextLine(title=u"ExpertInnen", required=False)
    widget(
        "assigned_experts",
        AjaxSelectFieldWidget,
        vocabulary="plone.app.vocabularies.Users",
        pattern_options={"placeholder": u"Tippen und ExpertIn auswählen."},
    )
