
from django.http import HttpResponse
from django.shortcuts import render

from datetime import datetime
from django.contrib.auth import authenticate


# Create your views here.
def index(request):
    if not request.session.get('history'):
        request.session['history'] = []
    request.session['history'] = request.session['history'] + [datetime.now().strftime('%H:%M:%S')]
    print(request.session['history'])
    

    return render(request, 'user/profile.html')
