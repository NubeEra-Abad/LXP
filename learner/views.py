from telnetlib import STATUS
from django.shortcuts import render
from . import forms,models
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from datetime import date, timedelta
from django.contrib import messages
from time import gmtime, strftime
from lxpapp import models as LXPModel
from django.db.models import Sum,Count
from social_django.models import UserSocialAuth

#for showing signup/login button for learner

def learnerclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'learner/learnerclick.html')

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

def learner_exam_view(request):
    try:    
        if str(request.session['utype']) == 'learner':
            course = LXPModel.Course.objects.all().filter(id__in= LXPModel.UserCourse.objects.values('course_id').filter (user_id= request.user.id))
            a=''
            for x in course:
                a = x.id
            exams=LXPModel.Exam.objects.all().filter(questiontpye='MCQ',course_id = a)
            return render(request,'learner/exam/learner_exam.html',{'exams':exams})
    except:
        return render(request,'lxpapp/404page.html')

def learner_take_exam_view(request,pk):
    try:    
        if str(request.session['utype']) == 'learner':
            exam = LXPModel.Exam.objects.all().filter(id=pk)
            mcqquestion= LXPModel.McqQuestion.objects.filter(exam_id=pk)
            total_marks = 0
            total_questions = 0
            for x in mcqquestion:
                total_marks = total_marks + x.marks
                total_questions = total_questions + 1
            return render(request,'learner/exam/learner_take_exam.html',{'exam':exam,'total_questions':total_questions,'total_marks':total_marks})
    except:
        return render(request,'lxpapp/404page.html')

def learner_start_exam_view(request,pk):
    try:    
        if str(request.session['utype']) == 'learner':
            if request.method == 'POST':
                mcqresult = LXPModel.McqResult.objects.create(learner_id = request.user.id,exam_id =pk,marks=0,wrong=0,correct=0)
                mcqresult.save()
                questions=LXPModel.McqQuestion.objects.all().filter(exam_id=pk).order_by('?')
                score=0
                wrong=0
                correct=0
                total=0
                r_id = 0
                q_id = 0
                r_id = mcqresult.id
                for q in questions:
                    total+=1
                    question = LXPModel.McqQuestion.objects.all().filter(question=q.question)
                    for i in question:
                        q_id = i.id
                    resdet = LXPModel.McqResultDetails.objects.create(mcqresult_id = r_id,question_id =q_id,selected =str(request.POST.get(q.question)).replace('option',''))
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
                resdetobj = LXPModel.McqResultDetails.objects.raw("SELECT  lxpapp_mcqquestion.id,  lxpapp_mcqquestion.question as q,  lxpapp_mcqquestion.option1 as o1,  lxpapp_mcqquestion.option2 as o2,  lxpapp_mcqquestion.option3 as o3,  lxpapp_mcqquestion.option4 as o4,  lxpapp_mcqquestion.answer AS Correct,  lxpapp_mcqresultdetails.selected AS answered   FROM  lxpapp_mcqresultdetails  LEFT OUTER JOIN lxpapp_mcqresult ON (lxpapp_mcqresultdetails.mcqresult_id = lxpapp_mcqresult.id)  LEFT OUTER JOIN lxpapp_exam ON (lxpapp_mcqresult.exam_id = lxpapp_exam.id)  LEFT OUTER JOIN lxpapp_mcqquestion ON (lxpapp_exam.id = lxpapp_mcqquestion.exam_id)  AND (lxpapp_mcqresultdetails.question_id = lxpapp_mcqquestion.id) Where lxpapp_mcqresult.learner_id= " + str(request.user.id) + " AND lxpapp_exam.id = " + str(pk) + " AND lxpapp_mcqresult.id = " +  str(r_id) )
                return render(request,'learner/exam/learner_exam_result.html',{'total':total,'percent':percent, 'wrong':wrong,'correct':correct,'time': request.POST.get('timer'),'score':score,'resdetobj':resdetobj})
            else:
                questions=LXPModel.McqQuestion.objects.all()
                context = {
                    'questions':questions
                }
            exam=LXPModel.Exam.objects.get(id=pk)
            questions=LXPModel.McqQuestion.objects.all().filter(exam_id=exam.id).order_by('?')
            return render(request,'learner/exam/learner_start_exam.html',{'exam':exam,'questions':questions})
    except:
        return render(request,'lxpapp/404page.html')

def learner_show_exam_reuslt_view(request,pk):
    try:    
        if str(request.session['utype']) == 'learner':
            exams=LXPModel.McqResult.objects.all().filter(exam_id__in = LXPModel.Exam.objects.all(), learner_id=request.user.id,exam_id = pk)
            return render(request,'learner/exam/learner_show_exam_reuslt.html',{'exams':exams})
    except:
        return render(request,'lxpapp/404page.html')

def learner_show_exam_reuslt_details_view(request,pk):
    try:    
        if str(request.session['utype']) == 'learner':
            exams=LXPModel.McqResultDetails.objects.all().filter(question_id__in = LXPModel.McqQuestion.objects.all(), mcqresult_id = pk)
            return render(request,'learner/exam/learner_exam_result_details.html',{'exams':exams})
    except:
        return render(request,'lxpapp/404page.html')


def learner_short_exam_view(request):
    try:    
        if str(request.session['utype']) == 'learner':
            course = LXPModel.Course.objects.all().filter(id__in= LXPModel.UserCourse.objects.values('course_id').filter (user_id= request.user.id))
            a=''
            for x in course:
                a = x.id
            shortexams=LXPModel.Exam.objects.all().filter(questiontpye='ShortAnswer',course_id = a)
            return render(request,'learner/shortexam/learner_short_exam.html',{'shortexams':shortexams})
    except:
        return render(request,'lxpapp/404page.html')

def learner_take_short_exam_view(request,pk):
    try:    
        if str(request.session['utype']) == 'learner':
            shortexam = LXPModel.Exam.objects.all().filter(id=pk)
            mcqquestion= LXPModel.ShortQuestion.objects.filter(exam_id=pk)
            total_marks = 0
            total_questions = 0
            for x in mcqquestion:
                total_marks = total_marks + x.marks
                total_questions = total_questions + 1
            return render(request,'learner/shortexam/learner_take_short_exam.html',{'shortexam':shortexam,'total_questions':total_questions,'total_marks':total_marks})
    except:
        return render(request,'lxpapp/404page.html')

def learner_start_short_exam_view(request,pk):
    try:    
        if str(request.session['utype']) == 'learner':
            if request.method == 'POST':
                shortresult = LXPModel.ShortResult.objects.create(learner_id = request.user.id,exam_id =pk,marks=0)
                shortresult.save()
                questions=LXPModel.ShortQuestion.objects.all().filter(exam_id=pk).order_by('?')
                r_id = 0
                q_id = 0
                r_id = shortresult.id
                for q in questions:
                    question = LXPModel.ShortQuestion.objects.all().filter(question=q.question)
                    for i in question:
                        q_id = i.id
                    a=request.POST.get(str(q_id))
                    resdet = LXPModel.ShortResultDetails.objects.create(shortresult_id = r_id,question_id =q_id,answer =a,feedback ='',marks=0)
                    resdet.save()
                    
                shortresult.timetaken = request.POST.get('timer')
                shortresult.save()
                course = LXPModel.Course.objects.all().filter(id__in= LXPModel.UserCourse.objects.values('course_id').filter (user_id= request.user.id))
                a=''
                for x in course:
                    a = x.id
                shortexams=LXPModel.Exam.objects.all().filter(questiontpye='ShortAnswer',course_id = a)
                return render(request,'learner/shortexam/learner_short_exam.html',{'shortexams':shortexams})
            shortexam=LXPModel.Exam.objects.get(id=pk)
            questions=LXPModel.ShortQuestion.objects.all().filter(exam_id=shortexam.id).order_by('?')
            return render(request,'learner/shortexam/learner_start_short_exam.html',{'shortexam':shortexam,'questions':questions})
    except:
        return render(request,'lxpapp/404page.html')

def learner_show_short_exam_reuslt_view(request,pk):
    try:    
        if str(request.session['utype']) == 'learner':
            shortexams=LXPModel.ShortResult.objects.all().filter(exam_id__in = LXPModel.Exam.objects.all(), learner_id=request.user.id,exam_id = pk)
            return render(request,'learner/shortexam/learner_show_short_exam_reuslt.html',{'shortexams':shortexams})
    except:
        return render(request,'lxpapp/404page.html')

def learner_show_short_exam_reuslt_details_view(request,pk):
    try:    
        if str(request.session['utype']) == 'learner':
            shortexams=LXPModel.ShortResultDetails.objects.all().filter(question_id__in = LXPModel.ShortQuestion.objects.all(), shortresult_id = pk)
            return render(request,'learner/shortexam/learner_short_exam_result_details.html',{'shortexams':shortexams})
    except:
        return render(request,'lxpapp/404page.html')

def learner_video_Course_view(request):
    try:    
        if str(request.session['utype']) == 'learner':
            # users = LXPModel.Course.objects.all().filter(id__in = LXPModel.UserCourse.objects.all().filter(user_id=str(request.user.id)))  
            # for course in users:
            #     videos1=LXPModel.CourseDetails.objects.raw(" SELECT ff.id, ff.coursedetails_name, (SELECT count(g.id) AS vw FROM lxpapp_videowatched as g  WHERE g.learner_id = " + str(request.user.id) + " and g.CourseName = ff.coursedetails_name) as vw, (SELECT count(x.id) AS vw FROM lxpapp_videolinks as x  WHERE  x.CourseName = ff.coursedetails_name) as ctotal FROM  lxpapp_coursedetails  as ff LEFT OUTER JOIN lxpapp_course as a ON (ff.course_id = a.id) LEFT outer JOIN social_auth_usersocialauth as b ON (a.course_name = b.course_name) WHERE   a.course_name = '" + str(course.course_name) + "' and b.user_id = " + str(request.user.id))
            #     return render(request,'learner/learner_video_course.html',{'videos':videos1, 'coursename':str(course.course_name)})
            videos1 = LXPModel.UserCourse.objects.all().filter(course_id__in = LXPModel.Course.objects.all(),user_id=str(request.user.id))  
            return render(request,'learner/video/learner_video_course.html',{'videos':videos1})
    except:
        return render(request,'lxpapp/404page.html')

def learner_video_Course_subject_view(request,course_id):
    try:    
        if str(request.session['utype']) == 'learner':
            coursename = LXPModel.Course.objects.only('course_name').get(id=course_id).course_name
            subject = LXPModel.CourseDetails.objects.all().filter(subject_id__in = LXPModel.Playlist.objects.all(),course_id=str(course_id))
            subject = LXPModel.Playlist.objects.raw('SELECT DISTINCT y.id,  y.name  , (SELECT COUNT (PLI.id) FROM lxpapp_playlistitem PLI LEFT OUTER JOIN lxpapp_video PLIV ON (PLI.video_id = PLIV.id)  WHERE  PLI.playlist_id = y.id) as Vtotal  , (SELECT COUNT(WC.id) FROM  lxpapp_videowatched WC  LEFT OUTER JOIN lxpapp_video WCV ON (WC.video_id = WCV.id)  LEFT OUTER JOIN lxpapp_playlistitem WCPL ON (WCV.id = WCPL.video_id) WHERE WCPL.playlist_id = y.id) as VWatched FROM  lxpapp_coursedetails  LEFT OUTER JOIN lxpapp_playlist y ON (lxpapp_coursedetails.subject_id = y.id)  WHERE lxpapp_coursedetails.course_id = ' + str(course_id))
            tc = LXPModel.Video.objects.raw('SELECT 1 as id, SUM(DISTINCT (SELECT COUNT (PLI.id) FROM lxpapp_playlistitem PLI LEFT OUTER JOIN lxpapp_video PLIV ON (PLI.video_id = PLIV.id) WHERE  PLI.playlist_id = y.id))  as Vtotal FROM  lxpapp_coursedetails LEFT OUTER JOIN lxpapp_playlist y ON (lxpapp_coursedetails.subject_id = y.id) WHERE lxpapp_coursedetails.course_id = ' + str(course_id))
            wc = LXPModel.VideoWatched.objects.raw('SELECT 1 as id, SUM(DISTINCT (SELECT COUNT(WC.id) FROM  lxpapp_videowatched WC  LEFT OUTER JOIN lxpapp_video WCV ON (WC.video_id = WCV.id)  LEFT OUTER JOIN lxpapp_playlistitem WCPL ON (WCV.id = WCPL.video_id) WHERE WCPL.playlist_id = y.id)) as VWatched FROM  lxpapp_coursedetails  LEFT OUTER JOIN lxpapp_playlist y ON (lxpapp_coursedetails.subject_id = y.id)  WHERE lxpapp_coursedetails.course_id = ' + str(course_id))
            per = 0
            for x in tc:
                tc = x.Vtotal

            for x in wc:
                wc = x.VWatched
            try:
                per = (100*wc)/tc
            except:
                per =0
            dif = tc-wc

            return render(request,'learner/video/learner_video_course_subject.html',{'subject':subject,'coursename':coursename,'course_id':course_id,'dif':dif,'per':per,'wc':wc,'tc':tc})
    except:
        return render(request,'lxpapp/404page.html')
 
def learner_video_list_view(request,subject_id,course_id):
    try:     
        if str(request.session['utype']) == 'learner':
            subjectname = LXPModel.Playlist.objects.only('name').get(id=subject_id).name
            coursename = LXPModel.Course.objects.only('course_name').get(id=course_id).course_name
            list = LXPModel.PlaylistItem.objects.raw('SELECT   vid.id,  vid.name,  ifnuLL(lxpapp_videowatched.id, 0) AS watched_id, ifnuLL((SELECT id FROM lxpapp_material Where lxpapp_material.chapter_id = vid.id),0) as matid FROM  lxpapp_playlistitem  LEFT OUTER JOIN lxpapp_video vid ON (lxpapp_playlistitem.video_id = vid.id)  LEFT OUTER JOIN lxpapp_videowatched ON (vid.id = lxpapp_videowatched.video_id) WHERE  lxpapp_playlistitem.playlist_id = '+str (subject_id)+'  AND (lxpapp_videowatched.learner_id = '+str(request.user.id)+' OR  lxpapp_videowatched.learner_id IS NULL  OR  lxpapp_videowatched.learner_id > 0)')  
            return render(request,'learner/video/learner_video_list.html',{'list':list,'subjectname':subjectname,'subject_id':subject_id,'course_id':course_id,'coursename':coursename})
    except:
        return render(request,'lxpapp/404page.html')

def learner_show_video_view(request,subject_id,course_id,video_id):
    try:    
        if str(request.session['utype']) == 'learner':
            subjectname = LXPModel.Playlist.objects.only('name').get(id=subject_id).name
            coursename = LXPModel.Course.objects.only('course_name').get(id=course_id).course_name
            Videos=LXPModel.Video.objects.all().filter(id=video_id)
            topicname =''
            url=''
            for x in Videos:
                videocount = LXPModel.VideoWatched.objects.all().filter(video_id = video_id,learner_id=request.user.id)
                topicname =x.name
                url = "https://www.youtube.com/embed/" + x.video_id
                
            if not videocount:
                for x in Videos:
                    vw=  LXPModel.VideoWatched.objects.create(video_id = video_id,learner_id=request.user.id)
                    vw.save()
            return render(request,'learner/video/learner_show_video.html',{'topicname':topicname,'url':url,'subjectname':subjectname,'subject_id':subject_id,'course_id':course_id,'coursename':coursename})
    except:
        return render(request,'lxpapp/404page.html')


def learner_see_material_view(request,subject_id,chapter_id,course_id,pk):
    try:
        if str(request.session['utype']) == 'learner':
            details= LXPModel.Material.objects.all().filter(id=pk)
            subjectname = LXPModel.Playlist.objects.only('name').get(id=subject_id).name
            chaptername = LXPModel.Video.objects.only('name').get(id=chapter_id).name

            materialtype = 0
            for x in details:
                materialtype = x.mtype

            if materialtype == 1:
                return render(request,'learner/material/learner_material_htmlshow.html',{'details':details,'subjectname':subjectname,'chaptername':chaptername,'subject_id':subject_id,'course_id':course_id})
            if materialtype == 2:
                return render(request,'learner/material/learner_material_urlshow.html',{'details':details,'subjectname':subjectname,'chaptername':chaptername,'subject_id':subject_id,'course_id':course_id})
            if materialtype == 3:
                return render(request,'learner/material/learner_material_pdfshow.html',{'details':details,'subjectname':subjectname,'chaptername':chaptername,'subject_id':subject_id,'course_id':course_id})
    except:
        return render(request,'ilmsapp/404page.html')

def learner_check_k8sterminal_view(request):
    #try:
        if str(request.session['utype']) == 'learner':
            if request.method=='POST':
                password = request.POST.get("password")
                if password == '' or password is None:
                    messages.info(request, 'Please Enter password')
                    return render(request,'learner/k8sterminal/learner_check_k8sterminal.html')
                usage = LXPModel.K8STerminal.objects.all().filter(learner_id= request.user.id)
                if not usage:
                    messages.info(request, 'Invalid password or Terminal Setting not found, please contact to your trainer')
                    return render(request,'learner/k8sterminal/learner_check_k8sterminal.html')
                totcount = 0
                passwordmain=''
                for x in usage:
                    totcount += x.usagevalue
                    passwordmain = x.Password
                usagecount = LXPModel.K8STerminalLearnerCount.objects.all().filter(learner_id= request.user.id)
                count = 0
                for x in usagecount:
                    count += x.usedvalue
                if password != passwordmain:
                    messages.info(request, 'Invalid password or Terminal Setting not found, please contact to your trainer')
                    return render(request,'learner/k8sterminal/learner_check_k8sterminal.html')
                if count > totcount:
                    messages.info(request, 'Terminal usage permission exceed, please contact to your trainer')
                    return render(request,'learner/k8sterminal/learner_check_k8sterminal.html')
                
                count += 1
                usagecount = LXPModel.K8STerminalLearnerCount.objects.create(
                            learner_id = request.user.id,
                            usedvalue = 1
                ).save()
                return render(request,'learner/k8sterminal/learner_launch_k8sterminal.html')
            return render(request,'learner/k8sterminal/learner_check_k8sterminal.html')
    #except: 
        return render(request,'lxpapp/404page.html')