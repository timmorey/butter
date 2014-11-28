##
# name.py - Created by Timothy Morey on 2/8/2014
#

from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.db import models

from core.models.dialect import Dialect


class Name(models.Model):
    class Meta:
        app_label = 'core'

    namedobject_content_type = models.ForeignKey(ContentType,
                                                 related_name='+')
    namedobject_id = models.CharField(max_length=22)
    namedobject = generic.GenericForeignKey('namedobject_content_type',
                                            'namedobject_id')

    dialect = models.ForeignKey('Dialect',
                                related_name='words')

    value = models.CharField(max_length=256)


    def __str__(self):
        return self.__unicode__()

    
    def __unicode__(self):
        return self.value


    def fromjson(self, json):
        d = Dialect.objects.get(pk=json['dialect'])
        if d is None:
            d = Dialect()
            d.id = json['dialect']
            d.save()

        self.dialect = d
        self.value = json['value']
        self.save()


    def tojson(self):
        json = {'dialect': self.dialect.id,
                'value': self.value }
        return json
