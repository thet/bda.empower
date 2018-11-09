# -*- coding: utf-8 -*-
from Acquisition import aq_parent
from bda.empower import _
from plone.app.textfield import RichText
from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import model
from zope import schema
from zope.interface import provider
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary
from zope.schema.interfaces import IVocabularyFactory
from bda.empower.workspacedefinition import get_workspace_definition

import logging

logger = logging.getLogger(__name__)

INHERIT = "__inherit__"


@provider(IVocabularyFactory)
def workspace_next_vocabulary_factory(context):
    workspace_definition = get_workspace_definition()
    if context.portal_type not in ["Case", "Contribution"]:
        raise ValueError(
            "workspace_next_vocabulary_factory called in wrong context"
        )
    if context.portal_type == "Case":
        first_id, first_record = workspace_definition.items()[0]
        return SimpleVocabulary([SimpleTerm(first_id, first_record["title"])])
    parent = aq_parent(context)
    while parent.workspace == INHERIT:
        parent = aq_parent(parent)
        if parent.portal_type not in ["Case", "Contribution"]:
            raise ValueError(
                "workspace_next_vocabulary_factory called in wrong context"
            )
    vocab_values = [
        SimpleTerm(INHERIT, title=_("inherit", default=u"Inherited"))
    ]
    workspace_record = workspace_definition[parent.workspace]
    for workspace_id in workspace_record["next"]:
        vocab_values.append(
            SimpleTerm(
                workspace_id, workspace_definition[workspace_id]["title"]
            )
        )
    return SimpleVocabulary(vocab_values)


@provider(IFormFieldProvider)
class IContributionBehavior(model.Schema):
    """ Schema Only Behavior Contribution
    """

    text = RichText(title=_(u"Text"), required=False)

    workspace = schema.Choice(
        title=u"Workspace", required=True, vocabulary="empower.next_workspaces"
    )
