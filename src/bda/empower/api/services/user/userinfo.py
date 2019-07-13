# -*- coding: utf-8 -*-
from plone.restapi.interfaces import ISerializeToJson
from plone.restapi.services import Service
from zope.component import queryMultiAdapter

import plone.api


class UserInfo(Service):

    def reply(self):
        """Reply to REST/JSON requests.
        """
        user = plone.api.user.get_current()
        serializer = queryMultiAdapter((user, self.request), ISerializeToJson)
        return serializer()
