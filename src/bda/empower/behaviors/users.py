# -*- coding: utf-8 -*-
from bda.empower.i18n import _
from plone.app.z3cform.widget import AjaxSelectFieldWidget
from plone.autoform.directives import widget
from plone.autoform.directives import write_permission
from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import model
from zope import schema
from zope.interface import provider

import logging


logger = logging.getLogger(__name__)


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
        vocabulary="plone.app.vocabularies.Users",
        pattern_options={"placeholder": _(u"Type and select expert.")},
    )
    write_permission(experts_assigned="bda.empower.ModifyExpertsAssigned")
