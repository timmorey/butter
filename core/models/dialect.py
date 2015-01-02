##
# dialect.py - Created by Timothy Morey on 2/8/2014
#

from butter.core.models.coreobject import CoreObject

from django.db import models


class Dialect(CoreObject):
    class meta:
        app_label = 'core'


    base = models.ForeignKey('Dialect',
                             blank=True,
                             null=True,
                             on_delete=models.SET_NULL,
                             related_name='extensions')


    def __str__(self):
        return '%s' % (self.defaultname())

    
    def fromjson(self, json):
        super(Dialect, self).fromjson(json)

        if 'base' in json:
            d = Dialect.objects.get(pk=json['base'])
            self.base = d
        
        self.save()


    def tojson(self):
        json = super(Dialect, self).tojson()
        if self.base is not None:
            json['base'] = self.base.id

        return json
            

def defaultdialect():
    for dialect in Dialect.objects.all():
        if dialect.hasname('default'):
            return dialect

def internaldialect():
    for dialect in Dialect.objects.all():
        if dialect.hasname('internal'):
            return dialect

def abbrevdialect():
    for dialect in Dialect.objects.all():
        if dialect.hasname('default-abbreviation'):
           return dialect
