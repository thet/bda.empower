# -*- coding: utf-8 -*-
from Products.CMFCore.utils import getToolByName
from Products.GenericSetup.interfaces import ISetupTool


_marker = []


def loadMigrationProfile(context, profile, steps=_marker):
    if not ISetupTool.providedBy(context):
        context = getToolByName(context, 'portal_setup')
    if steps is _marker:
        context.runAllImportStepsFromProfile(profile, purge_old=False)
    else:
        for step in steps:
            context.runImportStepFromProfile(profile,
                                             step,
                                             run_dependencies=False,
                                             purge_old=False)


def reload_gs_profile(context):
    loadMigrationProfile(context, "profile-bda.empower:default")
