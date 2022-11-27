from django.shortcuts import render,redirect,reverse
import os
#from social_django.models import UserSocialAuth as a

from urllib.parse import parse_qs, urlparse
from . import forms,models
from django.db.models import Sum
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required,user_passes_test
from django.conf import settings
from datetime import date, timedelta
from django.db.models import Q
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.db import connection
from django.contrib.auth.decorators import login_required
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import googleapiclient.discovery
scopes = ["https://www.googleapis.com/auth/youtube.readonly"]

def login(request):
    return render(request, 'ilmsapp/index.html')

@login_required
def home(request):
    
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')  
    return render(request,'ilmsapp/404page.html')

def afterlogin_view(request):
    das = models.Course.objects.raw("SELECT * FROM social_auth_usersocialauth where user_id = " + str(request.user.id))
    print(das.__len__)
    if not das:
        request.session['utype'] = 'admin'
        return redirect('admin-dashboard')
    elif das:
        for xx in das:
            if xx.utype == 1:
                if xx.status:
                    request.session['utype'] = 'trainer'
                    return redirect('trainer/trainer-dashboard')
                else:
                    return render(request,'trainer/trainer_wait_for_approval.html')
            elif not xx.utype == 2:
                if xx.status:
                    request.session['utype'] = 'learner'
                    return render(request,'learner/learner_dashboard.html')
                else:
                    send_mail('New User Login / Pending User Login Notification', 'Please check following user is registered or relogin before approval\n' + 'E-mail : ' + str (request.user.email) + '\nFirst Name : ' + str (request.user.first_name) + '\nLast Name : '+ str (request.user.last_name), 'info@nubeera.com', ['info@nubeera.com'])
                    return render(request,'learner/learner_wait_for_approval.html')
            elif not xx.utype == 3:
                if xx.status:
                    request.session['utype'] = 'cto'
                    return render(request,'cto/cto_dashboard.html')
                else:
                    send_mail('New User Login / Pending User Login Notification', 'Please check following user is registered or relogin before approval\n' + 'E-mail : ' + str (request.user.email) + '\nFirst Name : ' + str (request.user.first_name) + '\nLast Name : '+ str (request.user.last_name), 'info@nubeera.com', ['info@nubeera.com'])
                    return render(request,'cto/cto_wait_for_approval.html')
            elif not xx.utype == 4:
                if xx.status:
                    request.session['utype'] = 'CFO'
                    return render(request,'CFO/CFO_dashboard.html')
                else:
                    send_mail('New User Login / Pending User Login Notification', 'Please check following user is registered or relogin before approval\n' + 'E-mail : ' + str (request.user.email) + '\nFirst Name : ' + str (request.user.first_name) + '\nLast Name : '+ str (request.user.last_name), 'info@nubeera.com', ['info@nubeera.com'])
                    return render(request,'CFO/CFO_wait_for_approval.html')

def adminclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return HttpResponseRedirect('adminlogin')

def admin_dashboard_view(request):
    #try:
        if str(request.session['utype']) == 'admin':
            dict={
            'total_learner':0,
            'total_trainer':0,
            'total_exam':0,
            'total_question':0,
            }
            return render(request,'ilmsapp/admin_dashboard.html',context=dict)
   # except:
        return render(request,'ilmsapp/404page.html')

def syncyoutube_view(request):
    pllist = models.PlayList.objects.all()
    return render(request,'ilmsapp/syncyoutube.html',{'pllist':pllist})
def syncyoutube_start_view(request):
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "GoogleCredV1.json"
    xxx = 0
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes)
    flow.run_local_server()
    credentials = flow.credentials
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)
    
    pllist = models.PlayList.objects.all()
    for plyLstitem in pllist:
        url = 'https://www.youtube.com/playlist?list=' + str(plyLstitem.playlist_id)
        query = parse_qs(urlparse(url).query, keep_blank_values=True)
        playlist_id = query["list"][0]
        youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)
        request1 = youtube.playlistItems().list(
            part = "snippet",
            playlistId = playlist_id,
            maxResults = 5000
        )
        response1 = request1.execute()
        playlist_items = []
        playlistname = plyLstitem.playlist_name
        while request1 is not None:
            response1 = request1.execute()
            playlist_items += response1["items"]
            request1 = youtube.playlistItems().list_next(request1, response1)
        for t in playlist_items:
            xxx += 1
            currenturl = 'https://www.youtube.com/embed/' + t["snippet"]["resourceId"]["videoId"]
            tochk= models.VideoLinks.objects.all().filter(Url=currenturl)
            if tochk:
                a=''
            else:
                y = models.VideoLinks.objects.create(SrNo=xxx,TopicName=t["snippet"]['title'],Url='https://www.youtube.com/embed/' + t["snippet"]["resourceId"]["videoId"],CourseName=playlistname,TopicCovered=0)
                y.save()
    print ('all done')
    dict={
    'total_learner':0,
    'total_trainer':0,
    'total_exam':0,
    'total_question':0,
    }
    return render(request,'ilmsapp/admin_dashboard.html',context=dict)

def aboutus_view(request):
    return render(request,'ilmsapp/aboutus.html')

def contactus_view(request):
    try:    
        if str(request.session['utype']) == 'admin':
            sub = forms.ContactusForm()
            if request.method == 'POST':
                sub = forms.ContactusForm(request.POST)
                if sub.is_valid():
                    email = sub.cleaned_data['Email']
                    name=sub.cleaned_data['Name']
                    message = sub.cleaned_data['Message']
                    send_mail(str(name)+' || '+str(email),message,settings.EMAIL_HOST_USER, settings.EMAIL_RECEIVING_USER, fail_silently = False)
                    return render(request, 'ilmsapp/contactussuccess.html')
            return render(request, 'ilmsapp/contactus.html', {'form':sub})
    except:
        return render(request,'ilmsapp/404page.html')
def admin_view_user_view(request):
    #try:    
        if str(request.session['utype']) == 'admin':
            users = models.Course.objects.raw("SELECT social_auth_usersocialauth.id,  social_auth_usersocialauth.provider,  social_auth_usersocialauth.uid,  auth_user.first_name,  auth_user.last_name,  CASE WHEN social_auth_usersocialauth.utype = 1 THEN 'Trainer' WHEN social_auth_usersocialauth.utype = 2 THEN 'cto' WHEN social_auth_usersocialauth.utype = 3 THEN 'learner' WHEN social_auth_usersocialauth.utype = 4 THEN 'CFO' END AS utype,  CASE WHEN social_auth_usersocialauth.status = 0 THEN 'Inactive' ELSE 'Active' END AS status,  ilmsapp_course.course_name,auth_user.id as user_id FROM  social_auth_usersocialauth  LEFT OUTER JOIN auth_user ON (social_auth_usersocialauth.user_id = auth_user.id)  LEFT OUTER JOIN ilmsapp_usercourse ON (auth_user.id = ilmsapp_usercourse.user_id)  LEFT OUTER JOIN ilmsapp_course ON (ilmsapp_usercourse.course_id = ilmsapp_course.id)")
            return render(request,'ilmsapp/admin_view_user.html',{'users':users})
    #except:
        return render(request,'ilmsapp/404page.html')

def active_user_view(request,pk):
    try:    
        if str(request.session['utype']) == 'admin':
            cursor = connection.cursor()
            cursor.execute("UPDATE social_auth_usersocialauth SET status = 1 WHERE id = " + str(pk))
            users = models.Course.objects.raw("SELECT * FROM social_auth_usersocialauth where user_id = " + str(request.user.id))
            return HttpResponseRedirect('/admin-view-user',{'users':users})
    except:
        return render(request,'ilmsapp/404page.html')

def inactive_user_view(request,pk):
    try:    
        if str(request.session['utype']) == 'admin':
            cursor = connection.cursor()
            cursor.execute("UPDATE social_auth_usersocialauth SET status = 0 WHERE id = " + str(pk))
            users = models.Course.objects.raw("SELECT * FROM social_auth_usersocialauth where user_id = " + str(request.user.id))
            return HttpResponseRedirect('/admin-view-user',{'users':users})
    except:
        return render(request,'ilmsapp/404page.html')
def admin_update_course_view(request,pk):
    #try:    
        if str(request.session['utype']) == 'admin':
            if request.method=="POST":
                course=request.POST['newcourse']
                print(course)
                usercouse = models.UserCourse.objects.all().filter(user_id=pk)
                usercouse.delete()
                usercouse = models.UserCourse.objects.create(user_id=pk,course_id=course,remarks='')
                usercouse.save()
                users = models.Course.objects.raw("SELECT * FROM social_auth_usersocialauth where user_id = " + str(request.user.id))
                return HttpResponseRedirect('/admin-view-user',{'users':users})
            course = models.Course.objects.all()
            return render(request,'ilmsapp/admin_update_course.html',{'courses':course,'uid':pk})
    #except:
        return render(request,'ilmsapp/404page.html')

def admin_mark_usertype_view(request,pk):
    #try:    
        if str(request.session['utype']) == 'admin':
            if request.method=="POST":
                newtype=request.POST['newtype']
                cursor = connection.cursor()
                cursor.execute("UPDATE social_auth_usersocialauth SET utype = " + str (newtype) + " WHERE id = " + str(pk))
                users = models.Course.objects.raw("SELECT * FROM social_auth_usersocialauth where user_id = " + str(request.user.id))
                return HttpResponseRedirect('/admin-view-user',{'users':users})
            return render(request,'ilmsapp/admin_mark_usertype.html',{'courses':'course','uid':pk})
    #except:
        return render(request,'ilmsapp/404page.html')
