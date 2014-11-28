##
# unit.py - Created by Timothy Morey on 2/8/2014
#

from django.db import models

from core.models import CoreObject


class Unit(CoreObject):
    class Meta:
        app_label = 'core'


    unittype = models.CharField(max_length=64, default='')

    tobasefactor = models.FloatField(default=1.0)
    
    baseoffset = models.FloatField(default=0.0)
    
    unitoffset = models.FloatField(default=0.0)
    
    baseunit = models.ForeignKey('Unit',
                                 blank=True,
                                 null=True,
                                 on_delete=models.PROTECT,
                                 related_name='+')


    def __str__(self):
        return '%s (%s)' % (self.defaultname(), self.abbreviation())


    def commonbase(self, other):
        # base cases
        #
        if self is None or other is None:
            return None
        elif self.pk == other.pk:
            return self

        # check all of other's bases to see if any of them match self
        #
        otherbase = other.baseunit
        while otherbase is not None:
            if self.pk == otherbase.pk:
                return self
            otherbase = otherbase.baseunit

        # recurse to self.baseunit, if ther is one
        #
        if self.baseunit is None:
            return None
        else:
            return self.baseunit.commonbase(other)
        

    def convertto(self, unit, value):
        commbase = self.commonbase(unit)
        if commbase is not None:
            pathtobase = []
            pathfrombase = []
            curunit = self
            while not curunit.pk == commbase.pk:
                pathtobase.append(curunit)
                curunit = curunit.baseunit

            curunit = unit
            while not curunit.pk == commbase.pk:
                pathfrombase.insert(0, curunit)
                curunit = curunit.baseunit

            for curunit in pathtobase:
                value += curunit.unitoffset
                value *= curunit.tobasefactor
                value += curunit.baseoffset

            for curunit in pathfrombase:
                value -= curunit.baseoffset
                value /= curunit.tobasefactor
                value -= curunit.unitoffset

        return value


    def fromjson(self, json):
        super(Unit, self).fromjson(json)

        if 'type' in json:
            self.unittype = json['type']

        if 'toBaseFactor' in json:
            self.tobasefactor = float(json['toBaseFactor'])

        if 'baseOffset' in json:
            self.baseoffset = float(json['baseOffset'])

        if 'unitOffset' in json:
            self.unitoffset = float(json['unitOffset'])

        if 'baseUnit' in json:
            baseunitid = json['baseUnit']
            if len(baseunitid.strip()) > 0:
                self.baseunit, created = Unit.objects.get_or_create(pk=json['baseUnit'])
            else:
                self.baseunit = None
                self.tobasefactor = 1
                self.baseoffset = 0
                self.unitoffset = 0
            
        self.save()


    def tojson(self):
        json = super(Unit, self).tojson()

        json['type'] = self.unittype
        json['toBaseFactor'] = self.tobasefactor
        json['baseOffset'] = self.baseoffset
        json['unitOffset'] = self.unitoffset
    
        if self.baseunit is not None:
            json['baseUnit'] = self.baseunit.id

        return json


def createunit(unittype=None,
               baseunit=None, 
               tobasefactor=1, 
               baseoffset=0, 
               unitoffset=0,
               defaultname=None,
               internalname=None,
               abbrev=None):
    
    from core.models.dialect import Dialect
    from core.models.dialect import defaultdialect
    from core.models.dialect import internaldialect
    from core.models.dialect import abbrevdialect

    unit = Unit()
    unit.unittype = unittype
    unit.baseunit = baseunit
    unit.tobasefactor = tobasefactor
    unit.baseoffset = baseoffset
    unit.unitoffset = unitoffset
    unit.save()

    if defaultname is not None:
        unit.addname(defaultname, defaultdialect())

    if internalname is not None:
        unit.addname(internalname, internaldialect())

    if abbrev is not None:
        unit.addname(abbrev, abbrevdialect())

    return unit


def findunits(searchstring):
    results = []

    for unit in Unit.objects.all():
        for name in unit.getnames():
            if searchstring.lower() in name.value.lower():
                if not unit in results:
                    results.append(unit)

    return results


def unitwithabbrev(abbrev):
    from core.models.dialect import abbrevdialect

    for unit in Unit.objects.all():
        for name in unit.getnames():
            if name.dialect_id == abbrevdialect().pk:
                if name.value == abbrev:
                    return unit
