from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required

def trainerclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'trainer/trainerclick.html')

@login_required
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
        return render(request,'lxpapp/404page.html')
