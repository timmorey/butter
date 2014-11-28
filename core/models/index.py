##
# index.py - Created by Timothy Morey on 9/20/2014
#

from django.db import models
from core.models import CoreObject


class Index(CoreObject):
    class Meta:
        app_label = 'core'


    parent = models.ForeignKey('Index',
                               blank=True,
                               null=True,
                               on_delete=models.CASCADE,
                               related_name='children')
    
    parentorder = models.IntegerField()


    def fromjson(self, json):
        from core.models.dialect import Dialect
        from core.modesl.unit import Unit

        super(Index, self).fromjson(json)

        if 'children' in json:
            for i in range(len(json['children'])):
                childjson = json['children'][i]
                index, created = Index.objects.get_or_create(pk=childjson['id'])
                index.fromjson(childjson)
                index.parent = self
                index.parentorder = i
                index.save()

        if 'contents' in json:
            for contentlink in self.contents:
                contentlink.delete()

            for i in range(len(json['contents'])):
                contentjson = json['contents'][i]
                if 'dialect' in contentjson:
                    dialect, created = Dialect.objects.get_or_create(pk=contentjson['dialect'])
                    if created:
                        dialect.save()

                    contentlink = IndexMembership()
                    contentlink.index = self
                    contentlink.content = dialect
                    contentlink.contentorder = i
                    contentlink.save()

                elif 'unit' in json['contents']:
                    unit, created = Unit.objects.get_or_create(pk=contentjson['unit'])
                    if created:
                        unit.save()

                    contentlink = IndexMembership()
                    contentlink.index = self
                    contentlink.content = unit
                    contentlink.contentorder = i
                    contentlink.save()

        self.save()


    def tojson(self):
        from core.models.dialect import Dialect
        from core.models.unit import Unit

        json = super(Index, self).tojson()
        
        childrenjson = []
        for index in sorted(self.children.all(), key=lambda index: index.parentorder):
            childrenjson.append(index.tojson())
        json['children'] = childrenjson

        contentsjson = []
        for contentlink in sorted(self.contents.all(), key=lambda item: item.content_order):
            if isinstance(contentlink.content, Dialect):
                contentsjson.append({'dialect': contentlink.content.pk})
            elif isinstance(contentlink.content, Unit):
                contentsjson.append({'unit': contentlink.content.pk})

        json['contents'] = contentsjson

        return json
