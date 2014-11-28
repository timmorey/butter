##
# coreobject.py - Created by Timothy Morey on 2/8/2014
#

import base64
import uuid

from django.db import models

class CoreObject(models.Model):
    class Meta:
        abstract = True
        app_label = 'core'


    id = models.CharField(default=None,
                          primary_key=True,
                          max_length=22)


    def addname(self, namevalue, dialect):
        from core.models.name import Name
        name = Name()
        name.value = namevalue
        name.dialect = dialect
        name.namedobject = self
        name.save()


    def delete(self, *args, **kwargs):
        for name in self.getnames():
            name.delete()

        super(CoreObject, self).delete(*args, **kwargs)


    def fromjson(self, json):
        from core.models.name import Name

        self.id = json['id']

        for namejson in json['names']:
            alreadyexists = False
            for name in self.getnames():
                if name.dialect.pk == namejson['dialect']:
                    alreadyexists = True
                    name.fromjson(namejson)
                    if name.value == '':
                        name.delete()
                    else:
                        name.save()
                    break
            
            if not alreadyexists:
                name = Name()
                name.namedobject = self
                name.fromjson(namejson)
                if name.value != '':
                    name.save()


    def generatepk(self):
        self.id = base64.urlsafe_b64encode(uuid.uuid4().bytes)[0:22]


    def getnames(self):
        from core.models.name import Name
        return Name.objects.filter(namedobject_id=self.id)


    def hasname(self, namevalue):
        for name in self.getnames():
            if name.value == namevalue:
                return True
        return False


    def nameindialect(self, dialect):
        for name in self.getnames():
            if name.dialect_id == dialect.pk:
                return name.value

    def internalname(self):
        from core.models.dialect import internaldialect
        return self.nameindialect(internaldialect())


    def defaultname(self):
        from core.models.dialect import defaultdialect
        return self.nameindialect(defaultdialect())


    def abbreviation(self):
        from core.models.dialect import abbrevdialect
        return self.nameindialect(abbrevdialect())


    def save(self, *args, **kwargs):
        if self.id is None:
            self.generatepk()
            
        super(CoreObject, self).save(*args, **kwargs)


    def tojson(self):
        json = { 'id': self.id,
                 'names': [] }
        for name in self.getnames():
            json['names'].append(name.tojson())
        
        return json
