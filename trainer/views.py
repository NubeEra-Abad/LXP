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

def trainer_exam_view(request):
    #try:
        if str(request.session['utype']) == 'trainer':
            return render(request,'trainer/exam/trainer_exam.html')
    #except:
        return render(request,'ilmsapp/404page.html')

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

def trainer_view_exam_view(request):
    #try:
        if str(request.session['utype']) == 'trainer':
            exams = iLMSModel.Exam.objects.all().filter(course_id__in = iLMSModel.Course.objects.all())
            return render(request,'trainer/exam/trainer_view_exam.html',{'exams':exams})
    #except:
        return render(request,'ilmsapp/404page.html')

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
 
def trainer_mcqquestion_view(request):
    #try:
        if str(request.session['utype']) == 'trainer':
            return render(request,'trainer/mcqquestion/trainer_mcqquestion.html')
    #except:
        return render(request,'ilmsapp/404page.html')

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

def trainer_view_mcqquestion_view(request):
    #try:
        if str(request.session['utype']) == 'trainer':
            mcqquestions = iLMSModel.McqQuestion.objects.all().filter(exam_id__in = iLMSModel.Exam.objects.all())
            return render(request,'trainer/mcqquestion/trainer_view_mcqquestion.html',{'mcqquestions':mcqquestions})
    #except:
        return render(request,'ilmsapp/404page.html')

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

def trainer_shortquestion_view(request):
    #try:
        if str(request.session['utype']) == 'trainer':
            return render(request,'trainer/shortquestion/trainer_shortquestion.html')
    #except:
        return render(request,'ilmsapp/404page.html')

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

def trainer_view_shortquestion_view(request):
    #try:
        if str(request.session['utype']) == 'trainer':
            shortquestions = iLMSModel.ShortQuestion.objects.all().filter(exam_id__in = iLMSModel.Exam.objects.all())
            return render(request,'trainer/shortquestion/trainer_view_shortquestion.html',{'shortquestions':shortquestions})
    #except:
        return render(request,'ilmsapp/404page.html')

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

def trainer_pending_short_exam_result_view(request):
    #try:
        if str(request.session['utype']) == 'trainer':
            pending = iLMSModel.ShortResult.objects.all().filter( learner_id__in = User.objects.all(),exam_id__in = iLMSModel.Exam.objects.all(),status = False)
            return render(request,'trainer/shortexam/trainer_pending_short_exam_reuslt.html',{'pending':pending})
    #except:
        return render(request,'ilmsapp/404page.html')

def trainer_update_short_question_result_view(request,pk):
    #try:
        if str(request.session['utype']) == 'trainer':
            resultdetails = iLMSModel.ShortResultDetails.objects.all().filter( question_id__in = iLMSModel.ShortQuestion.objects.all(),shortresult_id = pk)
            return render(request,'trainer/shortexam/trainer_update_short_question_result.html',{'resultdetails':resultdetails})
    #except:
        return render(request,'ilmsapp/404page.html')

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