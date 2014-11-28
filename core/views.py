##
# views.py - Created by Timothy Morey on 2/8/2014
#

import json

from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.csrf import csrf_exempt

from core.models import Dialect, Index, Resource, Unit


################################################################################
# /dialect
#

def dialectroot(request):
    if request.method == 'GET':
        response = {'dialects': []}
        for dialect in Dialect.objects.all():
            response['dialects'].append(dialect.tojson())
        return HttpResponse(json.dumps(response), 
                            content_type='application/json')

    else:
        raise Exception('Invalid request method')

def dialectdetail(request, dialectid):
    if request.method == 'GET':
        dialect = get_object_or_404(Dialect, id=dialectid)
        return HttpResponse(json.dumps(dialect.tojson()), 
                            content_type='application/json')

    elif request.method == 'POST':
        if not request.user.is_authenticated():
            return HttpResponse(status=401)

        dialect, created = Dialect.objects.get_or_create(pk=dialectid)
        index.fromjson(json.loads(request.body))
        return HttpResponse()

    elif request.method == 'DELETE':
        if not request.user.is_authenticated():
            return HttpResponse(status=401)

        dialect = get_object_or_404(Dialect, id=dialectid)
        dialect.delete()
        return HttpResponse()

    else:
        raise Exception('Invalid request method')

################################################################################
# /index
#

def indexroot(request):
    if request.method == 'GET':
        response = {'indexes': []}
        for index in Index.objects.all():
            response['indexes'].append(index.tojson())
        return HttpResponse(json.dumps(response), 
                            content_type='application/json')

    else:
        raise Exception('Invalid request method')


@csrf_exempt
def indexdetail(request, indexid):
    if request.method == 'GET':
        index = get_object_or_404(Index, id=indexid)
        return HttpResponse(json.dumps(index.tojson()), 
                            content_type='application/json')

    elif request.method == 'POST':
        if not request.user.is_authenticated():
            return HttpResponse(status=401)

        index, created = Index.objects.get_or_create(pk=indexid)
        index.fromjson(json.loads(request.body))
        return HttpResponse()

    elif request.method == 'DELETE':
        if not request.user.is_authenticated():
            return HttpResponse(status=401)

        index = get_object_or_404(Index, id=indexid)
        index.delete()
        return HttpResponse()

    else:
        raise Exception('Invalid request method')

################################################################################
# /resource
#

def resourceroot(request):
    if request.method == 'GET':
        response = {'resources': []}
        for resource in Resource.objects.all():
            response['resources'].append(resource.tojson())
        return HttpResponse(json.dumps(response), 
                            content_type='application/json')

    else:
        raise Exception('Invalid request method')

@csrf_exempt
def resourcedetail(request, resourceid):
    if request.method == 'GET':
        resource = get_object_or_404(Resource, id=resourceid)
        return HttpResponse(json.dumps(resource.tojson()), 
                            content_type='application/json')

    elif request.method == 'POST':
        if not request.user.is_authenticated():
            return HttpResponse(status=401)

        resource, created = Resource.objects.get_or_create(pk=resourceid)
        resource.fromjson(json.loads(request.body))
        return HttpResponse()

    elif request.method == 'DELETE':
        if not request.user.is_authenticated():
            return HttpResponse(status=401)

        resource = get_object_or_404(Resource, id=resourceid)
        resource.delete()
        return HttpResponse()

    else:
        raise Exception('Invalid request method')

################################################################################
# /unit
#

def unitroot(request):
    if request.method == 'GET':
        response = {'units': []}
        for unit in Unit.objects.all():
            response['units'].append(unit.tojson())
        return HttpResponse(json.dumps(response), 
                            content_type='application/json')

    else:
        raise Exception('Invalid request method')


@csrf_exempt
def unitdetail(request, unitid):
    if request.method == 'GET':
        unit = get_object_or_404(Unit, id=unitid)
        return HttpResponse(json.dumps(unit.tojson()), 
                            content_type='application/json')

    elif request.method == 'POST':
        if not request.user.is_authenticated():
            return HttpResponse(status=401)

        unit, created = Unit.objects.get_or_create(pk=unitid)
        unit.fromjson(json.loads(request.body))
        return HttpResponse()

    elif request.method == 'DELETE':
        if not request.user.is_authenticated():
            return HttpResponse(status=401)

        unit = get_object_or_404(Unit, id=unitid)
        unit.delete()
        return HttpResponse()

    else:
        raise Exception('Invalid request method')

