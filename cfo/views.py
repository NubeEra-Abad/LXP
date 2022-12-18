from django.shortcuts import render,redirect
from . import models
from ilmsapp import models as iLMSModel
from ilmsapp import forms as ILMSFORM
from django.http import HttpResponseRedirect
from django.db import connection
from django.contrib import messages
from django.contrib.auth.models import User
from social_django.models import UserSocialAuth
from django.contrib.auth.decorators import login_required,user_passes_test

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
        return render(request,'ilmsapp/404page.html')
 
@login_required
def cfo_manage_learner_view(request):
    #try:    
        if str(request.session['utype']) == 'cfo':
            users = iLMSModel.Course.objects.raw("SELECT social_auth_usersocialauth.id,  social_auth_usersocialauth.provider,  social_auth_usersocialauth.uid,  auth_user.first_name,  auth_user.last_name,  CASE WHEN social_auth_usersocialauth.utype = 1 THEN 'Trainer' WHEN social_auth_usersocialauth.utype = 2 THEN 'learner' WHEN social_auth_usersocialauth.utype = 3 THEN 'cto' WHEN social_auth_usersocialauth.utype = 4 THEN 'cfo' END AS utype,  CASE WHEN social_auth_usersocialauth.status = 0 THEN 'Inactive' ELSE 'Active' END AS status,  ilmsapp_course.course_name,auth_user.id as user_id FROM  social_auth_usersocialauth  LEFT OUTER JOIN auth_user ON (social_auth_usersocialauth.user_id = auth_user.id)  LEFT OUTER JOIN ilmsapp_usercourse ON (auth_user.id = ilmsapp_usercourse.user_id)  LEFT OUTER JOIN ilmsapp_course ON (ilmsapp_usercourse.course_id = ilmsapp_course.id) WHERE social_auth_usersocialauth.utype = 2 OR social_auth_usersocialauth.utype = 0 ")
            return render(request,'cfo/cfo_manage_learner.html',{'users':users})
    #except:
        return render(request,'ilmsapp/404page.html')

@login_required
def cfo_active_learner_view(request,userid,pk):
    try:    
        if str(request.session['utype']) == 'cfo':
            cursor = connection.cursor()
            cursor.execute("UPDATE social_auth_usersocialauth SET status = 1 WHERE id = " + str(pk))
            users = UserSocialAuth.objects.all()
            isfirstlogin =iLMSModel.IsFirstLogIn.objects.all().filter(user_id = userid)
            if not isfirstlogin:
                isfirstlogin =iLMSModel.IsFirstLogIn.objects.create(user_id = userid)
                isfirstlogin.save()
            return render(request,'cfo/cfo_manage_learner.html',{'users':users})
    except:
        return render(request,'ilmsapp/404page.html')

@login_required
def cfo_inactive_learner_view(request,pk):
    try:    
        if str(request.session['utype']) == 'cfo':
            cursor = connection.cursor()
            cursor.execute("UPDATE social_auth_usersocialauth SET status = 0 WHERE id = " + str(pk))
            users = iLMSModel.Course.objects.raw("SELECT social_auth_usersocialauth.id,  social_auth_usersocialauth.provider,  social_auth_usersocialauth.uid,  auth_user.first_name,  auth_user.last_name,  CASE WHEN social_auth_usersocialauth.utype = 1 THEN 'Trainer' WHEN social_auth_usersocialauth.utype = 2 THEN 'learner' WHEN social_auth_usersocialauth.utype = 3 THEN 'cto' WHEN social_auth_usersocialauth.utype = 4 THEN 'cfo' END AS utype,  CASE WHEN social_auth_usersocialauth.status = 0 THEN 'Inactive' ELSE 'Active' END AS status,  ilmsapp_course.course_name,auth_user.id as user_id FROM  social_auth_usersocialauth  LEFT OUTER JOIN auth_user ON (social_auth_usersocialauth.user_id = auth_user.id)  LEFT OUTER JOIN ilmsapp_usercourse ON (auth_user.id = ilmsapp_usercourse.user_id)  LEFT OUTER JOIN ilmsapp_course ON (ilmsapp_usercourse.course_id = ilmsapp_course.id) WHERE social_auth_usersocialauth.utype = 2 OR social_auth_usersocialauth.utype = 0 ")
            return render(request,'cfo/cfo_manage_learner.html',{'users':users})
    except:
        return render(request,'ilmsapp/404page.html')

@login_required
def cfo_update_learner_course_view(request,pk):
    #try:    
        if str(request.session['utype']) == 'cfo':
            if request.method=="POST":
                course=request.POST['newcourse']
                print(course)
                usercouse = iLMSModel.UserCourse.objects.all().filter(user_id=pk)
                usercouse.delete()
                usercouse = iLMSModel.UserCourse.objects.create(user_id=pk,course_id=course,remarks='')
                usercouse.save()
                users = iLMSModel.Course.objects.raw("SELECT social_auth_usersocialauth.id,  social_auth_usersocialauth.provider,  social_auth_usersocialauth.uid,  auth_user.first_name,  auth_user.last_name,  CASE WHEN social_auth_usersocialauth.utype = 1 THEN 'Trainer' WHEN social_auth_usersocialauth.utype = 2 THEN 'learner' WHEN social_auth_usersocialauth.utype = 3 THEN 'cto' WHEN social_auth_usersocialauth.utype = 4 THEN 'cfo' END AS utype,  CASE WHEN social_auth_usersocialauth.status = 0 THEN 'Inactive' ELSE 'Active' END AS status,  ilmsapp_course.course_name,auth_user.id as user_id FROM  social_auth_usersocialauth  LEFT OUTER JOIN auth_user ON (social_auth_usersocialauth.user_id = auth_user.id)  LEFT OUTER JOIN ilmsapp_usercourse ON (auth_user.id = ilmsapp_usercourse.user_id)  LEFT OUTER JOIN ilmsapp_course ON (ilmsapp_usercourse.course_id = ilmsapp_course.id) WHERE social_auth_usersocialauth.utype = 2 OR social_auth_usersocialauth.utype = 0 ")
                return render(request,'cfo/cfo_manage_learner.html',{'users':users})
            course = iLMSModel.Course.objects.all()
            return render(request,'cfo/cfo_update_learner_course.html',{'courses':course,'uid':pk})
    #except:
        return render(request,'ilmsapp/404page.html')

@login_required
def cfo_coursetype_view(request):
    try:
        if str(request.session['utype']) == 'cfo':
            return render(request,'cfo/coursetype/cfo_coursetype.html')
    except:
        return render(request,'ilmsapp/404page.html')

@login_required
def cfo_add_coursetype_view(request):
    try:
        if str(request.session['utype']) == 'cfo':
            if request.method=='POST':
                coursetypeForm=ILMSFORM.CourseTypeForm(request.POST)
                if coursetypeForm.is_valid(): 
                    coursetypetext = coursetypeForm.cleaned_data["coursetype_name"]
                    coursetype = iLMSModel.CourseType.objects.all().filter(coursetype_name__iexact = coursetypetext)
                    if coursetype:
                        messages.info(request, 'CourseType Name Already Exist')
                        coursetypeForm=ILMSFORM.CourseTypeForm()
                        return render(request,'cfo/coursetype/cfo_add_coursetype.html',{'coursetypeForm':coursetypeForm})                  
                    else:
                        coursetypeForm.save()
                else:
                    print("form is invalid")
            coursetypeForm=ILMSFORM.CourseTypeForm()
            return render(request,'cfo/coursetype/cfo_add_coursetype.html',{'coursetypeForm':coursetypeForm})
    except:
        return render(request,'ilmsapp/404page.html')

@login_required
def cfo_update_coursetype_view(request,pk):
    #try:
        if str(request.session['utype']) == 'cfo':
            coursetype = iLMSModel.CourseType.objects.get(id=pk)
            coursetypeForm=ILMSFORM.CourseTypeForm(request.POST,instance=coursetype)
            if request.method=='POST':
                if coursetypeForm.is_valid(): 
                    coursetypetext = coursetypeForm.cleaned_data["coursetype_name"]
                    coursetype = iLMSModel.CourseType.objects.all().filter(coursetype_name__iexact = coursetypetext).exclude(id=pk)
                    if coursetype:
                        messages.info(request, 'CourseType Name Already Exist')
                        return render(request,'cfo/coursetype/cfo_update_coursetype.html',{'coursetypeForm':coursetypeForm})
                    else:
                        coursetypeForm.save()
                        coursetypes = iLMSModel.CourseType.objects.all()
                        return render(request,'cfo/coursetype/cfo_view_coursetype.html',{'coursetypes':coursetypes})
            return render(request,'cfo/coursetype/cfo_update_coursetype.html',{'coursetypeForm':coursetypeForm,'sub':coursetype.coursetype_name})
    #except:
        return render(request,'ilmsapp/404page.html')

@login_required
def cfo_view_coursetype_view(request):
    try:
        if str(request.session['utype']) == 'cfo':
            coursetypes = iLMSModel.CourseType.objects.all()
            return render(request,'cfo/coursetype/cfo_view_coursetype.html',{'coursetypes':coursetypes})
    except:
        return render(request,'ilmsapp/404page.html')

@login_required
def cfo_delete_coursetype_view(request,pk):
    try:
        if str(request.session['utype']) == 'cfo':  
            coursetype=iLMSModel.CourseType.objects.get(id=pk)
            coursetype.delete()
            return HttpResponseRedirect('/cfo/coursetype/cfo-view-coursetype')
        coursetypes = iLMSModel.CourseType.objects.all()
        return render(request,'cfo/coursetype/cfo_view_coursetype.html',{'coursetypes':coursetypes})
    except:
        return render(request,'ilmsapp/404page.html')

@login_required
def cfo_batch_view(request):
    try:
        if str(request.session['utype']) == 'cfo':
            return render(request,'cfo/batch/cfo_batch.html')
    except:
        return render(request,'ilmsapp/404page.html')

@login_required
def cfo_add_batch_view(request):
    #try:
        if str(request.session['utype']) == 'cfo':
            if request.method=='POST':
                batchForm=ILMSFORM.BatchForm(request.POST)
                if batchForm.is_valid(): 
                    batchtext = batchForm.cleaned_data["batch_name"]
                    batch = iLMSModel.Batch.objects.all().filter(batch_name__iexact = batchtext)
                    if batch:
                        messages.info(request, 'Batch Name Already Exist')
                        batchForm=ILMSFORM.BatchForm()
                        return render(request,'cfo/batch/cfo_add_batch.html',{'batchForm':batchForm})                  
                    else:
                        batchname = batchForm.cleaned_data["batch_name"]
                        
                        courseid = iLMSModel.Course.objects.only('id').get(course_name=batchForm.cleaned_data["courseID"]).id
                        coursetypeid = iLMSModel.CourseType.objects.only('id').get(coursetype_name=batchForm.cleaned_data["coursetypeID"]).id

                        batchtable = iLMSModel.Batch.objects.create(batch_name=batchname,stdate=batchForm.cleaned_data["stdate"],enddate=batchForm.cleaned_data["enddate"],coursetype_id=coursetypeid,course_id=courseid)
                        batchtable.save()
                        selectedlist = request.POST.getlist('listbox2')
                        for x in selectedlist:
                            trainerid = str(x)
                            trainerid=trainerid.split('-')
                            trainerid=trainerid[0]
                            batchtrainertable = iLMSModel.BatchTrainer.objects.create(batch_id=batchtable.id,trainer_id=trainerid)
                            batchtrainertable.save()
                else:
                    print("form is invalid")
            batchForm=ILMSFORM.BatchForm()
            trainers =  UserSocialAuth.objects.filter(user_id__in=User.objects.all(),status = True,utype=1)
            return render(request,'cfo/batch/cfo_add_batch.html',{'batchForm':batchForm,'trainers':trainers})
    #except:
        return render(request,'ilmsapp/404page.html')

@login_required
def cfo_update_batch_view(request,pk):
    #try:
        if str(request.session['utype']) == 'cfo':
            batch = iLMSModel.Batch.objects.get(id=pk)
            batchForm=ILMSFORM.BatchForm(request.POST,instance=batch)
            if request.method=='POST':
                if batchForm.is_valid(): 
                    batchtext = batchForm.cleaned_data["batch_name"]
                    batch = iLMSModel.Batch.objects.all().filter(batch_name__iexact = batchtext).exclude(id=pk)
                    if batch:
                        messages.info(request, 'Batch Name Already Exist')
                        return render(request,'cfo/batch/cfo_update_batch.html',{'batchForm':batchForm})
                    else:
                        batchForm.save()
                        batchs = iLMSModel.Batch.objects.all()
                        return render(request,'cfo/batch/cfo_view_batch.html',{'batchs':batchs})
            return render(request,'cfo/batch/cfo_update_batch.html',{'batchForm':batchForm,'sub':batch.batch_name})
    #except:
        return render(request,'ilmsapp/404page.html')

@login_required
def cfo_view_batch_view(request):
    try:
        if str(request.session['utype']) == 'cfo':
            batchs = iLMSModel.Batch.objects.all()
            return render(request,'cfo/batch/cfo_view_batch.html',{'batchs':batchs})
    except:
        return render(request,'ilmsapp/404page.html')

@login_required
def cfo_delete_batch_view(request,pk):
    try:
        if str(request.session['utype']) == 'cfo':  
            batch=iLMSModel.Batch.objects.get(id=pk)
            batch.delete()
            return HttpResponseRedirect('/cfo/batch/cfo-view-batch')
        batchs = iLMSModel.Batch.objects.all()
        return render(request,'cfo/batch/cfo_view_batch.html',{'batchs':batchs})
    except:
        return render(request,'ilmsapp/404page.html')