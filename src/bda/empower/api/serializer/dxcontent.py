# -*- coding: utf-8 -*-
from bda.empower.interfaces import IBdaEmpowerLayer
from plone.dexterity.interfaces import IDexterityContainer
from plone.dexterity.interfaces import IDexterityContent
from plone.restapi.interfaces import ISerializeToJson
from zope.component import adapter
from zope.interface import implementer
from plone.restapi.serializer import dxcontent


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
        return result


@implementer(ISerializeToJson)
@adapter(IDexterityContainer, IBdaEmpowerLayer)
class SerializeFolderToJson(dxcontent.SerializeFolderToJson):

    def _build_query(self):
        path = '/'.join(self.context.getPhysicalPath())
        query = {'path': {'depth': 1, 'query': path},
                 'sort_on': 'getObjPositionInParent'}
        return query

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
        return result
