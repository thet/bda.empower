# -*- coding: utf-8 -*-
from plone.app.content.interfaces import INameFromTitle
from zope.interface import implementer

import os
import random


random.seed(int(os.urandom(10).encode("hex"), 16))

_REF = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"


def int2str(value):
    res = []
    while value > 0:
        res.append(_REF[value % len(_REF)])
        value = int(value / len(_REF))
    res.reverse()
    return "".join(res)


@implementer(INameFromTitle)
class NameByRandomNumber(object):
    """Name Chooser for 3-byte Base62 ID

    """

    range = len(_REF) ** 3

    def __init__(self, context):
        self.context = context

    @property
    def title(self):
        return int2str(random.randint(1, self.range))
