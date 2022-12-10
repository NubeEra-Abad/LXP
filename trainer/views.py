from django.core.mail import send_mail
from django.shortcuts import render,redirect
from time import gmtime, strftime
from django.contrib import messages
from ilmsapp import models as iLMSModel
from ilmsapp import forms as ILMSFORM
from django.db.models import Sum
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required,user_passes_test
from django.conf import settings
from datetime import datetime
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

