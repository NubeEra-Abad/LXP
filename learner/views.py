from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def learnerclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'learner/learnerclick.html')

@login_required
def learner_dashboard_view(request):
    try:    
        if str(request.session['utype']) == 'learner':
            dict={
            'total_Video':0,
            'total_exam':0,
            }
            return render(request,'learner/learner_dashboard.html',context=dict)
    except:
        return render(request,'lxpapp/404page.html')
