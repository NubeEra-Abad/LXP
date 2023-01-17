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
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, View, DeleteView
from django.core import serializers
from django.http import JsonResponse

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
            exams=LXPModel.Exam.objects.raw("SELECT  lxpapp_exam.id,  lxpapp_batch.batch_name,  lxpapp_exam.exam_name FROM  lxpapp_batch  INNER JOIN lxpapp_batchlearner ON (lxpapp_batch.id = lxpapp_batchlearner.batch_id)  INNER JOIN lxpapp_exam ON (lxpapp_batch.id = lxpapp_exam.batch_id) WHERE lxpapp_exam.questiontpye = 'MCQ' AND lxpapp_batchlearner.learner_id = " + str(request.user.id)) 
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
                resdetobj = LXPModel.McqResultDetails.objects.raw("SELECT 1 as id,  lxpapp_mcqquestion.question as q,  lxpapp_mcqquestion.option1 as o1,  lxpapp_mcqquestion.option2 as o2,  lxpapp_mcqquestion.option3 as o3,  lxpapp_mcqquestion.option4 as o4,  lxpapp_mcqquestion.answer AS Correct,  lxpapp_mcqquestion.marks,  lxpapp_mcqresultdetails.selected AS answered  FROM  lxpapp_mcqresultdetails  INNER JOIN lxpapp_mcqresult ON (lxpapp_mcqresultdetails.mcqresult_id = lxpapp_mcqresult.id)  INNER JOIN lxpapp_mcqquestion ON (lxpapp_mcqresultdetails.question_id = lxpapp_mcqquestion.id) WHERE lxpapp_mcqresult.id = " + str(r_id) + " AND lxpapp_mcqresult.learner_id = " + str(request.user.id) + " ORDER BY lxpapp_mcqquestion.id" )
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
            shortexams=LXPModel.Exam.objects.raw("SELECT  lxpapp_exam.id,  lxpapp_batch.batch_name,  lxpapp_exam.exam_name FROM  lxpapp_batch  INNER JOIN lxpapp_batchlearner ON (lxpapp_batch.id = lxpapp_batchlearner.batch_id)  INNER JOIN lxpapp_exam ON (lxpapp_batch.id = lxpapp_exam.batch_id) WHERE lxpapp_exam.questiontpye = 'ShortAnswer' AND lxpapp_batchlearner.learner_id = " + str(request.user.id)) 
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
                
                shortexams=LXPModel.Exam.objects.raw("SELECT  lxpapp_exam.id,  lxpapp_batch.batch_name,  lxpapp_exam.exam_name FROM  lxpapp_batch  INNER JOIN lxpapp_batchlearner ON (lxpapp_batch.id = lxpapp_batchlearner.batch_id)  INNER JOIN lxpapp_exam ON (lxpapp_batch.id = lxpapp_exam.batch_id) WHERE lxpapp_exam.questiontpye = 'ShortAnswer' AND lxpapp_batchlearner.learner_id = " + str(request.user.id)) 
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
            videos1 = LXPModel.BatchCourse.objects.raw('SELECT DISTINCT lxpapp_course.id,  lxpapp_course.course_name,lxpapp_batchcourse.batch_id FROM  lxpapp_batchcourse   INNER JOIN lxpapp_course ON (lxpapp_batchcourse.course_id = lxpapp_course.id)   INNER JOIN lxpapp_batch ON (lxpapp_batchcourse.batch_id = lxpapp_batch.id)   INNER JOIN lxpapp_batchlearner ON (lxpapp_batchlearner.batch_id = lxpapp_batch.id) WHERE   lxpapp_batchlearner.learner_id = ' + str(request.user.id))
            return render(request,'learner/video/learner_video_course.html',{'videos':videos1})
    except:
        return render(request,'lxpapp/404page.html')

def learner_video_Course_subject_view(request,course_id):
    try:    
        if str(request.session['utype']) == 'learner':
            coursename = LXPModel.Course.objects.only('course_name').get(id=course_id).course_name
            subject = LXPModel.Playlist.objects.raw('select distinct  y.id,  y.name ,  ( select    count( xx.id) from lxpapp_coursedetails xx where xx.course_id= yyy.course_id and xx.subject_id = y.id ) as Vtotal , ( select count (lxpapp_videowatched.id) as a from lxpapp_coursedetails ghgh inner join lxpapp_videowatched on (ghgh.chapter_id = lxpapp_videowatched.video_id) where ghgh.id = yyy.id AND lxpapp_videowatched.learner_id = ' + str(request.user.id) + ' ) as VWatched from lxpapp_coursedetails yyy left outer join lxpapp_playlist y on (yyy.subject_id = y.id) where yyy.course_id = ' + str(course_id))
            tc = LXPModel.Video.objects.raw('select 1 as id, count(lxpapp_coursedetails.id) as Vtotal from lxpapp_coursedetails where lxpapp_coursedetails.course_id = ' + str(course_id))
            wc = LXPModel.VideoWatched.objects.raw('select 1 as id, count (lxpapp_videowatched.id) as VWatched from lxpapp_coursedetails ghgh inner join lxpapp_videowatched on (ghgh.chapter_id = lxpapp_videowatched.video_id) where lxpapp_videowatched.learner_id = ' + str(request.user.id) + ' AND ghgh.course_id = ' + str(course_id))
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

            return render(request,'learner/video/learner_video_course_subject.html',{'subject':subject,'coursename':coursename,'course_id':course_id,'dif':dif,'per':per,'wc':wc,'tc':tc})
    except:
        return render(request,'lxpapp/404page.html')
 
def learner_video_list_view(request,subject_id,course_id):
    try:     
        if str(request.session['utype']) == 'learner':
            subjectname = LXPModel.Playlist.objects.only('name').get(id=subject_id).name
            coursename = LXPModel.Course.objects.only('course_name').get(id=course_id).course_name
            list = LXPModel.PlaylistItem.objects.raw('select distinct  mainvid.id,  mainvid.name,      ifnull((SELECT    lxpapp_videowatched.video_id FROM  lxpapp_videowatched where lxpapp_videowatched.learner_id = ' + str(request.user.id) + ' AND lxpapp_videowatched.video_id =  mainvid.id), 0) as watched,  ifnull((SELECT    lxpapp_videotounlock.video_id FROM  lxpapp_videotounlock where lxpapp_videotounlock.learner_id = ' + str(request.user.id) + ' AND lxpapp_videotounlock.video_id =  mainvid.id), 0) as unlocked from lxpapp_coursedetails  inner join lxpapp_video mainvid on    (lxpapp_coursedetails.chapter_id = mainvid.id) where  lxpapp_coursedetails.course_id = ' + str (course_id) + ' and lxpapp_coursedetails.subject_id = ' + str (subject_id))  
            return render(request,'learner/video/learner_video_list.html',{'list':list,'subjectname':subjectname,'subject_id':subject_id,'course_id':course_id,'coursename':coursename})
    except:
        return render(request,'lxpapp/404page.html')

def learner_show_video_view(request,subject_id,course_id,video_id):
    try:    
        if str(request.session['utype']) == 'learner':
            subjectname = LXPModel.Playlist.objects.only('name').get(id=subject_id).name
            coursename = LXPModel.Course.objects.only('course_name').get(id=course_id).course_name
            Videos=LXPModel.Video.objects.all().filter(id=video_id)
            vunlock=LXPModel.Video.objects.raw('SELECT DISTINCT   lxpapp_video.id,  lxpapp_video.name FROM  lxpapp_playlistitem  INNER JOIN lxpapp_video ON (lxpapp_playlistitem.video_id = lxpapp_video.id)  INNER JOIN lxpapp_coursedetails ON (lxpapp_video.id = lxpapp_coursedetails.chapter_id)  INNER JOIN lxpapp_batchcourse ON (lxpapp_batchcourse.course_id = lxpapp_coursedetails.course_id)  INNER JOIN lxpapp_batchlearner ON (lxpapp_batchlearner.batch_id = lxpapp_batchcourse.batch_id) WHERE  lxpapp_playlistitem.playlist_id = ' + str(subject_id) + ' AND  lxpapp_video.id > ' + str(video_id) + '  AND lxpapp_batchlearner.learner_id = ' + str(request.user.id) + ' LIMIT 1 ')
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
            if vunlock:
                for x in vunlock:
                    vu=  LXPModel.VideoToUnlock.objects.create(video_id = x.id ,learner_id=request.user.id)
                    vu.save()

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
    try:
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
    except: 
        return render(request,'lxpapp/404page.html')
class CrudView(TemplateView):
    template_name = 'learner/crud_ajax/crud.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['users'] = LXPModel.CrudUser.objects.all()
        return context


class CreateCrudUser(View):
    def  get(self, request):
        name1 = request.GET.get('name', None)
        address1 = request.GET.get('address', None)
        age1 = request.GET.get('age', None)

        obj = LXPModel.CrudUser.objects.create(
            name = name1,
            address = address1,
            age = age1
        )

        user = {'id':obj.id,'name':obj.name,'address':obj.address,'age':obj.age}

        data = {
            'user': user
        }
        return JsonResponse(data)

class DeleteCrudUser(View):
    def  get(self, request):
        id1 = request.GET.get('id', None)
        LXPModel.CrudUser.objects.get(id=id1).delete()
        data = {
            'deleted': True
        }
        return JsonResponse(data)


class UpdateCrudUser(View):
    def  get(self, request):
        id1 = request.GET.get('id', None)
        name1 = request.GET.get('name', None)
        address1 = request.GET.get('address', None)
        age1 = request.GET.get('age', None)

        obj = LXPModel.CrudUser.objects.get(id=id1)
        obj.name = name1
        obj.address = address1
        obj.age = age1
        obj.save()

        user = {'id':obj.id,'name':obj.name,'address':obj.address,'age':obj.age}

        data = {
            'user': user
        }
        return JsonResponse(data)

@login_required
def learner_python_terminal_view(request):
    try:
        if str(request.session['utype']) == 'learner':  
            return render(request,'learner/terminals/learner_python_terminal.html')
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def learner_linux_terminal_view(request):
    try:
        if str(request.session['utype']) == 'learner':  
            return render(request,'learner/terminals/linux/learner_linux_terminal.html')
    except:
        return render(request,'lxpapp/404page.html')