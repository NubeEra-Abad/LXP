from django.shortcuts import render,redirect
from . import models
from ilmsapp import models as ILMSMODEL
from ilmsapp import forms as ILMSFORM
from django.http import HttpResponseRedirect
from django.db import connection
def cfoclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'cfo/cfoclick.html')
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
        return render(request,'ilmsapp/404page.html')

def cfo_manage_learner_view(request):
    #try:    
        if str(request.session['utype']) == 'cfo':
            users = ILMSMODEL.Course.objects.raw("SELECT social_auth_usersocialauth.id,  social_auth_usersocialauth.provider,  social_auth_usersocialauth.uid,  auth_user.first_name,  auth_user.last_name,  CASE WHEN social_auth_usersocialauth.utype = 1 THEN 'Trainer' WHEN social_auth_usersocialauth.utype = 2 THEN 'learner' WHEN social_auth_usersocialauth.utype = 3 THEN 'cto' WHEN social_auth_usersocialauth.utype = 4 THEN 'cfo' END AS utype,  CASE WHEN social_auth_usersocialauth.status = 0 THEN 'Inactive' ELSE 'Active' END AS status,  ilmsapp_course.course_name,auth_user.id as user_id FROM  social_auth_usersocialauth  LEFT OUTER JOIN auth_user ON (social_auth_usersocialauth.user_id = auth_user.id)  LEFT OUTER JOIN ilmsapp_usercourse ON (auth_user.id = ilmsapp_usercourse.user_id)  LEFT OUTER JOIN ilmsapp_course ON (ilmsapp_usercourse.course_id = ilmsapp_course.id) WHERE social_auth_usersocialauth.utype = 2 OR social_auth_usersocialauth.utype = 0 ")
            return render(request,'cfo/cfo_manage_learner.html',{'users':users})
    #except:
        return render(request,'ilmsapp/404page.html')

def cfo_active_learner_view(request,pk):
    try:    
        if str(request.session['utype']) == 'cfo':
            cursor = connection.cursor()
            cursor.execute("UPDATE social_auth_usersocialauth SET status = 1 WHERE id = " + str(pk))
            users = ILMSMODEL.Course.objects.raw("SELECT social_auth_usersocialauth.id,  social_auth_usersocialauth.provider,  social_auth_usersocialauth.uid,  auth_user.first_name,  auth_user.last_name,  CASE WHEN social_auth_usersocialauth.utype = 1 THEN 'Trainer' WHEN social_auth_usersocialauth.utype = 2 THEN 'learner' WHEN social_auth_usersocialauth.utype = 3 THEN 'cto' WHEN social_auth_usersocialauth.utype = 4 THEN 'cfo' END AS utype,  CASE WHEN social_auth_usersocialauth.status = 0 THEN 'Inactive' ELSE 'Active' END AS status,  ilmsapp_course.course_name,auth_user.id as user_id FROM  social_auth_usersocialauth  LEFT OUTER JOIN auth_user ON (social_auth_usersocialauth.user_id = auth_user.id)  LEFT OUTER JOIN ilmsapp_usercourse ON (auth_user.id = ilmsapp_usercourse.user_id)  LEFT OUTER JOIN ilmsapp_course ON (ilmsapp_usercourse.course_id = ilmsapp_course.id) WHERE social_auth_usersocialauth.utype = 2 OR social_auth_usersocialauth.utype = 0 ")
            return render(request,'cfo/cfo_manage_learner.html',{'users':users})
    except:
        return render(request,'ilmsapp/404page.html')

def cfo_inactive_learner_view(request,pk):
    try:    
        if str(request.session['utype']) == 'cfo':
            cursor = connection.cursor()
            cursor.execute("UPDATE social_auth_usersocialauth SET status = 0 WHERE id = " + str(pk))
            users = ILMSMODEL.Course.objects.raw("SELECT social_auth_usersocialauth.id,  social_auth_usersocialauth.provider,  social_auth_usersocialauth.uid,  auth_user.first_name,  auth_user.last_name,  CASE WHEN social_auth_usersocialauth.utype = 1 THEN 'Trainer' WHEN social_auth_usersocialauth.utype = 2 THEN 'learner' WHEN social_auth_usersocialauth.utype = 3 THEN 'cto' WHEN social_auth_usersocialauth.utype = 4 THEN 'cfo' END AS utype,  CASE WHEN social_auth_usersocialauth.status = 0 THEN 'Inactive' ELSE 'Active' END AS status,  ilmsapp_course.course_name,auth_user.id as user_id FROM  social_auth_usersocialauth  LEFT OUTER JOIN auth_user ON (social_auth_usersocialauth.user_id = auth_user.id)  LEFT OUTER JOIN ilmsapp_usercourse ON (auth_user.id = ilmsapp_usercourse.user_id)  LEFT OUTER JOIN ilmsapp_course ON (ilmsapp_usercourse.course_id = ilmsapp_course.id) WHERE social_auth_usersocialauth.utype = 2 OR social_auth_usersocialauth.utype = 0 ")
            return render(request,'cfo/cfo_manage_learner.html',{'users':users})
    except:
        return render(request,'ilmsapp/404page.html')

def cfo_update_learner_course_view(request,pk):
    #try:    
        if str(request.session['utype']) == 'cfo':
            if request.method=="POST":
                course=request.POST['newcourse']
                print(course)
                usercouse = ILMSMODEL.UserCourse.objects.all().filter(user_id=pk)
                usercouse.delete()
                usercouse = ILMSMODEL.UserCourse.objects.create(user_id=pk,course_id=course,remarks='')
                usercouse.save()
                users = ILMSMODEL.Course.objects.raw("SELECT social_auth_usersocialauth.id,  social_auth_usersocialauth.provider,  social_auth_usersocialauth.uid,  auth_user.first_name,  auth_user.last_name,  CASE WHEN social_auth_usersocialauth.utype = 1 THEN 'Trainer' WHEN social_auth_usersocialauth.utype = 2 THEN 'learner' WHEN social_auth_usersocialauth.utype = 3 THEN 'cto' WHEN social_auth_usersocialauth.utype = 4 THEN 'cfo' END AS utype,  CASE WHEN social_auth_usersocialauth.status = 0 THEN 'Inactive' ELSE 'Active' END AS status,  ilmsapp_course.course_name,auth_user.id as user_id FROM  social_auth_usersocialauth  LEFT OUTER JOIN auth_user ON (social_auth_usersocialauth.user_id = auth_user.id)  LEFT OUTER JOIN ilmsapp_usercourse ON (auth_user.id = ilmsapp_usercourse.user_id)  LEFT OUTER JOIN ilmsapp_course ON (ilmsapp_usercourse.course_id = ilmsapp_course.id) WHERE social_auth_usersocialauth.utype = 2 OR social_auth_usersocialauth.utype = 0 ")
                return render(request,'cfo/cfo_manage_learner.html',{'users':users})
            course = ILMSMODEL.Course.objects.all()
            return render(request,'cfo/cfo_update_learner_course.html',{'courses':course,'uid':pk})
    #except:
        return render(request,'ilmsapp/404page.html')