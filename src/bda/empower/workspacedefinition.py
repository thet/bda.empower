# -*- coding: utf-8 -*-
from bda.empower import _
from collections import OrderedDict


WORKSPACE_DEFINITION = OrderedDict()
WORKSPACE_DEFINITION["analysis"] = {
    "title": _("analysis", default=u"Analysis"),
    "next": ["strategy"],
    "no-parent": False,
}

WORKSPACE_DEFINITION["strategy"] = {
    "title": _("strategy", default=u"Strategy"),
    "next": ["action"],
    "no-parent": False,
}

WORKSPACE_DEFINITION["action"] = {
    "title": _("action", default=u"Action"),
    "next": ["evaluation"],
    "no-parent": True,
}

WORKSPACE_DEFINITION["evaluation"] = {
    "title": _("evaluation", default=u"Evaluation"),
    "next": ["strategy", "action"],
    "no-parent": False,
}
