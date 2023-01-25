from django.shortcuts import render,redirect
from django.contrib import messages
from lxpapp import models as LXPModel
from lxpapp import forms as LXPFORM
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib.auth.models import User
from django.db.models import Sum,Count,Q
from youtubemanager import PlaylistManager
from django.http import HttpResponse
from django.template import loader

import os
from pathlib import Path
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from urllib.parse import parse_qs, urlparse
import googleapiclient.discovery
scopes = ["https://www.googleapis.com/auth/youtube.readonly"]
from social_django.models import UserSocialAuth
from apiclient.discovery import build
from apiclient.errors import HttpError
from apiclient.http import MediaFileUpload
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import argparser, run_flow
from pytube import Playlist
import http.client as hc
import httplib2
import os
import random
import time
httplib2.RETRIES = 1
CLIENT_SECRETS_FILE = "GoogleCredV1.json"
MAX_RETRIES = 10
RETRIABLE_EXCEPTIONS = (httplib2.HttpLib2Error, IOError, hc.NotConnected,
                        hc.IncompleteRead, hc.ImproperConnectionState,
                        hc.CannotSendRequest, hc.CannotSendHeader,
                        hc.ResponseNotReady, hc.BadStatusLine)
RETRIABLE_STATUS_CODES = [500, 502, 503, 504]
YOUTUBE_UPLOAD_SCOPE = "https://www.googleapis.com/auth/youtube"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

MISSING_CLIENT_SECRETS_MESSAGE = """
   %s
""" % os.path.abspath(os.path.join(os.path.dirname(__file__),
                                   CLIENT_SECRETS_FILE))

VALID_PRIVACY_STATUSES = ("public", "private", "unlisted")

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
        return render(request,'lxpapp/404page.html')

@login_required
def trainer_exam_view(request):
    try:
        if str(request.session['utype']) == 'trainer':
            return render(request,'trainer/exam/trainer_exam.html')
    except:
        return render(request,'lxpapp/404page.html')


@login_required
def trainer_add_exam_view(request):
    try:
        if str(request.session['utype']) == 'trainer':
            if request.method=='POST':
                examForm=LXPFORM.ExamForm(request.POST)
                if examForm.is_valid(): 
                    examtext = examForm.cleaned_data["exam_name"]
                    exam = LXPModel.Exam.objects.all().filter(exam_name__iexact = examtext)
                    if exam:
                        messages.info(request, 'Exam Name Already Exist')
                        examForm=LXPFORM.ExamForm()
                        return render(request,'trainer/exam/trainer_add_exam.html',{'examForm':examForm})                  
                    else:
                        batch=LXPModel.Batch.objects.get(id=request.POST.get('batchID'))
                        exam = LXPModel.Exam.objects.create(batch_id = batch.id,exam_name = examtext,questiontpye = request.POST.get('questiontpye'))
                        exam.save()
                else:
                    print("form is invalid")
            examForm=LXPFORM.ExamForm()
            from django import forms
            #d = LXPModel.Batch.objects.all().filter(id__in= LXPModel.BatchTrainer.objects.all().filter(trainer_id=str(request.user.id)))
            d = LXPModel.Batch.objects.all()
            examForm.fields['batchID'] = forms.ModelChoiceField(d)
            return render(request,'trainer/exam/trainer_add_exam.html',{'examForm':examForm})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def trainer_update_exam_view(request,pk):
    try:
        if str(request.session['utype']) == 'trainer':
            exam = LXPModel.Exam.objects.get(id=pk)
            examForm=LXPFORM.ExamForm(request.POST,instance=exam)
            
            if request.method=='POST':
                if examForm.is_valid(): 
                    examtext = examForm.cleaned_data["exam_name"]
                    exam = LXPModel.Exam.objects.all().filter(exam_name__iexact = examtext).exclude(id=pk)
                    if exam:
                        messages.info(request, 'Exam Name Already Exist')
                        return render(request,'trainer/exam/trainer_update_exam.html',{'examForm':examForm})
                    else:
                        bid = examForm.cleaned_data['batchID']
                        questiontpye = examForm.cleaned_data['questiontpye']
                        examForm.batchID = bid
                        examForm.questiontpye = questiontpye
                        examForm.save()
                        exams = LXPModel.Exam.objects.all()
                        return render(request,'trainer/exam/trainer_view_exam.html',{'exams':exams})
            return render(request,'trainer/exam/trainer_update_exam.html',{'examForm':examForm,'ex':exam.exam_name,'sub':exam.questiontpye})
    except:
        return render(request,'lxpapp/404page.html')
@login_required
def trainer_upload_exam_csv_view(request):
    if request.method=='POST':
        file=request.FILES["select_file"]
        examtext=request.POST.get('exam_name')
        batch=request.POST.get('batch')
        qtype=request.POST.get('examtype')
        exam = LXPModel.Exam.objects.all().filter(exam_name__iexact = examtext)
        if exam:
            messages.info(request, 'Exam Name Already Exist')
        else:
            if qtype=='0':
                qtype = 'MCQ'
            else:
                qtype = 'ShortAnswer'
            exam = LXPModel.Exam.objects.create(batch_id = batch,exam_name = examtext,questiontpye = qtype)
            exam.save()   
            csv_file = request.FILES["select_file"]
            file_data = csv_file.read().decode("utf-8")		
            lines = file_data.split("\n")
            no = 0
            for line in lines:						
                no = no + 1
                if no > 1:
                    fields = line.split(",")
                    if qtype == 'MCQ':
                        question = LXPModel.McqQuestion.objects.create(
                            question = fields[0],
                            option1 = fields[1],
                            option2 = fields[2],
                            option3 = fields[3],
                            option4 = fields[4],
                            answer = fields[5],
                            marks = fields[6],
                            exam_id = exam.id
                        )
                        question.save()
                    elif qtype == 'ShortAnswer':
                        question = LXPModel.ShortQuestion.objects.create(
                            question = fields[0],
                            marks = fields[1],
                            exam_id = exam.id
                        )
                        question.save()
    batch = LXPModel.Batch.objects.all()
    context = {'batch': batch}
    return render(request,'trainer/exam/trainer_upload_exam_csv.html',context)

def upload_csv(request):
	data = {}
	if "GET" == request.method:
		return render(request, "myapp/upload_csv.html", data)
    # if not GET, then proceed
	try:
		csv_file = request.FILES["csv_file"]
		file_data = csv_file.read().decode("utf-8")		
		lines = file_data.split("\n")
		#loop over the lines and save them in db. If error , store as string and then display
		for line in lines:						
			fields = line.split(",")
			data_dict = {}
			data_dict["name"] = fields[0]
			data_dict["start_date_time"] = fields[1]
			data_dict["end_date_time"] = fields[2]
			data_dict["notes"] = fields[3]
			

	except Exception as e:
		messages.error(request,"Unable to upload file. "+repr(e))

@login_required
def trainer_view_exam_view(request):
    try:
        if str(request.session['utype']) == 'trainer':
            exams = LXPModel.Exam.objects.all().filter(batch_id__in = LXPModel.Batch.objects.all())
            return render(request,'trainer/exam/trainer_view_exam.html',{'exams':exams})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def trainer_delete_exam_view(request,pk):
    try:
        if str(request.session['utype']) == 'trainer':  
            exam=LXPModel.Exam.objects.get(id=pk)
            exam.delete()
            return HttpResponseRedirect('/trainer/trainer-view-exam')
        exams = LXPModel.Exam.objects.all()
        return render(request,'trainer/exam/trainer_view_exam.html',{'exams':exams})
    except:
        return render(request,'lxpapp/404page.html')
 
@login_required
def trainer_mcqquestion_view(request):
    try:
        if str(request.session['utype']) == 'trainer':
            return render(request,'trainer/mcqquestion/trainer_mcqquestion.html')
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def trainer_add_mcqquestion_view(request):
    try:
        if str(request.session['utype']) == 'trainer':
            if request.method=='POST':
                mcqquestionForm=LXPFORM.McqQuestionForm(request.POST)
                if mcqquestionForm.is_valid(): 
                    questiontext = mcqquestionForm.cleaned_data["question"]
                    mcqquestion = LXPModel.McqQuestion.objects.all().filter(question__iexact = questiontext)
                    if mcqquestion:
                        messages.info(request, 'Mcq Question Name Already Exist')
                        mcqquestionForm=LXPFORM.McqQuestionForm()
                        return render(request,'trainer/mcqquestion/trainer_add_mcqquestion.html',{'mcqquestionForm':mcqquestionForm})                  
                    else:
                        exam=LXPModel.Exam.objects.get(id=request.POST.get('examID'))
                        mcqquestion = LXPModel.McqQuestion.objects.create(exam_id = exam.id,question = questiontext,option1=request.POST.get('option1'),option2=request.POST.get('option2'),option3=request.POST.get('option3'),option4=request.POST.get('option4'),answer=request.POST.get('answer'),marks=request.POST.get('marks'))
                        mcqquestion.save()
                else:
                    print("form is invalid")
            mcqquestionForm=LXPFORM.McqQuestionForm()
            return render(request,'trainer/mcqquestion/trainer_add_mcqquestion.html',{'mcqquestionForm':mcqquestionForm})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def trainer_update_mcqquestion_view(request,pk):
    try:
        if str(request.session['utype']) == 'trainer':
            mcqquestion = LXPModel.McqQuestion.objects.get(id=pk)
            mcqquestionForm=LXPFORM.McqQuestionForm(request.POST,instance=mcqquestion)
            if request.method=='POST':
                if mcqquestionForm.is_valid(): 
                    mcqquestiontext = mcqquestionForm.cleaned_data["mcqquestion_name"]
                    mcqquestion = LXPModel.McqQuestion.objects.all().filter(mcqquestion_name__iexact = mcqquestiontext).exclude(id=pk)
                    if mcqquestion:
                        messages.info(request, 'McqQuestion Name Already Exist')
                        return render(request,'trainer/mcqquestion/trainer_update_mcqquestion.html',{'mcqquestionForm':mcqquestionForm})
                    else:
                        mcqquestionForm.save()
                        mcqquestions = LXPModel.McqQuestion.objects.all()
                        return render(request,'trainer/mcqquestion/trainer_view_mcqquestion.html',{'mcqquestions':mcqquestions})
            return render(request,'trainer/mcqquestion/trainer_update_mcqquestion.html',{'mcqquestionForm':mcqquestionForm,'ex':mcqquestion.mcqquestion_name,'sub':mcqquestion.questiontpye})
    except:
        return render(request,'lxpapp/404page.html')
@login_required
def trainer_view_mcqquestion_exams_view(request):
    try:
        if str(request.session['utype']) == 'trainer':
            exams = LXPModel.Exam.objects.all().filter(questiontpye='MCQ')
            return render(request,'trainer/mcqquestion/trainer_view_mcqquestion_exams.html',{'exams':exams})
    except:
        return render(request,'lxpapp/404page.html')
@login_required
def trainer_view_mcqquestion_view(request,examid):
    try:
        if str(request.session['utype']) == 'trainer':
            mcqquestions = LXPModel.McqQuestion.objects.all().filter(exam_id__in = LXPModel.Exam.objects.all().filter(id=examid))
            return render(request,'trainer/mcqquestion/trainer_view_mcqquestion.html',{'mcqquestions':mcqquestions})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def trainer_delete_mcqquestion_view(request,pk):
    try:
        if str(request.session['utype']) == 'trainer':  
            mcqquestion=LXPModel.McqQuestion.objects.get(id=pk)
            mcqquestion.delete()
            return HttpResponseRedirect('/trainer/trainer-view-mcqquestion')
        mcqquestions = LXPModel.McqQuestion.objects.all()
        return render(request,'trainer/mcqquestion/trainer_view_mcqquestion.html',{'mcqquestions':mcqquestions})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def trainer_shortquestion_view(request):
    try:
        if str(request.session['utype']) == 'trainer':
            return render(request,'trainer/shortquestion/trainer_shortquestion.html')
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def trainer_add_shortquestion_view(request):
    try:
        if str(request.session['utype']) == 'trainer':
            if request.method=='POST':
                shortquestionForm=LXPFORM.ShortQuestionForm(request.POST)
                if shortquestionForm.is_valid(): 
                    questiontext = shortquestionForm.cleaned_data["question"]
                    shortquestion = LXPModel.ShortQuestion.objects.all().filter(question__iexact = questiontext)
                    if shortquestion:
                        messages.info(request, 'Short Question Already Exist')
                        shortquestionForm=LXPFORM.ShortQuestionForm()
                        return render(request,'trainer/shortquestion/trainer_add_shortquestion.html',{'shortquestionForm':shortquestionForm})                  
                    else:
                        exam=LXPModel.Exam.objects.get(id=request.POST.get('examID'))
                        shortquestion = LXPModel.ShortQuestion.objects.create(exam_id = exam.id,question = questiontext,marks=request.POST.get('marks'))
                        shortquestion.save()
                else:
                    print("form is invalid")
            shortquestionForm=LXPFORM.ShortQuestionForm()
            return render(request,'trainer/shortquestion/trainer_add_shortquestion.html',{'shortquestionForm':shortquestionForm})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def trainer_update_shortquestion_view(request,pk):
    try:
        if str(request.session['utype']) == 'trainer':
            shortquestion = LXPModel.ShortQuestion.objects.get(id=pk)
            shortquestionForm=LXPFORM.ShortQuestionForm(request.POST,instance=shortquestion)
            if request.method=='POST':
                if shortquestionForm.is_valid(): 
                    shortquestiontext = shortquestionForm.cleaned_data["question"]
                    shortquestion = LXPModel.ShortQuestion.objects.all().filter(question__iexact = shortquestiontext).exclude(id=pk)
                    if shortquestion:
                        messages.info(request, 'ShortQuestion Name Already Exist')
                        return render(request,'trainer/shortquestion/trainer_update_shortquestion.html',{'shortquestionForm':shortquestionForm})
                    else:
                        examid = LXPModel.Exam.objects.all().filter(id=request.POST['examID'])
                        shortquestionForm.examID=examid
                        shortquestionForm.save()
                        shortquestions = LXPModel.ShortQuestion.objects.all()
                        return render(request,'trainer/shortquestion/trainer_view_shortquestion.html',{'shortquestions':shortquestions})
            return render(request,'trainer/shortquestion/trainer_update_shortquestion.html',{'shortquestionForm':shortquestionForm,'ex':shortquestion.question})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def trainer_view_shortquestion_view(request):
    try:
        if str(request.session['utype']) == 'trainer':
            shortquestions = LXPModel.ShortQuestion.objects.all().filter(exam_id__in = LXPModel.Exam.objects.all())
            return render(request,'trainer/shortquestion/trainer_view_shortquestion.html',{'shortquestions':shortquestions})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def trainer_delete_shortquestion_view(request,pk):
    try:
        if str(request.session['utype']) == 'trainer':  
            shortquestion=LXPModel.ShortQuestion.objects.get(id=pk)
            shortquestion.delete()
            return HttpResponseRedirect('/trainer/trainer-view-shortquestion')
        shortquestions = LXPModel.ShortQuestion.objects.all()
        return render(request,'trainer/shortquestion/trainer_view_shortquestion.html',{'shortquestions':shortquestions})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def trainer_pending_short_exam_result_view(request):
    try:
        if str(request.session['utype']) == 'trainer':
            pending = LXPModel.ShortResult.objects.all().filter( learner_id__in = User.objects.all(),exam_id__in = LXPModel.Exam.objects.all(),status = False)
            return render(request,'trainer/shortexam/trainer_pending_short_exam_reuslt.html',{'pending':pending})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def trainer_update_short_question_result_view(request,pk):
    try:
        if str(request.session['utype']) == 'trainer':
            resultdetails = LXPModel.ShortResultDetails.objects.all().filter( question_id__in = LXPModel.ShortQuestion.objects.all(),shortresult_id = pk)
            return render(request,'trainer/shortexam/trainer_update_short_question_result.html',{'resultdetails':resultdetails})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def trainer_save_short_question_result_view(request,pk):
    try:
        if str(request.session['utype']) == 'trainer':
            if request.method=="POST":
                feedback=request.POST['newfeedback']
                marks=request.POST['newmarks']
                rid=request.POST['newid']
                qid=request.POST['newqid']
                answer=request.POST['newanswer']
                mainid=request.POST['newmainid']
                resupdate = LXPModel.ShortResultDetails.objects.all().filter(id=pk)
                resupdate.delete()
                resupdate = LXPModel.ShortResultDetails.objects.create(id=pk,marks=marks,feedback=feedback,question_id=qid,answer=answer,shortresult_id=mainid)
                resupdate.save()
                
                totmarks=LXPModel.ShortResultDetails.objects.all().filter(shortresult_id=mainid).aggregate(stars=Sum('marks'))['stars']
                maintbl=LXPModel.ShortResult.objects.get(id=mainid)
                tot=LXPModel.ShortResultDetails.objects.all().filter(shortresult_id=mainid).aggregate(stars=Count('marks'))['stars']
                totgiven=LXPModel.ShortResultDetails.objects.all().filter(shortresult_id=mainid,marks__gt=0).aggregate(stars=Count('marks'))['stars']
                if tot == totgiven:
                    maintbl.status=True
                maintbl.marks = totmarks
                maintbl.save()
                if tot == totgiven:
                    resultdetails = LXPModel.ShortResultDetails.objects.all().filter( question_id__in = LXPModel.ShortQuestion.objects.all(),shortresult_id = pk)
                    return render(request,'trainer/shortexam/trainer_update_short_question_result.html',{'resultdetails':resultdetails})
                else:
                    resultdetails = LXPModel.ShortResultDetails.objects.all().filter( question_id__in = LXPModel.ShortQuestion.objects.all(),shortresult_id = mainid)
                    return render(request,'trainer/shortexam/trainer_update_short_question_result.html',{'resultdetails':resultdetails})
    except:
        return render(request,'lxpapp/404page.html') 

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
    pllist = LXPModel.Playlist.objects.all().exclude(playlist_id='').order_by('name')
    return render(request,'trainer/youtube/trainer_sync_youtube.html',{'pllist':pllist})

@login_required
def trainer_sync_youtube_start_view(request):
    if request.method=='POST':
        pm = PlaylistManager()
        credentials = pm.getCredentials()
        # drive = googleapiclient.discovery.build('drive', 'v3', credentials=credentials)
        # files = drive.files().list().execute()
        alllist = pm.initializePlaylist(credentials)
        plcount = 1
        maxcount = alllist.__len__()
        for PL_ID in alllist:
                PL_NAME = ''#LXPModel.Playlist.objects.values('name').filter(playlist_id = PL_ID)
                plname = LXPModel.Playlist.objects.all().filter(playlist_id = PL_ID)
                for x in plname:
                    PL_NAME = x.name
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
    pllist = LXPModel.Playlist.objects.all().order_by('name')
    return render(request,'trainer/youtube/trainer_sync_youtube.html',{'pllist':pllist})    
######################################################################

@login_required
def trainer_sync_video_folder_view(request):
    return render(request,'trainer/youtube/trainer_sync_video_folder.html')
    

def get_authenticated_service():
    flow = flow_from_clientsecrets(CLIENT_SECRETS_FILE,
                                   scope=YOUTUBE_UPLOAD_SCOPE,
                                   message=MISSING_CLIENT_SECRETS_MESSAGE)

    storage = CLIENT_SECRETS_FILE#os.path.abspath(os.path.join(os.path.dirname(__file__),
                                   #CLIENT_SECRETS_FILE))
    
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, YOUTUBE_UPLOAD_SCOPE)
    flow.run_local_server()
    credentials = flow.credentials
    youtube = googleapiclient.discovery.build(
        YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, credentials=credentials)
    
    return youtube

def initialize_upload(youtube,filewithpath,onlyFoldername,onlyfilenamewithoutextension):
    tags = None
    playlistTitle = onlyFoldername
    title = onlyfilenamewithoutextension
    body = dict(
        snippet=dict(
            title=title,
            description=title,
            tags=tags,
            categoryId=27
        ),
        status=dict(
            privacyStatus='private'
        )
    )
    part=",".join(body.keys())
    insert_request = youtube.videos().insert(
        part=",".join(body.keys()),
        body=body,
        media_body=MediaFileUpload(filewithpath, chunksize=100 * 1024 * 1024, resumable=True)
    )
    resumable_upload(youtube,insert_request,playlistTitle)
    

# This method implements an exponential backoff strategy to resume a
# failed upload.
def resumable_upload(youtube,insert_request,playlisTitle):
    response = None
    error = None
    retry = 0
    while response is None:
        try:
            print("Uploading file...")
            status, response = insert_request.next_chunk()
            if response is not None:
                if 'id' in response:
                    videoId = response['id']
                    print("Video id '%s' was successfully uploaded." % videoId)
                    # objPlaylist = Playlist()
                    # objPlaylist.insert(playlisTitle,videoId)
                    playlist_id = LXPModel.Playlist.objects.all().filter(name=playlisTitle)
                    for x in playlist_id:
                        playlist_id = x.playlist_id
                    add_video_to_playlist(youtube,videoId,playlist_id)

                    #insert_into_playlist(videoId,playlistId)
                else:
                    exit("The upload failed with an unexpected response: %s" % response)
        except HttpError as e:
            if e.resp.status in RETRIABLE_STATUS_CODES:
                error = "A retriable HTTP error %d occurred:\n%s" % (e.resp.status,
                                                                     e.content)
            else:
                raise
        except RETRIABLE_EXCEPTIONS as e:
            error = "A retriable error occurred: %s" % e

        if error is not None:
            print(error)
            retry += 1
            if retry > MAX_RETRIES:
                exit("No longer attempting to retry.")

            max_sleep = 2 ** retry
            sleep_seconds = random.random() * max_sleep
            print("Sleeping %f seconds and then retrying..." % sleep_seconds)
            time.sleep(sleep_seconds)

def add_video_to_playlist(youtube,videoID,playlistID):
    try:
      add_video_request=youtube.playlistItems().insert(
      part="snippet",
      body={
            'snippet': {
              'playlistId': playlistID, 
              'resourceId': {
                      'kind': 'youtube#video',
                  'videoId': videoID
                }
            #'position': 0
            }
    }
     ).execute()
     
    except HttpError as e:
            raise

def trainer_start_sync_video_folder_view(request):
    if request.method=="POST":
        youtube = get_authenticated_service()
        
        folder=request.POST["select_folder"]
        folder = str.replace(folder,'/','\\')
        path ='D:\\upload\\iLMS'
        path =folder

        filelist = []
        folder = ''
        for root, dirs, files in os.walk(path):
            for file in files:
                filelist.append(os.path.join(root,file))
        for filewithpath in filelist:
            fullfolderpath = os.path.dirname(filewithpath)
            onlyfilenamewithextension = os.path.basename(filewithpath)
            file_extension = Path(onlyfilenamewithextension).suffix
            path=os.path.dirname(filewithpath)
            onlyFoldername = os.path.basename(path)
            onlyfilenamewithoutextension = Path(filewithpath).stem
            if file_extension.upper() == '.MP4':
                initialize_upload(youtube,filewithpath,onlyFoldername,onlyfilenamewithoutextension)
        return  redirect("/")

@login_required
def trainer_sync_youtube_byselected_playlist_start_view(request):
    if request.method=='POST':  
        if 'dblist' in request.POST:
            pllist = LXPModel.Playlist.objects.all().order_by('name')
            return render(request,'trainer/youtube/trainer_sync_youtube.html',{'pllist':pllist})
        elif 'cloudlist' in request.POST:
            pm = PlaylistManager()
            credentials = pm.getCredentials()
            pl =  pm.initializePlaylist(credentials)
            pllist = LXPModel.Playlist.objects.all().order_by('name')
            return render(request,'trainer/youtube/trainer_sync_youtube.html',{'pllist':pllist})
        elif 'startselected' in request.POST:
            pm = PlaylistManager()
            selectedlist = request.POST.getlist('playlist[]')
            maxcount = selectedlist.__len__()
            plcount = 1
            credentials = getcredentials(request)
            for PL_NAME in selectedlist:
                print(str(plcount) + ' ' + PL_NAME)
                PL_ID = LXPModel.Playlist.objects.all().filter(name = PL_NAME)
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
        mcqquestion =LXPModel.McqQuestionResource()
        dataset = Dataset()
        new_employee = request.FILES['myfile']
        data_import = dataset.load(new_employee.read())
        result = LXPModel.McqQuestionResource.import_data(dataset,dry_run=True)
        if not result.has_errors():
            LXPModel.McqQuestionResource.import_data(dataset,dry_run=False)        
    return render(request, 'Import_excel_db.html',{})

@login_required
def trainer_view_learner_video_view(request):
    try:
        if str(request.session['utype']) == 'trainer':
            #learner = UserSocialAuth.objects.raw("SELECT social_auth_usersocialauth.id,social_auth_usersocialauth.provider,social_auth_usersocialauth.uid,auth_user.first_name,  auth_user.last_name,  CASE WHEN social_auth_usersocialauth.utype = 0 THEN 'Learner' ELSE 'Trainer' END AS utype,CASE WHEN social_auth_usersocialauth.status = 0 THEN 'Inactive' ELSE 'Active' END AS status,IFNULL(course_name,'') AS course_name,auth_user.id as user_id FROM social_auth_usersocialauth  LEFT OUTER JOIN auth_user ON (social_auth_usersocialauth.user_id = auth_user.id)  WHERE social_auth_usersocialauth.utype = 0 AND social_auth_usersocialauth.status = 1 Order by social_auth_usersocialauth.uid")
            learner = UserSocialAuth.objects.raw('SELECT social_auth_usersocialauth.id,  social_auth_usersocialauth.user_id,  auth_user.first_name,  auth_user.last_name  , GROUP_CONCAT(DISTINCT lxpapp_course.course_name)  as course_name FROM  social_auth_usersocialauth  LEFT OUTER JOIN auth_user ON (social_auth_usersocialauth.user_id = auth_user.id)  INNER JOIN lxpapp_batchlearner ON (auth_user.id = lxpapp_batchlearner.learner_id)  INNER JOIN lxpapp_batchcourse ON (lxpapp_batchlearner.batch_id = lxpapp_batchcourse.batch_id)  INNER JOIN lxpapp_course ON (lxpapp_batchcourse.course_id = lxpapp_course.id) WHERE  (social_auth_usersocialauth.utype = 0 OR  social_auth_usersocialauth.utype = 2) AND  social_auth_usersocialauth.status = 1 GROUP BY  social_auth_usersocialauth.id,  social_auth_usersocialauth.user_id,  auth_user.first_name,  auth_user.last_name ')
            return render(request,'trainer/learnervideo/trainer_view_learner_video.html',{'learner':learner})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def trainer_learner_video_Course_view(request,user_id,userfirstname,userlastname):
#    try:    
        if str(request.session['utype']) == 'trainer':
            videos1 = LXPModel.BatchCourse.objects.raw('SELECT DISTINCT lxpapp_course.id,  lxpapp_course.course_name,lxpapp_batchcourse.batch_id FROM  lxpapp_batchcourse   INNER JOIN lxpapp_course ON (lxpapp_batchcourse.course_id = lxpapp_course.id)   INNER JOIN lxpapp_batch ON (lxpapp_batchcourse.batch_id = lxpapp_batch.id)   INNER JOIN lxpapp_batchlearner ON (lxpapp_batchlearner.batch_id = lxpapp_batch.id) WHERE   lxpapp_batchlearner.learner_id = ' + str(user_id))
            return render(request,'trainer/learnervideo/trainer_learner_video_course.html',{'videos':videos1,'userfirstname':userfirstname,'userlastname':userlastname,'user_id':user_id})
 #   except:
        return render(request,'lxpapp/404page.html')

@login_required
def trainer_learner_video_Course_subject_view(request,course_id,user_id):
#    try:    
        if str(request.session['utype']) == 'trainer':
            # coursename = LXPModel.Course.objects.only('course_name').get(id=course_id).course_name
            # subject = LXPModel.CourseDetails.objects.all().filter(subject_id__in = LXPModel.Playlist.objects.all(),course_id=str(course_id))
            # subject = LXPModel.Playlist.objects.raw('SELECT DISTINCT y.id,  y.name  , (SELECT COUNT (PLI.id) FROM lxpapp_playlistitem PLI LEFT OUTER JOIN lxpapp_video PLIV ON (PLI.video_id = PLIV.id)  WHERE  PLI.playlist_id = y.id) as Vtotal  , (SELECT COUNT(WC.id) FROM  lxpapp_videowatched WC  LEFT OUTER JOIN lxpapp_video WCV ON (WC.video_id = WCV.id)  LEFT OUTER JOIN lxpapp_playlistitem WCPL ON (WCV.id = WCPL.video_id) WHERE WCPL.playlist_id = y.id) as VWatched FROM  lxpapp_coursedetails  LEFT OUTER JOIN lxpapp_playlist y ON (lxpapp_coursedetails.subject_id = y.id)  WHERE lxpapp_coursedetails.course_id = ' + str(course_id))
            # tc = LXPModel.Video.objects.raw('SELECT 1 as id, count(lxpapp_video.id) AS FIELD_1 FROM  lxpapp_coursedetails  LEFT OUTER JOIN lxpapp_playlist ON (lxpapp_coursedetails.subject_id = lxpapp_playlist.id)  LEFT OUTER JOIN lxpapp_playlistitem ON (lxpapp_playlist.id = lxpapp_playlistitem.playlist_id)  LEFT OUTER JOIN lxpapp_video ON (lxpapp_playlistitem.video_id = lxpapp_video.id) WHERE   lxpapp_coursedetails.course_id = ' + str(course_id))
            # wc = LXPModel.VideoWatched.objects.raw('SELECT 1 as id, count(lxpapp_videowatched.id) AS FIELD_1 FROM  lxpapp_videowatched  LEFT OUTER JOIN lxpapp_video ON (lxpapp_videowatched.video_id = lxpapp_video.id)  LEFT OUTER  JOIN lxpapp_playlistitem ON (lxpapp_video.id = lxpapp_playlistitem.video_id)  LEFT OUTER  JOIN lxpapp_playlist ON (lxpapp_playlistitem.playlist_id = lxpapp_playlist.id)  LEFT OUTER  JOIN lxpapp_coursedetails ON (lxpapp_playlist.id = lxpapp_coursedetails.subject_id) WHERE   lxpapp_coursedetails.course_id = ' + str(course_id))
            # per = 0
            # for x in tc:
            #     tc = x.FIELD_1

            # for x in wc:
            #     wc = x.FIELD_1
            # try:
            #     per = (100*wc)/tc
            # except:
            #     per =0
            # dif = tc-wc

            coursename = LXPModel.Course.objects.only('course_name').get(id=course_id).course_name
            #subject = LXPModel.CourseDetails.objects.all().filter(subject_id__in = LXPModel.Playlist.objects.all(),course_id=str(course_id))
            subject = LXPModel.Playlist.objects.raw('SELECT id,name,Vtotal,VWatched FROM ( select distinct  y.id,  y.name ,  ( select    count( xx.id) from lxpapp_coursedetails xx where xx.course_id= yyy.course_id and xx.subject_id = y.id ) as Vtotal , ( select count (lxpapp_videowatched.id) as a from lxpapp_coursedetails ghgh inner join lxpapp_videowatched on (ghgh.chapter_id = lxpapp_videowatched.video_id) where ghgh.id = yyy.id AND lxpapp_videowatched.learner_id = ' + str(user_id) + ' ) as VWatched from lxpapp_coursedetails yyy left outer join lxpapp_playlist y on (yyy.subject_id = y.id) where yyy.course_id = ' + str(course_id) + ' ) ORDER BY name, VWatched')
            tc = LXPModel.Video.objects.raw('select 1 as id, count(lxpapp_coursedetails.id) as Vtotal from lxpapp_coursedetails where lxpapp_coursedetails.course_id = ' + str(course_id))
            wc = LXPModel.VideoWatched.objects.raw('select distinct 1 as id, count (lxpapp_videowatched.id) as VWatched from lxpapp_coursedetails ghgh inner join lxpapp_videowatched on (ghgh.chapter_id = lxpapp_videowatched.video_id) where lxpapp_videowatched.learner_id = ' + str(user_id) + ' AND ghgh.course_id = ' + str(course_id))
            per = 0
            for x in tc:
                tc = x.Vtotal

            for x in wc:
                wc = x.VWatched
            try:
                per = (100*int(wc))/int(tc)
            except:
                per =0
            if tc is None:
                tc = 0
            if wc is None:
                wc = 0
            dif = tc- wc

            return render(request,'trainer/learnervideo/trainer_learner_video_course_subject.html',{'user_id':user_id,'subject':subject,'coursename':coursename,'course_id':course_id,'dif':dif,'per':per,'wc':wc,'tc':tc})
 #   except:
        return render(request,'lxpapp/404page.html')
 
@login_required
def trainer_learner_video_list_view(request,subject_id,course_id,user_id):
    try:     
        if str(request.session['utype']) == 'trainer':
            subjectname = LXPModel.Playlist.objects.only('name').get(id=subject_id).name
            coursename = LXPModel.Course.objects.only('course_name').get(id=course_id).course_name
            list = LXPModel.PlaylistItem.objects.raw('select distinct  mainvid.id,  mainvid.name,      ifnull((SELECT    lxpapp_videowatched.video_id FROM  lxpapp_videowatched where lxpapp_videowatched.learner_id = ' + str(user_id) + ' AND lxpapp_videowatched.video_id =  mainvid.id), 0) as watched,  ifnull((SELECT    lxpapp_videotounlock.video_id FROM  lxpapp_videotounlock where lxpapp_videotounlock.learner_id = ' + str(user_id) + ' AND lxpapp_videotounlock.video_id =  mainvid.id), 0) as unlocked from lxpapp_coursedetails  inner join lxpapp_video mainvid on    (lxpapp_coursedetails.chapter_id = mainvid.id) where  lxpapp_coursedetails.course_id = ' + str (course_id) + ' and lxpapp_coursedetails.subject_id = ' + str (subject_id))  
            return render(request,'trainer/learnervideo/trainer_learner_video_list.html',{'list':list,'subjectname':subjectname,'subject_id':subject_id,'user_id':user_id,'course_id':course_id,'coursename':coursename})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def trainer_learner_approve_video(request,pk,studid):
    #try:
        if str(request.session['utype']) == 'trainer':
            unlock = LXPModel.VideoToUnlock.objects.create(learner_id=studid,video_id=pk)
            unlock.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    #except:
        return render(request,'ilmsapp/404page.html') 

@login_required
def trainer_learner_approveall_video(request,userid,subject_id):
    #try:
        if str(request.session['utype']) == 'trainer':
            videos=LXPModel.Playlist.objects.raw('SELECT   lxpapp_video.id FROM  lxpapp_playlistitem  INNER JOIN lxpapp_video ON (lxpapp_playlistitem.video_id = lxpapp_video.id) where lxpapp_playlistitem.playlist_id = ' + str (subject_id))
            for x in videos:
                unlock = LXPModel.VideoToUnlock.objects.create(learner_id=userid,video_id=x.id)
                unlock.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    #except:
        return render(request,'ilmsapp/404page.html')

@login_required
def trainer_learner_show_video_view(request,subject_id,course_id,video_id):
    try:    
        if str(request.session['utype']) == 'trainer':
            subjectname = LXPModel.Playlist.objects.only('name').get(id=subject_id).name
            coursename = LXPModel.Course.objects.only('course_name').get(id=course_id).course_name
            Videos=LXPModel.Video.objects.all().filter(id=video_id)
            topicname =''
            url=''
            for x in Videos:
                topicname =x.name
                url = "https://www.youtube.com/embed/" + x.video_id
            return render(request,'trainer/learnervideo/trainer_learner_show_video.html',{'topicname':topicname,'url':url,'subjectname':subjectname,'subject_id':subject_id,'course_id':course_id,'coursename':coursename})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def trainer_material_view(request):
    try:
        if str(request.session['utype']) == 'trainer':
            return render(request,'trainer/material/trainer_material.html')
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def trainer_material_chapters_view(request):
    subject = request.GET.get('subject')
    chapters = LXPModel.Video.objects.all().filter(id__in = LXPModel.PlaylistItem.objects.all().filter( playlist_id=subject))
    context = {'chapters': chapters}
    return render(request, 'trainer/material/trainer_material_chapters.html', context)

@login_required
def trainer_material_topics_view(request):
    chapters = request.GET.get('chapters')
    topics = LXPModel.Topic.objects.all().filter(id__in = LXPModel.Video.objects.all().filter( chapter_id=chapters))
    context = {'topics': topics}
    return render(request, 'trainer/material/trainer_material_topics.html', context)

@login_required
def trainer_add_material_view(request):
    try:
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
                    material = LXPModel.Material.objects.create(
                        subject_id = subject,
                        chapter_id = chapter,
                        mtype = mtype,
                        urlvalue=urlvalue,
                        description=description
                    ).save()

            subjects = LXPModel.Playlist.objects.all()
            context = {'subjects': subjects}
            return render(request,'trainer/material/trainer_add_material.html',context)
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def trainer_update_material_view(request,pk):
    try:
        if str(request.session['utype']) == 'trainer':
            material = LXPModel.Video.objects.get(id=pk)
            materialForm=LXPFORM.MaterialForm(request.POST,instance=material)
            if request.method=='POST':
                if materialForm.is_valid(): 
                    materialtext = materialForm.cleaned_data["name"]
                    subjecttext = materialForm.cleaned_data["subjectID"]
                    
                    material = LXPModel.Video.objects.all().filter(name__iexact = materialtext).exclude(id=pk)
                    if material:
                        messages.info(request, 'Material Name Already Exist')
                        return render(request,'trainer/material/trainer_update_material.html',{'materialForm':materialForm})
                    else:
                        subject = LXPModel.Playlist.objects.get(name=subjecttext)
                        
                        material = LXPModel.Video.objects.get(id=pk)
                        oldsubject =LXPModel.PlaylistItem.objects.get(video_id=pk)
                        material.name = materialtext
                        material.save()
                        PLItems = LXPModel.PlaylistItem.objects.get(video_id=pk,playlist_id = oldsubject.playlist_id)
                        PLItems.playlist_id =subject.id
                        PLItems.save()
                        c_list = LXPModel.Video.objects.raw('SELECT   lxpapp_video.id,  lxpapp_video.name,  lxpapp_video.video_id,  lxpapp_playlist.name AS plname FROM  lxpapp_playlistitem  INNER JOIN lxpapp_video ON (lxpapp_playlistitem.video_id = lxpapp_video.id)  INNER JOIN lxpapp_playlist ON (lxpapp_playlistitem.playlist_id = lxpapp_playlist.id)')
                        return render(request,'trainer/material/trainer_view_material.html',{'materials':c_list})
            return render(request,'trainer/material/trainer_update_material.html',{'materialForm':materialForm,'sub':material.name})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def trainer_view_material_view(request):
    try:
        if str(request.session['utype']) == 'trainer':
            c_list = LXPModel.Video.objects.raw('SELECT   lxpapp_video.id,  lxpapp_video.name,  lxpapp_video.video_id,  lxpapp_playlist.name AS plname FROM  lxpapp_playlistitem  INNER JOIN lxpapp_video ON (lxpapp_playlistitem.video_id = lxpapp_video.id)  INNER JOIN lxpapp_playlist ON (lxpapp_playlistitem.playlist_id = lxpapp_playlist.id)')
            materials = LXPModel.Material.objects.all().filter(subject_id__in=LXPModel.Playlist.objects.all())
            return render(request,'trainer/material/trainer_view_material.html',{'materials':materials})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def trainer_delete_material_view(request,pk):
    try:
        if str(request.session['utype']) == 'trainer':  
            material=LXPModel.Material.objects.get(id=pk)
            material.delete()
            materials = LXPModel.Material.objects.all().filter(subject_id__in=LXPModel.Playlist.objects.all())
            return render(request,'trainer/material/trainer_view_material.html',{'materials':materials})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def trainer_show_material_view(request,subjectname,chaptername,materialtype,pk):
    try:
        if str(request.session['utype']) == 'trainer':
            details= LXPModel.Material.objects.all().filter(id=pk)
            if materialtype == '1':
                return render(request,'trainer/material/trainer_material_htmlshow.html',{'details':details})
            if materialtype == '2':
                return render(request,'trainer/material/trainer_material_urlshow.html',{'details':details})
            if materialtype == '3':
                return render(request,'trainer/material/trainer_material_pdfshow.html',{'details':details})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def trainer_upload_file_view(request):
    subjects = LXPModel.Playlist.objects.all()
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
        material = LXPModel.Material.objects.create(
            subject_id = subject,
            chapter_id = chapter,
            mtype = mtype,
            urlvalue=url,
            description=description
        ).save()
    
    subjects = LXPModel.Playlist.objects.all()
    context = {'subjects': subjects}
    return render(request,'trainer/uploadpdf/trainer_upload_file.html',context)

@login_required
def trainer_start_upload_file_view(request):
    if request.method=="POST":
        file=request.FILES["select_file"]
        if file == "":
            return "Please return to previous page and select a file"
        if file:
            output = upload_subject_material_file_to_s3(request, file, settings.AWS_BUCKET_NAME)
            return output
        else:
            return redirect("/")


@login_required
def trainer_k8sterminal_view(request):
    try:
        if str(request.session['utype']) == 'trainer':
            return render(request,'trainer/k8sterminal/trainer_k8sterminal.html')
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def trainer_add_k8sterminal_view(request):
    try:
        if str(request.session['utype']) == 'trainer':
            if request.method=='POST':
                k8sterminalForm=LXPFORM.K8STerminalForm(request.POST)
                learner_id = request.POST['user_name']
                usagevalue = request.POST.get('usagevalue')
                password1 = request.POST.get("password")
                password2 = request.POST.get("confirmpassword")
                if password1 and password2 and password1 != password2:
                    messages.info(request, 'password_mismatch')
                else:
                    k8sterminal = LXPModel.K8STerminal.objects.create(
                        trainer_id = request.user.id,
                        learner_id = learner_id,
                        Password = password1,
                        usagevalue = usagevalue)
                    k8sterminal.save()
                    messages.info(request, 'Record Saved')
            k8sterminalForm=LXPFORM.K8STerminalForm()
            users = User.objects.all().filter(id__in = UserSocialAuth.objects.all().filter(Q(utype=0) | Q(utype=2),status = 1))
            return render(request,'trainer/k8sterminal/trainer_add_k8sterminal.html',{'k8sterminalForm':k8sterminalForm,'users':users})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def trainer_update_k8sterminal_view(request,pk):
    try:
        if str(request.session['utype']) == 'trainer':
            k8sterminal = LXPModel.K8STerminal.objects.get(id=pk)
            k8sterminalForm=LXPFORM.K8STerminalForm(request.POST,instance=k8sterminal)
            if request.method=='POST':
                if k8sterminalForm.is_valid(): 
                    k8sterminaltext = k8sterminalForm.cleaned_data["k8sterminal_name"]
                    chaptertext = k8sterminalForm.cleaned_data["chapterID"]
                    subjecttext = k8sterminalForm.cleaned_data["subjectID"]
                    k8sterminal = LXPModel.K8STerminal.objects.all().filter(k8sterminal_name__iexact = k8sterminaltext).exclude(id=pk)
                    if k8sterminal:
                        messages.info(request, 'K8STerminal Name Already Exist')
                        return render(request,'trainer/k8sterminal/trainer_update_k8sterminal.html',{'k8sterminalForm':k8sterminalForm})
                    else:
                        chapter = LXPModel.Video.objects.get(chapter_name=chaptertext)
                        subject = LXPModel.Playlist.objects.get(subject_name=subjecttext)
                        k8sterminal = LXPModel.K8STerminal.objects.get(id=pk)
                        k8sterminal.k8sterminal_name = k8sterminaltext
                        k8sterminal.subject_id = subject.id
                        k8sterminal.chapter_id = chapter.id
                        k8sterminal.save()
                        c_list = LXPModel.K8STerminal.objects.filter(chapter_id__in=LXPModel.Video.objects.all())
                        return render(request,'trainer/k8sterminal/trainer_view_k8sterminal.html',{'k8sterminals':c_list})
            return render(request,'trainer/k8sterminal/trainer_update_k8sterminal.html',{'k8sterminalForm':k8sterminalForm,'sub':k8sterminal.k8sterminal_name})
    except:
        return render(request,'lxpapp/404page.html')

#c_list = LXPModel.K8STerminal.objects.filter(chapter_id__in=LXPModel.Video.objects.all(),subject_id__in=LXPModel.Playlist.objects.all())
from django.core.paginator import Paginator
@login_required
def trainer_view_k8sterminal_view(request):
    try:
        if str(request.session['utype']) == 'trainer':
            k8sterminals = LXPModel.K8STerminal.objects.all().filter(learner_id__in = User.objects.all().filter(id__in=UserSocialAuth.objects.all()))
            return render(request,'trainer/k8sterminal/trainer_view_k8sterminal.html',{'k8sterminals':k8sterminals})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def trainer_delete_k8sterminal_view(request,pk):
    try:
        if str(request.session['utype']) == 'trainer':  
            k8sterminal=LXPModel.K8STerminal.objects.get(id=pk)
            k8sterminal.delete()
            return HttpResponseRedirect('/trainer/trainer-view-k8sterminal')
        k8sterminals = LXPModel.K8STerminal.objects.all()
        return render(request,'trainer/k8sterminal/trainer_view_k8sterminal.html',{'k8sterminals':k8sterminals})
    except:
        return render(request,'lxpapp/404page.html')


@login_required
def trainer_python_terminal_view(request):
    try:
        if str(request.session['utype']) == 'trainer':  
            return render(request,'trainer/terminals/trainer_python_terminal.html')
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def trainer_linux_terminal_view(request):
    try:
        if str(request.session['utype']) == 'trainer':  
            return render(request,'trainer/terminals/linux/trainer_linux_terminal.html')
    except:
        return render(request,'lxpapp/404page.html')

