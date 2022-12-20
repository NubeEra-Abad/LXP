from telnetlib import STATUS
from django.shortcuts import render
from . import forms,models
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from datetime import date, timedelta
from django.contrib import messages
from time import gmtime, strftime
from ilmsapp import models as iLMSModel
from django.db.models import Sum,Count
from social_django.models import UserSocialAuth

#for showing signup/login button for learner

def learnerclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'learner/learnerclick.html')

def learner_dashboard_view(request):
    #try:    
        if str(request.session['utype']) == 'learner':
            dict={
            'total_Video':0,
            'total_exam':0,
            }
            return render(request,'learner/learner_dashboard.html',context=dict)
    #except:
        return render(request,'ilmsapp/404page.html')

def learner_exam_view(request):
    #try:    
    if str(request.session['utype']) == 'learner':
        course = iLMSModel.Course.objects.all().filter(id__in= iLMSModel.UserCourse.objects.values('course_id').filter (user_id= request.user.id))
        a=''
        for x in course:
            a = x.id
        exams=iLMSModel.Exam.objects.all().filter(questiontpye='MCQ',course_id = a)
        return render(request,'learner/exam/learner_exam.html',{'exams':exams})
    #except:
        return render(request,'ilmsapp/404page.html')

def learner_take_exam_view(request,pk):
    #try:    
        if str(request.session['utype']) == 'learner':
            exam = iLMSModel.Exam.objects.all().filter(id=pk)
            mcqquestion= iLMSModel.McqQuestion.objects.filter(exam_id=pk)
            total_marks = 0
            total_questions = 0
            for x in mcqquestion:
                total_marks = total_marks + x.marks
                total_questions = total_questions + 1
            return render(request,'learner/exam/learner_take_exam.html',{'exam':exam,'total_questions':total_questions,'total_marks':total_marks})
    #except:
        return render(request,'ilmsapp/404page.html')

def learner_start_exam_view(request,pk):
    #try:    
        if str(request.session['utype']) == 'learner':
            if request.method == 'POST':
                mcqresult = iLMSModel.McqResult.objects.create(learner_id = request.user.id,exam_id =pk,marks=0,wrong=0,correct=0)
                mcqresult.save()
                questions=iLMSModel.McqQuestion.objects.all().filter(exam_id=pk).order_by('?')
                score=0
                wrong=0
                correct=0
                total=0
                r_id = 0
                q_id = 0
                r_id = mcqresult.id
                for q in questions:
                    total+=1
                    question = iLMSModel.McqQuestion.objects.all().filter(question=q.question)
                    for i in question:
                        q_id = i.id
                    resdet = iLMSModel.McqResultDetails.objects.create(mcqresult_id = r_id,question_id =q_id,selected =str(request.POST.get(q.question)).replace('option',''))
                    resdet.save()
                    if 'option' + q.answer ==  request.POST.get(q.question):
                        score+= q.marks
                        correct+=1
                        
                    else:
                        wrong+=1
                percent = score/(total) *100
                context = {
                    'score':score,
                    'time': request.POST.get('timer'),
                    'correct':correct,
                    'wrong':wrong,
                    'percent':percent,
                    'total':total
                }
                mcqresult.marks = score
                mcqresult.wrong = wrong
                mcqresult.correct = correct
                mcqresult.timetaken = request.POST.get('timer')
                mcqresult.save()
                resdetobj = iLMSModel.McqResultDetails.objects.raw("SELECT  ilmsapp_mcqquestion.id,  ilmsapp_mcqquestion.question as q,  ilmsapp_mcqquestion.option1 as o1,  ilmsapp_mcqquestion.option2 as o2,  ilmsapp_mcqquestion.option3 as o3,  ilmsapp_mcqquestion.option4 as o4,  ilmsapp_mcqquestion.answer AS Correct,  ilmsapp_mcqresultdetails.selected AS answered   FROM  ilmsapp_mcqresultdetails  LEFT OUTER JOIN ilmsapp_mcqresult ON (ilmsapp_mcqresultdetails.mcqresult_id = ilmsapp_mcqresult.id)  LEFT OUTER JOIN ilmsapp_exam ON (ilmsapp_mcqresult.exam_id = ilmsapp_exam.id)  LEFT OUTER JOIN ilmsapp_mcqquestion ON (ilmsapp_exam.id = ilmsapp_mcqquestion.exam_id)  AND (ilmsapp_mcqresultdetails.question_id = ilmsapp_mcqquestion.id) Where ilmsapp_mcqresult.learner_id= " + str(request.user.id) + " AND ilmsapp_exam.id = " + str(pk) + " AND ilmsapp_mcqresult.id = " +  str(r_id) )
                return render(request,'learner/exam/learner_exam_result.html',{'total':total,'percent':percent, 'wrong':wrong,'correct':correct,'time': request.POST.get('timer'),'score':score,'resdetobj':resdetobj})
            else:
                questions=iLMSModel.McqQuestion.objects.all()
                context = {
                    'questions':questions
                }
            exam=iLMSModel.Exam.objects.get(id=pk)
            questions=iLMSModel.McqQuestion.objects.all().filter(exam_id=exam.id).order_by('?')
            return render(request,'learner/exam/learner_start_exam.html',{'exam':exam,'questions':questions})
    #except:
        return render(request,'ilmsapp/404page.html')

def learner_show_exam_reuslt_view(request,pk):
    #try:    
    if str(request.session['utype']) == 'learner':
        exams=iLMSModel.McqResult.objects.all().filter(exam_id__in = iLMSModel.Exam.objects.all(), learner_id=request.user.id,exam_id = pk)
        
        return render(request,'learner/exam/learner_show_exam_reuslt.html',{'exams':exams})
    #except:
        return render(request,'ilmsapp/404page.html')

def learner_show_exam_reuslt_details_view(request,pk):
    #try:    
    if str(request.session['utype']) == 'learner':
        exams=iLMSModel.McqResultDetails.objects.all().filter(question_id__in = iLMSModel.McqQuestion.objects.all(), mcqresult_id = pk)
        return render(request,'learner/exam/learner_exam_result_details.html',{'exams':exams})
    #except:
        return render(request,'ilmsapp/404page.html')


def learner_short_exam_view(request):
    #try:    
    if str(request.session['utype']) == 'learner':
        course = iLMSModel.Course.objects.all().filter(id__in= iLMSModel.UserCourse.objects.values('course_id').filter (user_id= request.user.id))
        a=''
        for x in course:
            a = x.id
        shortexams=iLMSModel.Exam.objects.all().filter(questiontpye='ShortAnswer',course_id = a)
        return render(request,'learner/shortexam/learner_short_exam.html',{'shortexams':shortexams})
    #except:
        return render(request,'ilmsapp/404page.html')

def learner_take_short_exam_view(request,pk):
    #try:    
        if str(request.session['utype']) == 'learner':
            shortexam = iLMSModel.Exam.objects.all().filter(id=pk)
            mcqquestion= iLMSModel.ShortQuestion.objects.filter(exam_id=pk)
            total_marks = 0
            total_questions = 0
            for x in mcqquestion:
                total_marks = total_marks + x.marks
                total_questions = total_questions + 1
            return render(request,'learner/shortexam/learner_take_short_exam.html',{'shortexam':shortexam,'total_questions':total_questions,'total_marks':total_marks})
    #except:
        return render(request,'ilmsapp/404page.html')

def learner_start_short_exam_view(request,pk):
    #try:    
        if str(request.session['utype']) == 'learner':
            if request.method == 'POST':
                shortresult = iLMSModel.ShortResult.objects.create(learner_id = request.user.id,exam_id =pk,marks=0)
                shortresult.save()
                questions=iLMSModel.ShortQuestion.objects.all().filter(exam_id=pk).order_by('?')
                r_id = 0
                q_id = 0
                r_id = shortresult.id
                for q in questions:
                    question = iLMSModel.ShortQuestion.objects.all().filter(question=q.question)
                    for i in question:
                        q_id = i.id
                    a=request.POST.get(str(q_id))
                    resdet = iLMSModel.ShortResultDetails.objects.create(shortresult_id = r_id,question_id =q_id,answer =a,feedback ='',marks=0)
                    resdet.save()
                    
                shortresult.timetaken = request.POST.get('timer')
                shortresult.save()
                course = iLMSModel.Course.objects.all().filter(id__in= iLMSModel.UserCourse.objects.values('course_id').filter (user_id= request.user.id))
                a=''
                for x in course:
                    a = x.id
                shortexams=iLMSModel.Exam.objects.all().filter(questiontpye='ShortAnswer',course_id = a)
                return render(request,'learner/shortexam/learner_short_exam.html',{'shortexams':shortexams})
            shortexam=iLMSModel.Exam.objects.get(id=pk)
            questions=iLMSModel.ShortQuestion.objects.all().filter(exam_id=shortexam.id).order_by('?')
            return render(request,'learner/shortexam/learner_start_short_exam.html',{'shortexam':shortexam,'questions':questions})
    #except:
        return render(request,'ilmsapp/404page.html')

def learner_show_short_exam_reuslt_view(request,pk):
    #try:    
    if str(request.session['utype']) == 'learner':
        shortexams=iLMSModel.ShortResult.objects.all().filter(exam_id__in = iLMSModel.Exam.objects.all(), learner_id=request.user.id,exam_id = pk)
        return render(request,'learner/shortexam/learner_show_short_exam_reuslt.html',{'shortexams':shortexams})
    #except:
        return render(request,'ilmsapp/404page.html')

def learner_show_short_exam_reuslt_details_view(request,pk):
    #try:    
    if str(request.session['utype']) == 'learner':
        shortexams=iLMSModel.ShortResultDetails.objects.all().filter(question_id__in = iLMSModel.ShortQuestion.objects.all(), shortresult_id = pk)
        return render(request,'learner/shortexam/learner_short_exam_result_details.html',{'shortexams':shortexams})
    #except:
        return render(request,'ilmsapp/404page.html')

def learner_video_Course_view(request):
#    try:    
        if str(request.session['utype']) == 'learner':
            # users = iLMSModel.Course.objects.all().filter(id__in = iLMSModel.UserCourse.objects.all().filter(user_id=str(request.user.id)))  
            # for course in users:
            #     videos1=iLMSModel.CourseDetails.objects.raw(" SELECT ff.id, ff.coursedetails_name, (SELECT count(g.id) AS vw FROM ilmsapp_videowatched as g  WHERE g.learner_id = " + str(request.user.id) + " and g.CourseName = ff.coursedetails_name) as vw, (SELECT count(x.id) AS vw FROM ilmsapp_videolinks as x  WHERE  x.CourseName = ff.coursedetails_name) as ctotal FROM  ilmsapp_coursedetails  as ff LEFT OUTER JOIN ilmsapp_course as a ON (ff.course_id = a.id) LEFT outer JOIN social_auth_usersocialauth as b ON (a.course_name = b.course_name) WHERE   a.course_name = '" + str(course.course_name) + "' and b.user_id = " + str(request.user.id))
            #     return render(request,'learner/learner_video_course.html',{'videos':videos1, 'coursename':str(course.course_name)})
            videos1 = iLMSModel.UserCourse.objects.all().filter(course_id__in = iLMSModel.Course.objects.all(),user_id=str(request.user.id))  
            return render(request,'learner/video/learner_video_course.html',{'videos':videos1})
 #   except:
        return render(request,'ilmsapp/404page.html')

def learner_video_Course_subject_view(request,course_id):
#    try:    
        if str(request.session['utype']) == 'learner':
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

            return render(request,'learner/video/learner_video_course_subject.html',{'subject':subject,'coursename':coursename,'course_id':course_id,'dif':dif,'per':per,'wc':wc,'tc':tc})
 #   except:
        return render(request,'ilmsapp/404page.html')
 
def learner_video_list_view(request,subject_id,course_id):
    try:     
        if str(request.session['utype']) == 'learner':
            subjectname = iLMSModel.Playlist.objects.only('name').get(id=subject_id).name
            coursename = iLMSModel.Course.objects.only('course_name').get(id=course_id).course_name
            list = iLMSModel.PlaylistItem.objects.all().filter(video_id__in = iLMSModel.Video.objects.all(),playlist_id=str(subject_id))  
            return render(request,'learner/video/learner_video_list.html',{'list':list,'subjectname':subjectname,'subject_id':subject_id,'course_id':course_id,'coursename':coursename})
    except:
        return render(request,'ilmsapp/404page.html')

def learner_show_video_view(request,subject_id,course_id,video_id):
    #try:    
        if str(request.session['utype']) == 'learner':
            subjectname = iLMSModel.Playlist.objects.only('name').get(id=subject_id).name
            coursename = iLMSModel.Course.objects.only('course_name').get(id=course_id).course_name
            Videos=iLMSModel.Video.objects.all().filter(id=video_id)
            topicname =''
            url=''
            for x in Videos:
                videocount = iLMSModel.VideoWatched.objects.all().filter(video_id = video_id,learner_id=request.user.id)
                topicname =x.name
                url = "https://www.youtube.com/embed/" + x.video_id
                
            if not videocount:
                for x in Videos:
                    vw=  iLMSModel.VideoWatched.objects.create(video_id = video_id,learner_id=request.user.id)
                    vw.save()
            return render(request,'learner/video/learner_show_video.html',{'topicname':topicname,'url':url,'subjectname':subjectname,'subject_id':subject_id,'course_id':course_id,'coursename':coursename})
    #except:
        return render(request,'ilmsapp/404page.html')