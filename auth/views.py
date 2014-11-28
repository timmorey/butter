##
# views.py - Created by Timothy Morey on 2/17/2014
#

from django.contrib import auth
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        
        if user is not None and user.is_active:
            auth.login(request, user)
            return HttpResponse()
        
        else:
            raise Exception('Invalid username and/or password.')
    
    else:
        raise Exception('Invalid request method.')


@csrf_exempt
def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        return HttpResponse()
    
    else:
        raise Exception('Invalid request method.')
