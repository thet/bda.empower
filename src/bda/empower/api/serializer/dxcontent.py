# -*- coding: utf-8 -*-
from bda.empower import discourse
from bda.empower.interfaces import IBdaEmpowerLayer
from plone.dexterity.interfaces import IDexterityContainer
from plone.dexterity.interfaces import IDexterityContent
from plone.restapi.interfaces import ISerializeToJson
from plone.restapi.serializer import dxcontent
from zope.component import adapter
from zope.interface import implementer

import plone.api


def filter_permissions(perms):
    """Filter for bda.empower permissions and other important permissions.
    """

    #   id="bda.empower.AddContribution"
    #   title="bda.empower: Add Contribution"
    #   id="bda.empower.AddCase"
    #   title="bda.empower: Add Case"
    #   id="bda.empower.ModifyClient"
    #   title="bda.empower: Modify Client"
    #   id="bda.empower.ModifyExpertPool"
    #   title="bda.empower: Modify Expert Pool"
    #   id="bda.empower.ModifyCoordinators"
    #   title="bda.empower: Modify Coordinators"
    #   id="bda.empower.ModifyExpertsAssigned"
    #   title="bda.empower: Modify Experts Assigned"

    default_perms = [
        "View",
        "Add portal content",
        "Modify portal content",
        "Delete objects",
        "bda.empower: Add Contribution",
        "bda.empower: Add Case",
        "bda.empower: Modify Client",
        "bda.empower: Modify Expert Pool",
        "bda.empower: Modify Coordinators",
        "bda.empower: Modify Experts Assigned",
    ]
    perms = {p: v for p, v in perms.items() if p in default_perms}
    return perms


@implementer(ISerializeToJson)
@adapter(IDexterityContent, IBdaEmpowerLayer)
class SerializeToJson(dxcontent.SerializeToJson):

    def __call__(self, *args, **kwargs):
        result = super(SerializeToJson, self).__call__(*args, **kwargs)
        # TODO
        # obj = self.getVersion(kwargs['version'])
        obj = self.context
        result['can_edit'] = self.check_permission('Modify portal content', obj)
        result['can_delete'] = self.check_permission('Delete objects', obj)
        result['can_add'] = {
            'Contribution': self.check_permission('bda.empower.AddContribution', obj),
            'File': self.check_permission('Add portal content', obj),
            'Image': self.check_permission('Add portal content', obj)
        }

        current_case = discourse.get_initial_root(self.context)
        result['current_case'] = current_case.absolute_url() if current_case else None
        result['workspace_root'] = discourse.is_workspace_root(self.context)
        result['permissions'] = filter_permissions(
            plone.api.user.get_permissions(obj=self.context)
        )

        return result


@implementer(ISerializeToJson)
@adapter(IDexterityContainer, IBdaEmpowerLayer)
class SerializeFolderToJson(dxcontent.SerializeFolderToJson):

    def __call__(self, *args, **kwargs):
        result = super(SerializeFolderToJson, self).__call__(*args, **kwargs)
        # TODO
        # obj = self.getVersion(kwargs['version'])
        obj = self.context
        result['can_edit'] = self.check_permission('Modify portal content', obj)
        result['can_delete'] = self.check_permission('Delete objects', obj)
        result['can_add'] = {
            'Contribution': self.check_permission('bda.empower.AddContribution', obj),
            'File': self.check_permission('Add portal content', obj),
            'Image': self.check_permission('Add portal content', obj)
        }

        current_case = discourse.get_initial_root(self.context)
        result['current_case'] = current_case.absolute_url() if current_case else None
        result['workspace_root'] = discourse.is_workspace_root(self.context)
        result['permissions'] = filter_permissions(
            plone.api.user.get_permissions(obj=self.context)
        )

        return result
