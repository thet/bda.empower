# -*- coding: utf-8 -*-
from collective.fingerpointing.config import AUDIT_MESSAGE
from collective.fingerpointing.logger import log_info
from collective.fingerpointing.utils import get_request_information
from zope.interface.interfaces import implementer
from zope.interface.interfaces import IObjectEvent
from zope.interface.interfaces import ObjectEvent


def fingerpointing_log(name, **payload):
    user, ip = get_request_information()
    spayload = " ".join([(k + "=" + v) for k, v in payload.items()])
    log_info(AUDIT_MESSAGE.format(user, ip, name, spayload))


class IConfidentialObjectViewedEvent(IObjectEvent):
    """Event to fire if an confidential object was viewed
    """


@implementer(IConfidentialObjectViewedEvent)
class ConfidentialObjectViewedEvent(ObjectEvent):
    """Impl of Event to fire if an confidential object was viewed
    """

    def __init__(self, object, remark=None):
        super(ConfidentialObjectViewedEvent, self).__init__(object)
        self.remark = remark


def confidentialobjectviewed_logger(obj, event):
    """Log specific view events
    """
    payload = {"type": obj.portal_type, "id": obj.getId()}
    if event.remark is not None:
        payload["remark"] = event.remark
    fingerpointing_log("view", **payload)
