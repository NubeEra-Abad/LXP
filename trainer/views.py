from django.shortcuts import render,redirect
from django.contrib import messages
from ilmsapp import models as iLMSModel
from ilmsapp import forms as ILMSFORM
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib.auth.models import User
from django.db.models import Sum,Count
from youtubemanager import PlaylistManager
from django.http import HttpResponse
from django.template import loader
import os
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from urllib.parse import parse_qs, urlparse
import googleapiclient.discovery
scopes = ["https://www.googleapis.com/auth/youtube.readonly"]
from social_django.models import UserSocialAuth
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

@login_required
def trainer_exam_view(request):
    #try:
        if str(request.session['utype']) == 'trainer':
            return render(request,'trainer/exam/trainer_exam.html')
    #except:
        return render(request,'ilmsapp/404page.html')


@login_required
def trainer_add_exam_view(request):
    #try:
        if str(request.session['utype']) == 'trainer':
            if request.method=='POST':
                examForm=ILMSFORM.ExamForm(request.POST)
                if examForm.is_valid(): 
                    examtext = examForm.cleaned_data["exam_name"]
                    exam = iLMSModel.Exam.objects.all().filter(exam_name__iexact = examtext)
                    if exam:
                        messages.info(request, 'Exam Name Already Exist')
                        examForm=ILMSFORM.ExamForm()
                        return render(request,'trainer/exam/trainer_add_exam.html',{'examForm':examForm})                  
                    else:
                        course=iLMSModel.Course.objects.get(id=request.POST.get('courseID'))
                        exam = iLMSModel.Exam.objects.create(course_id = course.id,exam_name = examtext,questiontpye = request.POST.get('questiontpye'))
                        exam.save()
                else:
                    print("form is invalid")
            examForm=ILMSFORM.ExamForm()
            return render(request,'trainer/exam/trainer_add_exam.html',{'examForm':examForm})
    #except:
        return render(request,'ilmsapp/404page.html')

@login_required
def trainer_update_exam_view(request,pk):
    #try:
        if str(request.session['utype']) == 'trainer':
            exam = iLMSModel.Exam.objects.get(id=pk)
            examForm=ILMSFORM.ExamForm(request.POST,instance=exam)
            if request.method=='POST':
                if examForm.is_valid(): 
                    examtext = examForm.cleaned_data["exam_name"]
                    exam = iLMSModel.Exam.objects.all().filter(exam_name__iexact = examtext).exclude(id=pk)
                    if exam:
                        messages.info(request, 'Exam Name Already Exist')
                        return render(request,'trainer/exam/trainer_update_exam.html',{'examForm':examForm})
                    else:
                        examForm.save()
                        exams = iLMSModel.Exam.objects.all()
                        return render(request,'trainer/exam/trainer_view_exam.html',{'exams':exams})
            return render(request,'trainer/exam/trainer_update_exam.html',{'examForm':examForm,'ex':exam.exam_name,'sub':exam.questiontpye})
    #except:
        return render(request,'ilmsapp/404page.html')

@login_required
def trainer_view_exam_view(request):
    #try:
        if str(request.session['utype']) == 'trainer':
            exams = iLMSModel.Exam.objects.all().filter(course_id__in = iLMSModel.Course.objects.all())
            return render(request,'trainer/exam/trainer_view_exam.html',{'exams':exams})
    #except:
        return render(request,'ilmsapp/404page.html')

@login_required
def trainer_delete_exam_view(request,pk):
    #try:
        if str(request.session['utype']) == 'trainer':  
            exam=iLMSModel.Exam.objects.get(id=pk)
            exam.delete()
            return HttpResponseRedirect('/trainer/trainer-view-exam')
        exams = iLMSModel.Exam.objects.all()
        return render(request,'trainer/exam/trainer_view_exam.html',{'exams':exams})
    #except:
        return render(request,'ilmsapp/404page.html')
 
@login_required
def trainer_mcqquestion_view(request):
    #try:
        if str(request.session['utype']) == 'trainer':
            return render(request,'trainer/mcqquestion/trainer_mcqquestion.html')
    #except:
        return render(request,'ilmsapp/404page.html')

@login_required
def trainer_add_mcqquestion_view(request):
    #try:
        if str(request.session['utype']) == 'trainer':
            if request.method=='POST':
                mcqquestionForm=ILMSFORM.McqQuestionForm(request.POST)
                if mcqquestionForm.is_valid(): 
                    questiontext = mcqquestionForm.cleaned_data["question"]
                    mcqquestion = iLMSModel.McqQuestion.objects.all().filter(question__iexact = questiontext)
                    if mcqquestion:
                        messages.info(request, 'Mcq Question Name Already Exist')
                        mcqquestionForm=ILMSFORM.McqQuestionForm()
                        return render(request,'trainer/mcqquestion/trainer_add_mcqquestion.html',{'mcqquestionForm':mcqquestionForm})                  
                    else:
                        exam=iLMSModel.Exam.objects.get(id=request.POST.get('examID'))
                        mcqquestion = iLMSModel.McqQuestion.objects.create(exam_id = exam.id,question = questiontext,option1=request.POST.get('option1'),option2=request.POST.get('option2'),option3=request.POST.get('option3'),option4=request.POST.get('option4'),answer=request.POST.get('answer'),marks=request.POST.get('marks'))
                        mcqquestion.save()
                else:
                    print("form is invalid")
            mcqquestionForm=ILMSFORM.McqQuestionForm()
            return render(request,'trainer/mcqquestion/trainer_add_mcqquestion.html',{'mcqquestionForm':mcqquestionForm})
    #except:
        return render(request,'ilmsapp/404page.html')

@login_required
def trainer_update_mcqquestion_view(request,pk):
    #try:
        if str(request.session['utype']) == 'trainer':
            mcqquestion = iLMSModel.McqQuestion.objects.get(id=pk)
            mcqquestionForm=ILMSFORM.McqQuestionForm(request.POST,instance=mcqquestion)
            if request.method=='POST':
                if mcqquestionForm.is_valid(): 
                    mcqquestiontext = mcqquestionForm.cleaned_data["mcqquestion_name"]
                    mcqquestion = iLMSModel.McqQuestion.objects.all().filter(mcqquestion_name__iexact = mcqquestiontext).exclude(id=pk)
                    if mcqquestion:
                        messages.info(request, 'McqQuestion Name Already Exist')
                        return render(request,'trainer/mcqquestion/trainer_update_mcqquestion.html',{'mcqquestionForm':mcqquestionForm})
                    else:
                        mcqquestionForm.save()
                        mcqquestions = iLMSModel.McqQuestion.objects.all()
                        return render(request,'trainer/mcqquestion/trainer_view_mcqquestion.html',{'mcqquestions':mcqquestions})
            return render(request,'trainer/mcqquestion/trainer_update_mcqquestion.html',{'mcqquestionForm':mcqquestionForm,'ex':mcqquestion.mcqquestion_name,'sub':mcqquestion.questiontpye})
    #except:
        return render(request,'ilmsapp/404page.html')

@login_required
def trainer_view_mcqquestion_view(request):
    #try:
        if str(request.session['utype']) == 'trainer':
            mcqquestions = iLMSModel.McqQuestion.objects.all().filter(exam_id__in = iLMSModel.Exam.objects.all())
            return render(request,'trainer/mcqquestion/trainer_view_mcqquestion.html',{'mcqquestions':mcqquestions})
    #except:
        return render(request,'ilmsapp/404page.html')

@login_required
def trainer_delete_mcqquestion_view(request,pk):
    #try:
        if str(request.session['utype']) == 'trainer':  
            mcqquestion=iLMSModel.McqQuestion.objects.get(id=pk)
            mcqquestion.delete()
            return HttpResponseRedirect('/trainer/trainer-view-mcqquestion')
        mcqquestions = iLMSModel.McqQuestion.objects.all()
        return render(request,'trainer/mcqquestion/trainer_view_mcqquestion.html',{'mcqquestions':mcqquestions})
    #except:
        return render(request,'ilmsapp/404page.html')

@login_required
def trainer_shortquestion_view(request):
    #try:
        if str(request.session['utype']) == 'trainer':
            return render(request,'trainer/shortquestion/trainer_shortquestion.html')
    #except:
        return render(request,'ilmsapp/404page.html')

@login_required
def trainer_add_shortquestion_view(request):
    #try:
        if str(request.session['utype']) == 'trainer':
            if request.method=='POST':
                shortquestionForm=ILMSFORM.ShortQuestionForm(request.POST)
                if shortquestionForm.is_valid(): 
                    questiontext = shortquestionForm.cleaned_data["question"]
                    shortquestion = iLMSModel.ShortQuestion.objects.all().filter(question__iexact = questiontext)
                    if shortquestion:
                        messages.info(request, 'Short Question Already Exist')
                        shortquestionForm=ILMSFORM.ShortQuestionForm()
                        return render(request,'trainer/shortquestion/trainer_add_shortquestion.html',{'shortquestionForm':shortquestionForm})                  
                    else:
                        exam=iLMSModel.Exam.objects.get(id=request.POST.get('examID'))
                        shortquestion = iLMSModel.ShortQuestion.objects.create(exam_id = exam.id,question = questiontext,marks=request.POST.get('marks'))
                        shortquestion.save()
                else:
                    print("form is invalid")
            shortquestionForm=ILMSFORM.ShortQuestionForm()
            return render(request,'trainer/shortquestion/trainer_add_shortquestion.html',{'shortquestionForm':shortquestionForm})
    #except:
        return render(request,'ilmsapp/404page.html')

@login_required
def trainer_update_shortquestion_view(request,pk):
    #try:
        if str(request.session['utype']) == 'trainer':
            shortquestion = iLMSModel.ShortQuestion.objects.get(id=pk)
            shortquestionForm=ILMSFORM.ShortQuestionForm(request.POST,instance=shortquestion)
            if request.method=='POST':
                if shortquestionForm.is_valid(): 
                    shortquestiontext = shortquestionForm.cleaned_data["question"]
                    shortquestion = iLMSModel.ShortQuestion.objects.all().filter(question__iexact = shortquestiontext).exclude(id=pk)
                    if shortquestion:
                        messages.info(request, 'ShortQuestion Name Already Exist')
                        return render(request,'trainer/shortquestion/trainer_update_shortquestion.html',{'shortquestionForm':shortquestionForm})
                    else:
                        examid = iLMSModel.Exam.objects.all().filter(id=request.POST['examID'])
                        shortquestionForm.examID=examid
                        shortquestionForm.save()
                        shortquestions = iLMSModel.ShortQuestion.objects.all()
                        return render(request,'trainer/shortquestion/trainer_view_shortquestion.html',{'shortquestions':shortquestions})
            return render(request,'trainer/shortquestion/trainer_update_shortquestion.html',{'shortquestionForm':shortquestionForm,'ex':shortquestion.question})
    #except:
        return render(request,'ilmsapp/404page.html')

@login_required
def trainer_view_shortquestion_view(request):
    #try:
        if str(request.session['utype']) == 'trainer':
            shortquestions = iLMSModel.ShortQuestion.objects.all().filter(exam_id__in = iLMSModel.Exam.objects.all())
            return render(request,'trainer/shortquestion/trainer_view_shortquestion.html',{'shortquestions':shortquestions})
    #except:
        return render(request,'ilmsapp/404page.html')

@login_required
def trainer_delete_shortquestion_view(request,pk):
    #try:
        if str(request.session['utype']) == 'trainer':  
            shortquestion=iLMSModel.ShortQuestion.objects.get(id=pk)
            shortquestion.delete()
            return HttpResponseRedirect('/trainer/trainer-view-shortquestion')
        shortquestions = iLMSModel.ShortQuestion.objects.all()
        return render(request,'trainer/shortquestion/trainer_view_shortquestion.html',{'shortquestions':shortquestions})
    #except:
        return render(request,'ilmsapp/404page.html')

@login_required
def trainer_pending_short_exam_result_view(request):
    #try:
        if str(request.session['utype']) == 'trainer':
            pending = iLMSModel.ShortResult.objects.all().filter( learner_id__in = User.objects.all(),exam_id__in = iLMSModel.Exam.objects.all(),status = False)
            return render(request,'trainer/shortexam/trainer_pending_short_exam_reuslt.html',{'pending':pending})
    #except:
        return render(request,'ilmsapp/404page.html')

@login_required
def trainer_update_short_question_result_view(request,pk):
    #try:
        if str(request.session['utype']) == 'trainer':
            resultdetails = iLMSModel.ShortResultDetails.objects.all().filter( question_id__in = iLMSModel.ShortQuestion.objects.all(),shortresult_id = pk)
            return render(request,'trainer/shortexam/trainer_update_short_question_result.html',{'resultdetails':resultdetails})
    #except:
        return render(request,'ilmsapp/404page.html')

@login_required
def trainer_save_short_question_result_view(request,pk):
    #try:
        if str(request.session['utype']) == 'trainer':
            if request.method=="POST":
                feedback=request.POST['newfeedback']
                marks=request.POST['newmarks']
                rid=request.POST['newid']
                qid=request.POST['newqid']
                answer=request.POST['newanswer']
                mainid=request.POST['newmainid']
                resupdate = iLMSModel.ShortResultDetails.objects.all().filter(id=pk)
                resupdate.delete()
                resupdate = iLMSModel.ShortResultDetails.objects.create(id=pk,marks=marks,feedback=feedback,question_id=qid,answer=answer,shortresult_id=mainid)
                resupdate.save()
                
                totmarks=iLMSModel.ShortResultDetails.objects.all().filter(shortresult_id=mainid).aggregate(stars=Sum('marks'))['stars']
                maintbl=iLMSModel.ShortResult.objects.get(id=mainid)
                tot=iLMSModel.ShortResultDetails.objects.all().filter(shortresult_id=mainid).aggregate(stars=Count('marks'))['stars']
                totgiven=iLMSModel.ShortResultDetails.objects.all().filter(shortresult_id=mainid,marks__gt=0).aggregate(stars=Count('marks'))['stars']
                if tot == totgiven:
                    maintbl.status=True
                maintbl.marks = totmarks
                maintbl.save()
                if tot == totgiven:
                    resultdetails = iLMSModel.ShortResultDetails.objects.all().filter( question_id__in = iLMSModel.ShortQuestion.objects.all(),shortresult_id = pk)
                    return render(request,'trainer/shortexam/trainer_update_short_question_result.html',{'resultdetails':resultdetails})
                else:
                    resultdetails = iLMSModel.ShortResultDetails.objects.all().filter( question_id__in = iLMSModel.ShortQuestion.objects.all(),shortresult_id = mainid)
                    return render(request,'trainer/shortexam/trainer_update_short_question_result.html',{'resultdetails':resultdetails})
    #except:
        return render(request,'ilmsapp/404page.html') 

@login_required
def getcredentials(request):
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
    client_secrets_file = "GoogleCredV1.json"

    # Get credentials and create an API client
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes)
    flow.run_local_server()
    credentials = flow.credentials
    return credentials

@login_required
def trainer_sync_youtube_view(request):
    pllist = iLMSModel.Playlist.objects.all().exclude(playlist_id='').order_by('name')
    return render(request,'trainer/youtube/trainer_sync_youtube.html',{'pllist':pllist})

@login_required
def trainer_sync_youtube_start_view(request):
    if request.method=='POST':
        pm = PlaylistManager()
        credentials = pm.getCredentials()
        alllist = pm.initializePlaylist(credentials)
        plcount = 1
        maxcount = alllist.__len__()
        for PL_ID in alllist:
                PL_NAME = ''#iLMSModel.Playlist.objects.values('name').filter(playlist_id = PL_ID)
                print(str(plcount) + ' ' + PL_NAME)
                pm.getAllVideosForPlaylist(PL_ID,credentials,maxcount,plcount,PL_NAME)
                plcount = plcount + 1
                HttpResponse(loader.get_template('trainer/youtube/trainer_sync_youtube.html').render(
                    {
                        "plname": PL_NAME,
                        "maxcount": maxcount,
                        "plcount": plcount
                    }
                    ))
        dict={
        'total_learner':0,
        'total_trainer':0,
        'total_exam':0,
        'total_question':0,
        }
        return render(request,'trainer/trainer_dashboard.html',context=dict)
    pllist = iLMSModel.Playlist.objects.all().order_by('name')
    return render(request,'trainer/youtube/trainer_sync_youtube.html',{'pllist':pllist})    
######################################################################

@login_required
def trainer_sync_youtube_byselected_playlist_start_view(request):
    if request.method=='POST':  
        if 'dblist' in request.POST:
            pllist = iLMSModel.Playlist.objects.all().order_by('name')
            return render(request,'trainer/youtube/trainer_sync_youtube.html',{'pllist':pllist})
        elif 'cloudlist' in request.POST:
            pm = PlaylistManager()
            credentials = pm.getCredentials()
            pl =  pm.initializePlaylist(credentials)
            pllist = iLMSModel.Playlist.objects.all().order_by('name')
            return render(request,'trainer/youtube/trainer_sync_youtube.html',{'pllist':pllist})
        elif 'startselected' in request.POST:
            pm = PlaylistManager()
            selectedlist = request.POST.getlist('playlist[]')
            maxcount = selectedlist.__len__()
            plcount = 1
            credentials = getcredentials(request)
            for PL_NAME in selectedlist:
                print(str(plcount) + ' ' + PL_NAME)
                PL_ID = iLMSModel.Playlist.objects.all().filter(name = PL_NAME)
                _id = ''
                for z in PL_ID:
                    _id = z.playlist_id
                    break
                pm.getAllVideosForPlaylist(_id,credentials,maxcount,plcount,PL_NAME)
                plcount= plcount + 1
    dict={
    'total_learner':0,
    'total_trainer':0,
    'total_exam':0,
    'total_question':0,
    }
    return render(request,'trainer/trainer_dashboard.html',context=dict)

@login_required
def get_message_from_httperror(e):
    return e.error_details[0]['message']

def Import_excel(request):
    from tablib import Dataset
    if request.method == 'POST' :
        mcqquestion =iLMSModel.McqQuestionResource()
        dataset = Dataset()
        new_employee = request.FILES['myfile']
        data_import = dataset.load(new_employee.read())
        result = iLMSModel.McqQuestionResource.import_data(dataset,dry_run=True)
        if not result.has_errors():
            iLMSModel.McqQuestionResource.import_data(dataset,dry_run=False)        
    return render(request, 'Import_excel_db.html',{})

@login_required
def trainer_view_learner_video_view(request):
    #try:
        if str(request.session['utype']) == 'trainer':
            #learner = UserSocialAuth.objects.raw("SELECT social_auth_usersocialauth.id,social_auth_usersocialauth.provider,social_auth_usersocialauth.uid,auth_user.first_name,  auth_user.last_name,  CASE WHEN social_auth_usersocialauth.utype = 0 THEN 'Learner' ELSE 'Trainer' END AS utype,CASE WHEN social_auth_usersocialauth.status = 0 THEN 'Inactive' ELSE 'Active' END AS status,IFNULL(course_name,'') AS course_name,auth_user.id as user_id FROM social_auth_usersocialauth  LEFT OUTER JOIN auth_user ON (social_auth_usersocialauth.user_id = auth_user.id)  WHERE social_auth_usersocialauth.utype = 0 AND social_auth_usersocialauth.status = 1 Order by social_auth_usersocialauth.uid")
            learner = UserSocialAuth.objects.raw('SELECT social_auth_usersocialauth.id, social_auth_usersocialauth.user_id, auth_user.first_name, auth_user.last_name, GROUP_CONCAT(ilmsapp_course.course_name)  as course_name FROM social_auth_usersocialauth LEFT OUTER JOIN auth_user ON (social_auth_usersocialauth.user_id = auth_user.id) LEFT OUTER JOIN ilmsapp_usercourse ON (auth_user.id = ilmsapp_usercourse.user_id) LEFT OUTER JOIN ilmsapp_course ON (ilmsapp_usercourse.course_id = ilmsapp_course.id) WHERE (social_auth_usersocialauth.utype = 0 OR social_auth_usersocialauth.utype = 2) AND social_auth_usersocialauth.status = 1 GROUP BY social_auth_usersocialauth.id, social_auth_usersocialauth.user_id,  auth_user.first_name, auth_user.last_name ')
            return render(request,'trainer/learnervideo/trainer_view_learner_video.html',{'learner':learner})
    #except:
        return render(request,'ilmsapp/404page.html')

@login_required
def trainer_learner_video_Course_view(request,user_id,userfirstname,userlastname):
#    try:    
        if str(request.session['utype']) == 'trainer':
            videos1 = iLMSModel.UserCourse.objects.all().filter(course_id__in = iLMSModel.Course.objects.all(),user_id=user_id)  
            return render(request,'trainer/learnervideo/trainer_learner_video_course.html',{'videos':videos1,'userfirstname':userfirstname,'userlastname':userlastname})
 #   except:
        return render(request,'ilmsapp/404page.html')

@login_required
def trainer_learner_video_Course_subject_view(request,course_id):
#    try:    
        if str(request.session['utype']) == 'trainer':
            coursename = iLMSModel.Course.objects.only('course_name').get(id=course_id).course_name
            subject = iLMSModel.CourseDetails.objects.all().filter(subject_id__in = iLMSModel.Playlist.objects.all(),course_id=str(course_id))
            subject = iLMSModel.Playlist.objects.raw('SELECT y.id,  y.name  , (SELECT COUNT (PLI.id) FROM ilmsapp_playlistitem PLI LEFT OUTER JOIN ilmsapp_video PLIV ON (PLI.video_id = PLIV.id)  WHERE  PLI.playlist_id = y.id) as Vtotal  , (SELECT COUNT(WC.id) FROM  ilmsapp_videowatched WC  LEFT OUTER JOIN ilmsapp_video WCV ON (WC.video_id = WCV.id)  LEFT OUTER JOIN ilmsapp_playlistitem WCPL ON (WCV.id = WCPL.video_id) WHERE WCPL.playlist_id = y.id) as VWatched FROM  ilmsapp_coursedetails  LEFT OUTER JOIN ilmsapp_playlist y ON (ilmsapp_coursedetails.subject_id = y.id)  WHERE ilmsapp_coursedetails.course_id = ' + str(course_id))
            tc = iLMSModel.Video.objects.raw('SELECT 1 as id, count(ilmsapp_video.id) AS FIELD_1 FROM  ilmsapp_coursedetails  LEFT OUTER JOIN ilmsapp_playlist ON (ilmsapp_coursedetails.subject_id = ilmsapp_playlist.id)  LEFT OUTER JOIN ilmsapp_playlistitem ON (ilmsapp_playlist.id = ilmsapp_playlistitem.playlist_id)  LEFT OUTER JOIN ilmsapp_video ON (ilmsapp_playlistitem.video_id = ilmsapp_video.id) WHERE   ilmsapp_coursedetails.course_id = ' + str(course_id))
            wc = iLMSModel.VideoWatched.objects.raw('SELECT 1 as id, count(ilmsapp_videowatched.id) AS FIELD_1 FROM  ilmsapp_videowatched  LEFT OUTER JOIN ilmsapp_video ON (ilmsapp_videowatched.video_id = ilmsapp_video.id)  LEFT OUTER  JOIN ilmsapp_playlistitem ON (ilmsapp_video.id = ilmsapp_playlistitem.video_id)  LEFT OUTER  JOIN ilmsapp_playlist ON (ilmsapp_playlistitem.playlist_id = ilmsapp_playlist.id)  LEFT OUTER  JOIN ilmsapp_coursedetails ON (ilmsapp_playlist.id = ilmsapp_coursedetails.subject_id) WHERE   ilmsapp_coursedetails.course_id = ' + str(course_id))
            per = 0
            for x in tc:
                tc = x.FIELD_1

            for x in wc:
                wc = x.FIELD_1
            try:
                per = (100*wc)/tc
            except:
                per =0
            dif = tc-wc

            return render(request,'trainer/learnervideo/trainer_learner_video_course_subject.html',{'subject':subject,'coursename':coursename,'course_id':course_id,'dif':dif,'per':per,'wc':wc,'tc':tc})
 #   except:
        return render(request,'ilmsapp/404page.html')
 
@login_required
def trainer_learner_video_list_view(request,subject_id,course_id):
    try:     
        if str(request.session['utype']) == 'trainer':
            subjectname = iLMSModel.Playlist.objects.only('name').get(id=subject_id).name
            coursename = iLMSModel.Course.objects.only('course_name').get(id=course_id).course_name
            list = iLMSModel.PlaylistItem.objects.all().filter(video_id__in = iLMSModel.Video.objects.all(),playlist_id=str(subject_id))  
            return render(request,'trainer/learnervideo/trainer_learner_video_list.html',{'list':list,'subjectname':subjectname,'subject_id':subject_id,'course_id':course_id,'coursename':coursename})
    except:
        return render(request,'ilmsapp/404page.html')
 
@login_required
def trainer_learner_show_video_view(request,subject_id,course_id,video_id):
    #try:    
        if str(request.session['utype']) == 'trainer':
            subjectname = iLMSModel.Playlist.objects.only('name').get(id=subject_id).name
            coursename = iLMSModel.Course.objects.only('course_name').get(id=course_id).course_name
            Videos=iLMSModel.Video.objects.all().filter(id=video_id)
            topicname =''
            url=''
            for x in Videos:
                topicname =x.name
                url = "https://www.youtube.com/embed/" + x.video_id
            return render(request,'trainer/learnervideo/trainer_learner_show_video.html',{'topicname':topicname,'url':url,'subjectname':subjectname,'subject_id':subject_id,'course_id':course_id,'coursename':coursename})
    #except:
        return render(request,'ilmsapp/404page.html')

@login_required
def trainer_material_view(request):
    try:
        if str(request.session['utype']) == 'trainer':
            return render(request,'trainer/material/trainer_material.html')
    except:
        return render(request,'ilmsapp/404page.html')

@login_required
def trainer_material_chapters_view(request):
    subject = request.GET.get('subject')
    chapters = iLMSModel.Video.objects.all().filter(id__in = iLMSModel.PlaylistItem.objects.all().filter( playlist_id=subject))
    context = {'chapters': chapters}
    return render(request, 'trainer/material/trainer_material_chapters.html', context)

@login_required
def trainer_add_material_view(request):
    #try:
        if str(request.session['utype']) == 'trainer':
            if request.method=='POST':
                subject = request.POST.getlist('subject')
                chapter = request.POST.getlist('chapters')
                mtype = request.POST.getlist('mtype')
                urlvalue = request.POST.get('urlvalue')
                description = request.POST.get('description')
                for x in subject:
                    subject = x
                for x in chapter:
                    chapter = x
                for x in mtype:
                    mtype = x
                if subject == 'Choose your Subject':
                    messages.info(request, 'Please Select Subject')
                if chapter == 'Choose your Chapter':
                    messages.info(request, 'Please Select Chapter')
                if mtype == 'Choose your Type':
                    messages.info(request, 'Please Select Material Type')
                if urlvalue == '':
                    messages.info(request, 'Please Enter Details')
                if description is None:
                    messages.info(request, 'Please Enter Description')
 
                if description is not None and subject !='Choose your Subject' and  chapter !='Choose your Chapter' and mtype !='Choose your Type' and urlvalue !='':
                    material = iLMSModel.Material.objects.create(
                        subject_id = subject,
                        chapter_id = chapter,
                        mtype = mtype,
                        urlvalue=urlvalue,
                        description=description
                    ).save()

            subjects = iLMSModel.Playlist.objects.all()
            context = {'subjects': subjects}
            return render(request,'trainer/material/trainer_add_material.html',context)
    #except:
        return render(request,'ilmsapp/404page.html')

@login_required
def trainer_update_material_view(request,pk):
    #try:
        if str(request.session['utype']) == 'trainer':
            material = iLMSModel.Video.objects.get(id=pk)
            materialForm=ILMSFORM.MaterialForm(request.POST,instance=material)
            if request.method=='POST':
                if materialForm.is_valid(): 
                    materialtext = materialForm.cleaned_data["name"]
                    subjecttext = materialForm.cleaned_data["subjectID"]
                    
                    material = iLMSModel.Video.objects.all().filter(name__iexact = materialtext).exclude(id=pk)
                    if material:
                        messages.info(request, 'Material Name Already Exist')
                        return render(request,'trainer/material/trainer_update_material.html',{'materialForm':materialForm})
                    else:
                        subject = iLMSModel.Playlist.objects.get(name=subjecttext)
                        
                        material = iLMSModel.Video.objects.get(id=pk)
                        oldsubject =iLMSModel.PlaylistItem.objects.get(video_id=pk)
                        material.name = materialtext
                        material.save()
                        PLItems = iLMSModel.PlaylistItem.objects.get(video_id=pk,playlist_id = oldsubject.playlist_id)
                        PLItems.playlist_id =subject.id
                        PLItems.save()
                        c_list = iLMSModel.Video.objects.raw('SELECT   ilmsapp_video.id,  ilmsapp_video.name,  ilmsapp_video.video_id,  ilmsapp_playlist.name AS plname FROM  ilmsapp_playlistitem  INNER JOIN ilmsapp_video ON (ilmsapp_playlistitem.video_id = ilmsapp_video.id)  INNER JOIN ilmsapp_playlist ON (ilmsapp_playlistitem.playlist_id = ilmsapp_playlist.id)')
                        return render(request,'trainer/material/trainer_view_material.html',{'materials':c_list})
            return render(request,'trainer/material/trainer_update_material.html',{'materialForm':materialForm,'sub':material.name})
    #except:
        return render(request,'ilmsapp/404page.html')

@login_required
def trainer_view_material_view(request):
    #try:
        if str(request.session['utype']) == 'trainer':
            c_list = iLMSModel.Video.objects.raw('SELECT   ilmsapp_video.id,  ilmsapp_video.name,  ilmsapp_video.video_id,  ilmsapp_playlist.name AS plname FROM  ilmsapp_playlistitem  INNER JOIN ilmsapp_video ON (ilmsapp_playlistitem.video_id = ilmsapp_video.id)  INNER JOIN ilmsapp_playlist ON (ilmsapp_playlistitem.playlist_id = ilmsapp_playlist.id)')
            materials = iLMSModel.Material.objects.all().filter(subject_id__in=iLMSModel.Playlist.objects.all())
            return render(request,'trainer/material/trainer_view_material.html',{'materials':materials})
    #except:
        return render(request,'ilmsapp/404page.html')

@login_required
def trainer_delete_material_view(request,pk):
    try:
        if str(request.session['utype']) == 'trainer':  
            material=iLMSModel.Material.objects.get(id=pk)
            material.delete()
            materials = iLMSModel.Material.objects.all().filter(subject_id__in=iLMSModel.Playlist.objects.all())
            return render(request,'trainer/material/trainer_view_material.html',{'materials':materials})
    except:
        return render(request,'ilmsapp/404page.html')

@login_required
def trainer_show_material_view(request,subjectname,chaptername,materialtype,pk):
    #try:
        if str(request.session['utype']) == 'trainer':
            details= iLMSModel.Material.objects.all().filter(id=pk)
            if materialtype == '1':
                return render(request,'trainer/material/trainer_material_htmlshow.html',{'details':details})
            if materialtype == '2':
                return render(request,'trainer/material/trainer_material_urlshow.html',{'details':details})
            if materialtype == '3':
                return render(request,'trainer/material/trainer_material_pdfshow.html',{'details':details})
    #except:
        return render(request,'ilmsapp/404page.html')

@login_required
def trainer_upload_file_view(request):
    subjects = iLMSModel.Playlist.objects.all()
    context = {'subjects': subjects}
    return render(request,'trainer/uploadpdf/trainer_upload_file.html',context)

from django.conf import settings
from datetime import datetime
import boto3, botocore
ALLOWED_EXTENSIONS = set(['txt', 'zip', 'markdown', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
def allowed_file(name):
    return "." in name and name.split(".")[1].lower() in ALLOWED_EXTENSIONS
# Connect to the s3 service
s3 = boto3.client(
    "s3",
    aws_access_key_id=settings.AWS_ACCESS_KEY,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
)
#upload file to s3 w/ acl as public

@login_required  
def upload_file_to_s3(request,file, bucket_name, acl="public-read"):
    try:
        filename = datetime.now().strftime("%Y%m%d%H%M%S.pdf")
        print("intered in function")
        s3.upload_fileobj(
            file,
            bucket_name,
            filename,
            ExtraArgs={
                "ACL": acl,
                "ContentType": file.content_type
            }
        )
    except Exception as e:
        print("Something Unexpected Happened: ", e)
        return e
    # returns the webling to file upload to view
    url=settings.AWS_DOMAIN + '' + filename
    subject = request.POST.getlist('subject')
    chapter = request.POST.getlist('chapters')
    mtype = '3'
    description = 'file uploaded'
    for x in subject:
        subject = x
    for x in chapter:
        chapter = x
    for x in mtype:
        mtype = x
    if subject == 'Choose your Subject':
        messages.info(request, 'Please Select Subject')
    if chapter == 'Choose your Chapter':
        messages.info(request, 'Please Select Chapter')
    if mtype == 'Choose your Type':
        messages.info(request, 'Please Select Material Type')
    if description is None:
        messages.info(request, 'Please Enter Description')

    if description is not None and subject !='Choose your Subject' and  chapter !='Choose your Chapter' and mtype !='Choose your Type' :
        material = iLMSModel.Material.objects.create(
            subject_id = subject,
            chapter_id = chapter,
            mtype = mtype,
            urlvalue=url,
            description=description
        ).save()
    
    subjects = iLMSModel.Playlist.objects.all()
    context = {'subjects': subjects}
    return render(request,'trainer/uploadpdf/trainer_upload_file.html',context)

@login_required
def trainer_start_upload_file_view(request):
    if request.method=="POST":
        file=request.FILES["select_file"]
        if file == "":
            return "Please return to previous page and select a file"
        if file:
            output = upload_file_to_s3(request, file, settings.AWS_BUCKET_NAME)
            return output
        else:
            return redirect("/")