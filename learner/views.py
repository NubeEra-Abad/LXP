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
