# -*- coding: utf-8 -*-
from Acquisition import aq_parent
from bda.empower.i18n import _
from plone import api
from plone.app.z3cform.widget import AjaxSelectFieldWidget
from plone.autoform.directives import widget
from plone.autoform.directives import write_permission
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
def users_from_parent_vocabulary_factory(context):
    parent = aq_parent(context)
    if IClientAndExpertpoolAssignmentBehavior.providedBy(parent):
        attribute = "expert_pool"
    elif IExpertAssignmentBehavior.providedBy(parent):
        attribute = "experts_assigned"
    else:
        raise ValueError("Invalid parent context")
    values = (getattr(parent, attribute) or "").split(";")

    terms = [
        SimpleTerm(
            userid, title=api.user.get(userid=userid).getProperty("fullname")
        )
        for userid in values
    ]
    return SimpleVocabulary(terms)


@provider(IFormFieldProvider)
class IClientAndExpertpoolAssignmentBehavior(model.Schema):

    client = schema.TextLine(title=_(u"Client"), required=False)
    widget(
        "client",
        AjaxSelectFieldWidget,
        vocabulary="plone.app.vocabularies.Users",
        pattern_options={"placeholder": _(u"Type and select client.")},
    )
    write_permission(client="bda.empower.ModifyClient")

    coordinators = schema.TextLine(title=_(u"Coordinators"), required=False)
    widget(
        "coordinators",
        AjaxSelectFieldWidget,
        vocabulary="plone.app.vocabularies.Users",
        pattern_options={"placeholder": _(u"Type and select coordinator.")},
    )
    write_permission(expert_pool="bda.empower.ModifyExpertPool")

    expert_pool = schema.TextLine(title=_(u"Expert Pool"), required=False)
    widget(
        "expert_pool",
        AjaxSelectFieldWidget,
        vocabulary="plone.app.vocabularies.Users",
        pattern_options={"placeholder": _(u"Type and select expert.")},
    )
    write_permission(expert_pool="bda.empower.ModifyExpertPool")


@provider(IFormFieldProvider)
class IExpertAssignmentBehavior(model.Schema):

    experts_assigned = schema.TextLine(title=_(u"Experts"), required=False)
    widget(
        "experts_assigned",
        AjaxSelectFieldWidget,
        vocabulary="empower.parent_allowed_users",
        pattern_options={"placeholder": _(u"Type and select expert.")},
    )
    write_permission(experts_assigned="bda.empower.ModifyExpertsAssigned")
