from django.shortcuts import render,redirect
from . import models
from lxpapp import models as LXPModel
from lxpapp import forms as LXPFORM
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
        return render(request,'lxpapp/404page.html')
 
@login_required
def cfo_manage_learner_view(request):
    try:    
        if str(request.session['utype']) == 'cfo':
            users = LXPModel.Course.objects.raw("SELECT social_auth_usersocialauth.id,  social_auth_usersocialauth.provider,  social_auth_usersocialauth.uid,  auth_user.first_name,  auth_user.last_name,  CASE WHEN social_auth_usersocialauth.utype = 1 THEN 'Trainer' WHEN social_auth_usersocialauth.utype = 2 THEN 'learner' WHEN social_auth_usersocialauth.utype = 3 THEN 'cto' WHEN social_auth_usersocialauth.utype = 4 THEN 'cfo' END AS utype,  CASE WHEN social_auth_usersocialauth.status = 0 THEN 'Inactive' ELSE 'Active' END AS status,  lxpapp_course.course_name,auth_user.id as user_id FROM  social_auth_usersocialauth  LEFT OUTER JOIN auth_user ON (social_auth_usersocialauth.user_id = auth_user.id)  LEFT OUTER JOIN lxpapp_usercourse ON (auth_user.id = lxpapp_usercourse.user_id)  LEFT OUTER JOIN lxpapp_course ON (lxpapp_usercourse.course_id = lxpapp_course.id) WHERE social_auth_usersocialauth.utype = 2 OR social_auth_usersocialauth.utype = 0 ")
            return render(request,'cfo/cfo_manage_learner.html',{'users':users})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def cfo_active_learner_view(request,userid,pk):
    try:    
        if str(request.session['utype']) == 'cfo':
            cursor = connection.cursor()
            cursor.execute("UPDATE social_auth_usersocialauth SET status = 1 WHERE id = " + str(pk))
            users = UserSocialAuth.objects.all()
            isfirstlogin =LXPModel.IsFirstLogIn.objects.all().filter(user_id = userid)
            if not isfirstlogin:
                isfirstlogin =LXPModel.IsFirstLogIn.objects.create(user_id = userid)
                isfirstlogin.save()
            return render(request,'cfo/cfo_manage_learner.html',{'users':users})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def cfo_inactive_learner_view(request,pk):
    try:    
        if str(request.session['utype']) == 'cfo':
            cursor = connection.cursor()
            cursor.execute("UPDATE social_auth_usersocialauth SET status = 0 WHERE id = " + str(pk))
            users = LXPModel.Course.objects.raw("SELECT social_auth_usersocialauth.id,  social_auth_usersocialauth.provider,  social_auth_usersocialauth.uid,  auth_user.first_name,  auth_user.last_name,  CASE WHEN social_auth_usersocialauth.utype = 1 THEN 'Trainer' WHEN social_auth_usersocialauth.utype = 2 THEN 'learner' WHEN social_auth_usersocialauth.utype = 3 THEN 'cto' WHEN social_auth_usersocialauth.utype = 4 THEN 'cfo' END AS utype,  CASE WHEN social_auth_usersocialauth.status = 0 THEN 'Inactive' ELSE 'Active' END AS status,  lxpapp_course.course_name,auth_user.id as user_id FROM  social_auth_usersocialauth  LEFT OUTER JOIN auth_user ON (social_auth_usersocialauth.user_id = auth_user.id)  LEFT OUTER JOIN lxpapp_usercourse ON (auth_user.id = lxpapp_usercourse.user_id)  LEFT OUTER JOIN lxpapp_course ON (lxpapp_usercourse.course_id = lxpapp_course.id) WHERE social_auth_usersocialauth.utype = 2 OR social_auth_usersocialauth.utype = 0 ")
            return render(request,'cfo/cfo_manage_learner.html',{'users':users})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def cfo_update_learner_course_view(request,pk):
    try:    
        if str(request.session['utype']) == 'cfo':
            if request.method=="POST":
                course=request.POST['newcourse']
                print(course)
                usercouse = LXPModel.UserCourse.objects.all().filter(user_id=pk)
                usercouse.delete()
                usercouse = LXPModel.UserCourse.objects.create(user_id=pk,course_id=course,remarks='')
                usercouse.save()
                users = LXPModel.Course.objects.raw("SELECT social_auth_usersocialauth.id,  social_auth_usersocialauth.provider,  social_auth_usersocialauth.uid,  auth_user.first_name,  auth_user.last_name,  CASE WHEN social_auth_usersocialauth.utype = 1 THEN 'Trainer' WHEN social_auth_usersocialauth.utype = 2 THEN 'learner' WHEN social_auth_usersocialauth.utype = 3 THEN 'cto' WHEN social_auth_usersocialauth.utype = 4 THEN 'cfo' END AS utype,  CASE WHEN social_auth_usersocialauth.status = 0 THEN 'Inactive' ELSE 'Active' END AS status,  lxpapp_course.course_name,auth_user.id as user_id FROM  social_auth_usersocialauth  LEFT OUTER JOIN auth_user ON (social_auth_usersocialauth.user_id = auth_user.id)  LEFT OUTER JOIN lxpapp_usercourse ON (auth_user.id = lxpapp_usercourse.user_id)  LEFT OUTER JOIN lxpapp_course ON (lxpapp_usercourse.course_id = lxpapp_course.id) WHERE social_auth_usersocialauth.utype = 2 OR social_auth_usersocialauth.utype = 0 ")
                return render(request,'cfo/cfo_manage_learner.html',{'users':users})
            course = LXPModel.Course.objects.all()
            return render(request,'cfo/cfo_update_learner_course.html',{'courses':course,'uid':pk})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def cfo_coursetype_view(request):
    try:
        if str(request.session['utype']) == 'cfo':
            return render(request,'cfo/coursetype/cfo_coursetype.html')
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def cfo_add_coursetype_view(request):
    try:
        if str(request.session['utype']) == 'cfo':
            if request.method=='POST':
                coursetypeForm=LXPFORM.CourseTypeForm(request.POST)
                if coursetypeForm.is_valid(): 
                    coursetypetext = coursetypeForm.cleaned_data["coursetype_name"]
                    coursetype = LXPModel.CourseType.objects.all().filter(coursetype_name__iexact = coursetypetext)
                    if coursetype:
                        messages.info(request, 'CourseType Name Already Exist')
                        coursetypeForm=LXPFORM.CourseTypeForm()
                        return render(request,'cfo/coursetype/cfo_add_coursetype.html',{'coursetypeForm':coursetypeForm})                  
                    else:
                        coursetypeForm.save()
                else:
                    print("form is invalid")
            coursetypeForm=LXPFORM.CourseTypeForm()
            return render(request,'cfo/coursetype/cfo_add_coursetype.html',{'coursetypeForm':coursetypeForm})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def cfo_update_coursetype_view(request,pk):
    try:
        if str(request.session['utype']) == 'cfo':
            coursetype = LXPModel.CourseType.objects.get(id=pk)
            coursetypeForm=LXPFORM.CourseTypeForm(request.POST,instance=coursetype)
            if request.method=='POST':
                if coursetypeForm.is_valid(): 
                    coursetypetext = coursetypeForm.cleaned_data["coursetype_name"]
                    coursetype = LXPModel.CourseType.objects.all().filter(coursetype_name__iexact = coursetypetext).exclude(id=pk)
                    if coursetype:
                        messages.info(request, 'CourseType Name Already Exist')
                        return render(request,'cfo/coursetype/cfo_update_coursetype.html',{'coursetypeForm':coursetypeForm})
                    else:
                        coursetypeForm.save()
                        coursetypes = LXPModel.CourseType.objects.all()
                        return render(request,'cfo/coursetype/cfo_view_coursetype.html',{'coursetypes':coursetypes})
            return render(request,'cfo/coursetype/cfo_update_coursetype.html',{'coursetypeForm':coursetypeForm,'sub':coursetype.coursetype_name})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def cfo_view_coursetype_view(request):
    try:
        if str(request.session['utype']) == 'cfo':
            coursetypes = LXPModel.CourseType.objects.all()
            return render(request,'cfo/coursetype/cfo_view_coursetype.html',{'coursetypes':coursetypes})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def cfo_delete_coursetype_view(request,pk):
    try:
        if str(request.session['utype']) == 'cfo':  
            coursetype=LXPModel.CourseType.objects.get(id=pk)
            coursetype.delete()
            return HttpResponseRedirect('/cfo/coursetype/cfo-view-coursetype')
        coursetypes = LXPModel.CourseType.objects.all()
        return render(request,'cfo/coursetype/cfo_view_coursetype.html',{'coursetypes':coursetypes})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def cfo_batch_view(request):
    try:
        if str(request.session['utype']) == 'cfo':
            return render(request,'cfo/batch/cfo_batch.html')
    except:
        return render(request,'lxpapp/404page.html')
from django.db import transaction
@login_required
def cfo_add_batch_view(request):
    try:
        if str(request.session['utype']) == 'cfo':
            if request.method=='POST':
                batchForm=LXPFORM.BatchForm(request.POST)
                if batchForm.is_valid(): 
                    batchtext = batchForm.cleaned_data["batch_name"]
                    batch = LXPModel.Batch.objects.all().filter(batch_name__iexact = batchtext)
                    if batch:
                        messages.info(request, 'Batch Name Already Exist')
                        batchForm=LXPFORM.BatchForm()
                        return render(request,'cfo/batch/cfo_add_batch.html',{'batchForm':batchForm})                  
                    else:
                        batchname = batchForm.cleaned_data["batch_name"]
                        coursetypeid = LXPModel.CourseType.objects.only('id').get(coursetype_name=batchForm.cleaned_data["coursetypeID"]).id
                        batchtable = LXPModel.Batch.objects.create(batch_name=batchname,stdate=batchForm.cleaned_data["stdate"],enddate=batchForm.cleaned_data["enddate"],coursetype_id=coursetypeid)
                        batchtable.save()
                        selectedlist = request.POST.getlist('listbox1')
                        for x in selectedlist:
                            trainerid = str(x)
                            batchtrainertable = LXPModel.BatchTrainer.objects.create(batch_id=batchtable.id,trainer_id=trainerid)
                            batchtrainertable.save()
                        import json
                        json_data = json.loads(request.POST.get('myvalue'))
                        for cx in json_data:
                            a=json_data[cx]['id']
                            b=json_data[cx]['fee']
                            batchlearnertable = LXPModel.Batchlearner.objects.create(batch_id=batchtable.id,learner_id=a,fee=b)
                            batchlearnertable.save()
                        selectedlist = request.POST.getlist('listbox3')
                        for x in selectedlist:
                            courseid = str(x)
                            batchcoursetable = LXPModel.BatchCourse.objects.create(batch_id=batchtable.id,course_id=courseid)
                            batchcoursetable.save()
                else:
                    print("form is invalid")
            batchForm=LXPFORM.BatchForm()
            trainers =  User.objects.raw('SELECT   auth_user.id,  auth_user.username,  auth_user.first_name,  auth_user.last_name,  auth_user.email FROM  social_auth_usersocialauth  INNER JOIN auth_user ON (social_auth_usersocialauth.user_id = auth_user.id) WHERE  social_auth_usersocialauth.utype = 1 AND  social_auth_usersocialauth.status = true')
            learners =  User.objects.raw('SELECT   auth_user.id,  auth_user.username,  auth_user.first_name,  auth_user.last_name,  auth_user.email FROM  social_auth_usersocialauth  INNER JOIN auth_user ON (social_auth_usersocialauth.user_id = auth_user.id) WHERE  social_auth_usersocialauth.utype = 2 AND  social_auth_usersocialauth.status = true ORDER BY auth_user.username')
            courses =  LXPModel.Course.objects.all()
            return render(request,'cfo/batch/cfo_add_batch.html',{'batchForm':batchForm,'trainers':trainers,'learners':learners,'courses':courses})
    except:
        transaction.set_rollback(True)
        return render(request,'lxpapp/404page.html')

@login_required
def cfo_update_batch_view(request,pk):
    #try:
        if str(request.session['utype']) == 'cfo':
            batch = LXPModel.Batch.objects.get(id=pk)
            batchForm=LXPFORM.BatchForm(request.POST,instance=batch)
            if request.method=='POST':
                if batchForm.is_valid(): 
                    batchtext = batchForm.cleaned_data["batch_name"]
                    batch = LXPModel.Batch.objects.all().filter(batch_name__iexact = batchtext).exclude(id=pk)
                    if batch:
                        messages.info(request, 'Batch Name Already Exist')
                        return render(request,'cfo/batch/cfo_update_batch.html',{'batchForm':batchForm})
                    else:
                        batchForm.save()
                        selectedlist = request.POST.getlist('listbox1')
                        det = LXPModel.BatchTrainer.objects.all().filter(batch_id=pk)
                        det.delete()
                        for x in selectedlist:
                            trainerid = str(x)
                            batchtrainertable = LXPModel.BatchTrainer.objects.create(batch_id=pk,trainer_id=trainerid)
                            batchtrainertable.save()
                        import json
                        det = LXPModel.Batchlearner.objects.all().filter(batch_id=pk)
                        det.delete()
                        json_data = json.loads(request.POST.get('myvalue'))
                        for cx in json_data:
                            a=json_data[cx]['id']
                            b=json_data[cx]['fee']
                            batchlearnertable = LXPModel.Batchlearner.objects.create(batch_id=pk,learner_id=a,fee=b)
                            batchlearnertable.save()
                        selectedlist = request.POST.getlist('listbox3')
                        det = LXPModel.BatchCourse.objects.all().filter(batch_id=pk)
                        det.delete()
                        for x in selectedlist:
                            courseid = str(x)
                            batchcoursetable = LXPModel.BatchCourse.objects.create(batch_id=pk,course_id=courseid)
                            batchcoursetable.save()
                        batchs = LXPModel.Batch.objects.all()
                        return render(request,'cfo/batch/cfo_view_batch.html',{'batchs':batchs})
            trainers =  list(User.objects.raw('SELECT   auth_user.id,  auth_user.username,  auth_user.first_name,  auth_user.last_name,  auth_user.email FROM  social_auth_usersocialauth  INNER JOIN auth_user ON (social_auth_usersocialauth.user_id = auth_user.id) WHERE  social_auth_usersocialauth.utype = 1 AND  social_auth_usersocialauth.status = true'))
            learners =  list(User.objects.raw('SELECT   auth_user.id,  auth_user.username,  auth_user.first_name,  auth_user.last_name,  auth_user.email FROM  social_auth_usersocialauth  INNER JOIN auth_user ON (social_auth_usersocialauth.user_id = auth_user.id) WHERE  social_auth_usersocialauth.utype = 2 AND  social_auth_usersocialauth.status = true ORDER BY auth_user.username'))
            batchtrainers =  list(User.objects.raw('SELECT DISTINCT   auth_user.id,  auth_user.first_name , auth_user.last_name ,  auth_user.email FROM  lxpapp_batchtrainer  INNER JOIN auth_user ON (lxpapp_batchtrainer.trainer_id = auth_user.id)   WHERE lxpapp_batchtrainer.batch_id = ' + str (pk)))
            btrainer = []
            for c in batchtrainers:
                btrnr={}
                btrnr["id"]=c.id
                btrnr["first_name"]=c.first_name
                btrnr["last_name"]=c.last_name
                btrnr["email"]=c.email
                btrainer.append(btrnr)
            batchlearners =  list(User.objects.raw('SELECT DISTINCT   auth_user.id,  auth_user.first_name , auth_user.last_name ,  auth_user.email,lxpapp_batchlearner.fee FROM  lxpapp_batchlearner  INNER JOIN auth_user ON (lxpapp_batchlearner.learner_id = auth_user.id)   WHERE lxpapp_batchlearner.batch_id = ' + str (pk)))
            blearner = []
            for c in batchlearners:
                btrnr={}
                btrnr["id"]=c.id
                btrnr["first_name"]=c.first_name
                btrnr["last_name"]=c.last_name
                btrnr["email"]=c.email
                btrnr["fee"]=c.fee
                blearner.append(btrnr)
            courses =  LXPModel.Course.objects.all()
            import json
            btrainer = json.dumps(btrainer)
            blearner = json.dumps(blearner)
            query = LXPModel.Batch.objects.get(id=pk)
            stdate = (query.stdate).strftime('%Y-%m-%d')
            enddate = (query.enddate).strftime('%Y-%m-%d')
            coursetype = query.coursetype
            dict={
            'batchForm':batchForm,
            'sub':batch.batch_name,
            'trainers':trainers,
            'learners':learners,
            'batchtrainers':batchtrainers,
            'batchlearners':batchlearners,
            'courses':courses,
            'btrainer':btrainer,
            'blearner':blearner,
            'stdate':stdate,
            'enddate':enddate,
            'coursetype':coursetype}
            
            return render(request,'cfo/batch/cfo_update_batch.html',context=dict)
    #except:
        return render(request,'lxpapp/404page.html')

@login_required
def cfo_view_batch_view(request):
    try:
        if str(request.session['utype']) == 'cfo':
            batchs = LXPModel.Batch.objects.all()
            return render(request,'cfo/batch/cfo_view_batch.html',{'batchs':batchs})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def cfo_view_batch_details_view(request,batchname,pk):
    try:
        if str(request.session['utype']) == 'cfo':
            batchs = LXPModel.Batch.objects.raw("SELECT lxpapp_batch.id,  GROUP_CONCAT(DISTINCT lxpapp_course.course_name) as course_name,  lxpapp_batch.stdate,  lxpapp_batch.enddate,  GROUP_CONCAT(DISTINCT trainer.first_name || ' ' || trainer.last_name) AS trainer_name,  GROUP_CONCAT(DISTINCT learner.first_name || ' ' || learner.last_name) AS learner_name FROM  lxpapp_batchcourse  LEFT OUTER JOIN lxpapp_batch ON (lxpapp_batchcourse.batch_id = lxpapp_batch.id)  LEFT OUTER JOIN lxpapp_batchlearner ON (lxpapp_batch.id = lxpapp_batchlearner.batch_id)  LEFT OUTER JOIN lxpapp_batchtrainer ON (lxpapp_batch.id = lxpapp_batchtrainer.batch_id)  LEFT OUTER JOIN auth_user trainer ON (lxpapp_batchtrainer.trainer_id = trainer.id)  LEFT OUTER JOIN lxpapp_course ON (lxpapp_batchcourse.course_id = lxpapp_course.id)  LEFT OUTER JOIN auth_user learner ON (lxpapp_batchlearner.learner_id = learner.id) WHERE lxpapp_batch.id = " + str(pk))
            return render(request,'cfo/batch/cfo_view_batch_details.html',{'batchs':batchs,'batchname':batchname})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def cfo_delete_batch_view(request,pk):
    try:
        if str(request.session['utype']) == 'cfo':  
            batch=LXPModel.Batch.objects.get(id=pk)
            batch.delete()
        batchs = LXPModel.Batch.objects.all()
        return render(request,'cfo/batch/cfo_view_batch.html',{'batchs':batchs})
    except:
        return render(request,'lxpapp/404page.html')
@login_required
def cfo_learnerfee_view(request):
    try:
        if str(request.session['utype']) == 'cfo':
            return render(request,'cfo/learnerfee/cfo_learnerfee.html')
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def cfo_add_learnerfee_view(request):
    try:
        if str(request.session['utype']) == 'cfo':
            if request.method=='POST':
                learnerfeeForm=LXPFORM.LearnerFeeForm(request.POST)
                if learnerfeeForm.is_valid(): 
                    learnerid = LXPModel.User.objects.only('id').get(username=learnerfeeForm.cleaned_data["learnerID"]).id
                    pdate = learnerfeeForm.cleaned_data["paiddate"]
                    pfee = learnerfeeForm.cleaned_data["fee"]
                    learnerfee = LXPModel.LearnerFee.objects.create(
                        learner_id=learnerid,
                        paiddate = pdate,
                        fee =pfee
                    )
                    learnerfee.save()
                else:
                    print("form is invalid")
            learnerfeeForm=LXPFORM.LearnerFeeForm()
            return render(request,'cfo/learnerfee/cfo_add_learnerfee.html',{'learnerfeeForm':learnerfeeForm})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def cfo_update_learnerfee_view(request,pk):
    try:
        if str(request.session['utype']) == 'cfo':
            learnerfee = LXPModel.LearnerFee.objects.get(id=pk)
            learnerfeeForm=LXPFORM.LearnerFeeForm(request.POST,instance=learnerfee)
            if request.method=='POST':
                if learnerfeeForm.is_valid(): 
                    learnerfeetext = learnerfeeForm.cleaned_data["learnerfee_name"]
                    learnerfee = LXPModel.LearnerFee.objects.all().filter(learnerfee_name__iexact = learnerfeetext).exclude(id=pk)
                    if learnerfee:
                        messages.info(request, 'LearnerFee Name Already Exist')
                        return render(request,'cfo/learnerfee/cfo_update_learnerfee.html',{'learnerfeeForm':learnerfeeForm})
                    else:
                        learnerfeeForm.save()
                        learnerfees = LXPModel.LearnerFee.objects.all()
                        return render(request,'cfo/learnerfee/cfo_view_learnerfee.html',{'learnerfees':learnerfees})
            return render(request,'cfo/learnerfee/cfo_update_learnerfee.html',{'learnerfeeForm':learnerfeeForm,'sub':learnerfee.learnerfee_name})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def cfo_view_learnerfee_view(request):
    try:
        if str(request.session['utype']) == 'cfo':
            learnerfees = LXPModel.LearnerFee.objects.all()
            return render(request,'cfo/learnerfee/cfo_view_learnerfee.html',{'learnerfees':learnerfees})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def cfo_delete_learnerfee_view(request,pk):
    try:
        if str(request.session['utype']) == 'cfo':  
            learnerfee=LXPModel.LearnerFee.objects.get(id=pk)
            learnerfee.delete()
            return HttpResponseRedirect('/cfo/learnerfee/cfo-view-learnerfee')
        learnerfees = LXPModel.LearnerFee.objects.all()
        return render(request,'cfo/learnerfee/cfo_view_learnerfee.html',{'learnerfees':learnerfees})
    except:
        return render(request,'lxpapp/404page.html')
