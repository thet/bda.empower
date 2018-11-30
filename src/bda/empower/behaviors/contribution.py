# -*- coding: utf-8 -*-
from Acquisition import aq_base
from Acquisition import aq_parent
from bda.empower import discourse
from bda.empower.i18n import _
from bda.empower.interfaces import IWorkspaceAware
from plone.app.textfield import RichText
from plone.autoform.directives import write_permission
from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import model
from zope import schema
from zope.interface import provider
from zope.schema.interfaces import IContextAwareDefaultFactory
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


@provider(IContextAwareDefaultFactory)
def default_workspace(context):
    """Provide default workspace
    """
    workspace = getattr(aq_base(aq_parent(context)), "workspace", None)
    if workspace is None:
        wdefs = discourse.get_workspace_definitions()
        return wdefs.keys()[0]
    return workspace


@provider(IFormFieldProvider)
class IContributionBehavior(model.Schema, IWorkspaceAware):
    """ Schema Only Behavior Contribution
    """

    text = RichText(title=_(u"Contribution"), required=False)

    workspace = schema.Choice(
        title=u"Workspace",
        required=False,
        vocabulary="empower.next_workspaces",
        defaultFactory=default_workspace,
    )
    write_permission(workspace="bda.empower.ModifyWorkspaceType")
