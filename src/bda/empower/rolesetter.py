# -*- coding: utf-8 -*-
from .fingerpointing import fingerpointing_log
from plone import api

import logging


logger = logging.getLogger(__name__)


def _get_users_from_field(obj, fieldname):
    value = getattr(obj, fieldname, "")
    if not value:
        return []
    if value:
        return value.split(";")


def _revoke_roles(obj, rolename):
    """Remove all users with given local role"""
    for username in obj.users_with_local_role(rolename):
        api.user.revoke_roles(username=username, obj=obj, roles=[rolename])
        fingerpointing_log(
            "revoke_role_expert_assigned", username=username, id=obj.UID()
        )


def _set_role_for_users(obj, users, rolename):
    """Set for role for given users on obj"""
    for username in users:
        api.user.grant_roles(username=username, obj=obj, roles=[rolename])
        fingerpointing_log(
            "grant_role_experts_assigned", username=username, id=obj.UID()
        )


def _update_role_on_obj_using_users_from_field(obj, fieldname, rolename):
    logger.info("run subscriber update_expert_assigned_local_roles")
    _revoke_roles(obj, rolename)
    users = _get_users_from_field(obj, fieldname)
    _set_role_for_users(obj, users, rolename)
    obj.reindexObjectSecurity()


def update_expert_assigned_local_roles(obj, event):
    """ subcriber
    - to be configured to be called on ObjectCreated and ObjectModified
    """
    _update_role_on_obj_using_users_from_field(
        obj, "experts_assigned", "Expert"
    )


def update_initial_local_roles(obj, event):
    """ subcriber
    - to be configured to be called on ObjectCreated and ObjectModified
    """
    _update_role_on_obj_using_users_from_field(obj, "client", "Client")
    _update_role_on_obj_using_users_from_field(obj, "coordinators", "Expert")
    _update_role_on_obj_using_users_from_field(obj, "expert_pool", "Expert")
