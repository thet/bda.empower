# -*- coding: utf-8 -*-
from plone.restapi.services import Service

import plone.api


class UserId(Service):

    def reply(self):
        """Reply to REST/JSON requests.
        """
        current_user = plone.api.user.get_current()
        return {"userid": current_user.id}
