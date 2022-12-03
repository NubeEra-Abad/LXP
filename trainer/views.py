from django.core.mail import send_mail
from django.shortcuts import render,redirect
from time import gmtime, strftime
from . import models
from ilmsapp import models as ILMSMODEL
from ilmsapp import forms as ILMSFORM
from django.db.models import Sum
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required,user_passes_test
from django.conf import settings
from datetime import datetime
def trainerclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'trainer/trainerclick.html')
def trainer_dashboard_view(request):
    try:
        if str(request.session['utype']) == 'trainer':
            dict={
            'total_course':0,
            'total_exam':0,
            'total_shortExam':0,
            'total_question':0,
            'total_learner':0
            }
        return render(request,'trainer/trainer_dashboard.html',context=dict)
    except:
        return render(request,'ilmsapp/404page.html')

