# -*- coding: utf-8 -*-
from .fingerpointing import fingerpointing_log
from plone import api

import logging


logger = logging.getLogger(__name__)

ROLENAME = "Expert"


def update_expert_assigned_local_roles(obj, event):
    """ subcriber on ICOntribution

    to be configured to be called on ObjectCreated and ObjectModified
    """
    logger.info("run subscriber update_expert_assigned_local_roles")
    return
    # remove all users with local role "AKI EC Assigned" on parent (TN)
    for username in obj.users_with_local_role(ROLENAME):
        api.user.revoke_roles(username=username, obj=obj, roles=[ROLENAME])
        fingerpointing_log(
            "revoke_role_expert_assigned", username=username, id=obj.UID()
        )
    users = obj.assigned_experts or ""
    # set for einzel_coach'es from Verlauf local role "AKI EC Assigned"
    for username in users.split(";"):
        api.user.grant_roles(username=username, obj=obj, roles=[ROLENAME])
        fingerpointing_log(
            "grant_role_aki_ec_assigned", username=username, id=obj.UID()
        )
    obj.reindexObjectSecurity()
