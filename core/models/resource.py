##
# resource.py - Created by Timothy Morey on 2/8/2014
#

from django.db import models

from core.models import CoreObject


class Resource(CoreObject):
    class Meta:
        app_label = 'core'


    isa = models.ForeignKey('Unit',
                            blank=True,
                            null=True,
                            on_delete=models.PROTECT,
                            related_name='types')


    def __str__(self):
        return self.defaultname()


    def fromjson(self, json):
        super(Resource, self).fromjson(json)

        if 'isa' in json:
            self.isa = Resource.objects.get_or_create(pk=json['isa'])

        self.save()


    def tojson(self):
        json = super(Resource, self).tojson()
        
        if self.isa is not None:
            json['isa'] = self.isa.id

        return json
