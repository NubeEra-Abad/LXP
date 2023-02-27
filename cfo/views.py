from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required

@login_required
def cfoclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'cfo/cfoclick.html')

@login_required    
def cfo_dashboard_view(request):
    try:
        if str(request.session['utype']) == 'cfo':
            dict={
            'total_course':0,
            'total_exam':0,
            'total_shortExam':0,
            'total_question':0,
            'total_learner':0
            }
        return render(request,'cfo/cfo_dashboard.html',context=dict)
    except:
        return render(request,'lxpapp/404page.html')
 