from django.core.mail import send_mail
from django.forms.models import BaseInlineFormSet, inlineformset_factory
from django.forms import formset_factory
from django.shortcuts import render,redirect
from time import gmtime, strftime
from . import models
from ilmsapp import models as QMODEL
from ilmsapp import forms as QFORM
from django.db.models import Sum
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required,user_passes_test
from django.conf import settings
from datetime import datetime
from django.contrib import messages
def ctoclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'cto/ctoclick.html')
def cto_dashboard_view(request):
    #try:
        if str(request.session['utype']) == 'cto':
            dict={
            'total_course':0,
            'total_exam':0,
            'total_shortCourse':0,
            'total_question':0,
            'total_learner':0
            }
        return render(request,'cto/cto_dashboard.html',context=dict)
    #except:
        return render(request,'ilmsapp/404page.html')

def cto_subject_view(request):
    try:
        if str(request.session['utype']) == 'cto':
            return render(request,'cto/subject/cto_subject.html')
    except:
        return render(request,'ilmsapp/404page.html')

def cto_add_subject_view(request):
    try:
        if str(request.session['utype']) == 'cto':
            if request.method=='POST':
                subjectForm=QFORM.SubjectForm(request.POST)
                if subjectForm.is_valid(): 
                    subjecttext = subjectForm.cleaned_data["subject_name"]
                    subject = QMODEL.Subject.objects.all().filter(subject_name__iexact = subjecttext)
                    if subject:
                        messages.info(request, 'Subject Name Already Exist')
                        subjectForm=QFORM.SubjectForm()
                        return render(request,'cto/subject/cto_add_subject.html',{'subjectForm':subjectForm})                  
                    else:
                        subjectForm.save()
                else:
                    print("form is invalid")
            subjectForm=QFORM.SubjectForm()
            return render(request,'cto/subject/cto_add_subject.html',{'subjectForm':subjectForm})
    except:
        return render(request,'ilmsapp/404page.html')

def cto_update_subject_view(request,pk):
    #try:
        if str(request.session['utype']) == 'cto':
            subject = QMODEL.Subject.objects.get(id=pk)
            subjectForm=QFORM.SubjectForm(request.POST,instance=subject)
            if request.method=='POST':
                if subjectForm.is_valid(): 
                    subjecttext = subjectForm.cleaned_data["subject_name"]
                    subject = QMODEL.Subject.objects.all().filter(subject_name__iexact = subjecttext)
                    if subject:
                        messages.info(request, 'Subject Name Already Exist')
                        return render(request,'cto/subject/cto_update_subject.html',{'subjectForm':subjectForm})
                    else:
                        subjectForm.save()
                        subjects = QMODEL.Subject.objects.all()
                        return render(request,'cto/subject/cto_view_subject.html',{'subjects':subjects})
            return render(request,'cto/subject/cto_update_subject.html',{'subjectForm':subjectForm,'sub':subject.subject_name})
    #except:
        return render(request,'ilmsapp/404page.html')

def cto_view_subject_view(request):
    try:
        if str(request.session['utype']) == 'cto':
            subjects = QMODEL.Subject.objects.all()
            return render(request,'cto/subject/cto_view_subject.html',{'subjects':subjects})
    except:
        return render(request,'ilmsapp/404page.html')

def cto_delete_subject_view(request,pk):
    try:
        if str(request.session['utype']) == 'cto':  
            subject=QMODEL.Subject.objects.get(id=pk)
            subject.delete()
            return HttpResponseRedirect('/cto/subject/cto-view-subject')
        subjects = QMODEL.Subject.objects.all()
        return render(request,'cto/subject/cto_view_subject.html',{'subjects':subjects})
    except:
        return render(request,'ilmsapp/404page.html')

def cto_chapter_view(request):
    try:
        if str(request.session['utype']) == 'cto':
            return render(request,'cto/chapter/cto_chapter.html')
    except:
        return render(request,'ilmsapp/404page.html')

def cto_add_chapter_view(request):
    #try:
        if str(request.session['utype']) == 'cto':
            if request.method=='POST':
                chapterForm=QFORM.ChapterForm(request.POST)
                if chapterForm.is_valid(): 
                    chaptertext = chapterForm.cleaned_data["chapter_name"]
                    chapter = QMODEL.Chapter.objects.all().filter(chapter_name__iexact = chaptertext)
                    if chapter:
                        messages.info(request, 'Chapter Name Already Exist')
                        chapterForm=QFORM.ChapterForm()
                        return render(request,'cto/chapter/cto_add_chapter.html',{'chapterForm':chapterForm})                  
                    else:

                        subject=QMODEL.Subject.objects.get(id=request.POST.get('subjectID'))
                        chapter = QMODEL.Chapter.objects.create(subject_id = subject.id,chapter_name = chaptertext)
                        chapter.save()
                else:
                    print("form is invalid")
            chapterForm=QFORM.ChapterForm()
            return render(request,'cto/chapter/cto_add_chapter.html',{'chapterForm':chapterForm})
    #except:
        return render(request,'ilmsapp/404page.html')

def cto_update_chapter_view(request,pk):
    #try:
        if str(request.session['utype']) == 'cto':
            chapter = QMODEL.Chapter.objects.get(id=pk)
            chapterForm=QFORM.ChapterForm(request.POST,instance=chapter)
            if request.method=='POST':
                if chapterForm.is_valid(): 
                    chaptertext = chapterForm.cleaned_data["chapter_name"]
                    subjecttext = chapterForm.cleaned_data["subjectID"]
                    
                    chapter = QMODEL.Chapter.objects.all().filter(chapter_name__iexact = chaptertext)
                    if chapter:
                        messages.info(request, 'Chapter Name Already Exist')
                        return render(request,'cto/chapter/cto_update_chapter.html',{'chapterForm':chapterForm})
                    else:
                        subject = QMODEL.Subject.objects.get(subject_name=subjecttext)
                        chapter = QMODEL.Chapter.objects.get(id=pk)
                        chapter.chapter_name = chaptertext
                        chapter.subject_id = subject.id
                        chapter.save()
                        c_list = QMODEL.Chapter.objects.filter(subject_id__in=QMODEL.Subject.objects.all())
                        return render(request,'cto/chapter/cto_view_chapter.html',{'chapters':c_list})
            return render(request,'cto/chapter/cto_update_chapter.html',{'chapterForm':chapterForm,'sub':chapter.chapter_name})
    #except:
        return render(request,'ilmsapp/404page.html')

def cto_view_chapter_view(request):
    #try:
        if str(request.session['utype']) == 'cto':
            c_list = QMODEL.Chapter.objects.filter(subject_id__in=QMODEL.Subject.objects.all())
            return render(request,'cto/chapter/cto_view_chapter.html',{'chapters':c_list})
    #except:
        return render(request,'ilmsapp/404page.html')

def cto_delete_chapter_view(request,pk):
    try:
        if str(request.session['utype']) == 'cto':  
            chapter=QMODEL.Chapter.objects.get(id=pk)
            chapter.delete()
            return HttpResponseRedirect('/cto/chapter/cto-view-chapter')
        chapters = QMODEL.Chapter.objects.all()
        return render(request,'cto/chapter/cto_view_chapter.html',{'chapters':chapters})
    except:
        return render(request,'ilmsapp/404page.html')

def cto_topic_view(request):
    try:
        if str(request.session['utype']) == 'cto':
            return render(request,'cto/topic/cto_topic.html')
    except:
        return render(request,'ilmsapp/404page.html')

def cto_add_topic_view(request):
    #try:
        if str(request.session['utype']) == 'cto':
            if request.method=='POST':
                topicForm=QFORM.TopicForm(request.POST)
                if topicForm.is_valid(): 
                    topictext = topicForm.cleaned_data["topic_name"]
                    topic = QMODEL.Topic.objects.all().filter(topic_name__iexact = topictext)
                    if topic:
                        messages.info(request, 'Topic Name Already Exist')
                        topicForm=QFORM.TopicForm()
                        return render(request,'cto/topic/cto_add_topic.html',{'topicForm':topicForm})                  
                    else:

                        chapter=QMODEL.Chapter.objects.get(id=request.POST.get('chapterID'))
                        subject=QMODEL.Subject.objects.get(id=request.POST.get('subjectID'))
                        topic = QMODEL.Topic.objects.create(subject_id = subject.id,chapter_id = chapter.id,topic_name = topictext)
                        topic.save()
                else:
                    print("form is invalid")
            topicForm=QFORM.TopicForm()
            return render(request,'cto/topic/cto_add_topic.html',{'topicForm':topicForm})
    #except:
        return render(request,'ilmsapp/404page.html')

def cto_update_topic_view(request,pk):
    #try:
        if str(request.session['utype']) == 'cto':
            topic = QMODEL.Topic.objects.get(id=pk)
            topicForm=QFORM.TopicForm(request.POST,instance=topic)
            if request.method=='POST':
                if topicForm.is_valid(): 
                    topictext = topicForm.cleaned_data["topic_name"]
                    chaptertext = topicForm.cleaned_data["chapterID"]
                    subjecttext = topicForm.cleaned_data["subjectID"]
                    print(subjecttext)
                    print(chaptertext)
                    print(topictext)
                    topic = QMODEL.Topic.objects.all().filter(topic_name__iexact = topictext)
                    if topic:
                        messages.info(request, 'Topic Name Already Exist')
                        return render(request,'cto/topic/cto_update_topic.html',{'topicForm':topicForm})
                    else:
                        chapter = QMODEL.Chapter.objects.get(chapter_name=chaptertext)
                        subject = QMODEL.Subject.objects.get(subject_name=subjecttext)
                        topic = QMODEL.Topic.objects.get(id=pk)
                        topic.topic_name = topictext
                        topic.subject_id = subject.id
                        topic.chapter_id = chapter.id
                        topic.save()
                        c_list = QMODEL.Topic.objects.filter(chapter_id__in=QMODEL.Chapter.objects.all())
                        return render(request,'cto/topic/cto_view_topic.html',{'topics':c_list})
            return render(request,'cto/topic/cto_update_topic.html',{'topicForm':topicForm,'sub':topic.topic_name})
    #except:
        return render(request,'ilmsapp/404page.html')

def cto_view_topic_view(request):
    #try:
        if str(request.session['utype']) == 'cto':
            c_list = QMODEL.Topic.objects.filter(chapter_id__in=QMODEL.Chapter.objects.all(),subject_id__in=QMODEL.Subject.objects.all())
            return render(request,'cto/topic/cto_view_topic.html',{'topics':c_list})
    #except:
        return render(request,'ilmsapp/404page.html')

def cto_delete_topic_view(request,pk):
    try:
        if str(request.session['utype']) == 'cto':  
            topic=QMODEL.Topic.objects.get(id=pk)
            topic.delete()
            return HttpResponseRedirect('/cto/topic/cto-view-topic')
        topics = QMODEL.Topic.objects.all()
        return render(request,'cto/topic/cto_view_topic.html',{'topics':topics})
    except:
        return render(request,'ilmsapp/404page.html')

def cto_course_view(request):
    try:
        if str(request.session['utype']) == 'cto':
            return render(request,'cto/cto_course.html')
    except:
        return render(request,'ilmsapp/404page.html')
def cto_add_course_view(request):
    template_name = 'cto/cto_add_course.html'
    heading_message = 'Formset Demo'
    if request.method == 'GET':
        formset = QFORM.CourseDetailsFormset(request.GET or None)
    elif request.method == 'POST':
        formset = QFORM.CourseDetailsFormset(request.POST)
        if formset.is_valid():
            for form in formset:
                name = form.cleaned_data.get('course_name')
                # save book instance
                if name:
                    QMODEL.CourseDetails(course_id=name).save()
            # once all books are saved, redirect to book list view
            return redirect('cto-view-course')
    return render(request, template_name, {
        'formset': formset,
        'heading': heading_message,
    })
def cto_add_course_view1(request):
    #try:
        if str(request.session['utype']) == 'cto':
            if request.method=='POST':
                courseForm=QFORM.CourseForm(request.POST)
                if courseForm.is_valid(): 
                    coursetext = courseForm.cleaned_data["course_name"]
                    course = QMODEL.Course.objects.all().filter(course_name__iexact = coursetext)
                    if course:
                        messages.info(request, 'Course Name Already Exist')
                        courseForm=QFORM.CourseForm()
                        return render(request,'cto/cto_add_course.html',{'courseForm':courseForm})                  
                    else:
                        courseForm.save()
                else:
                    print("form is invalid")
            courseForm=QFORM.CourseForm()
            return render(request,'cto/cto_add_course.html',{'courseForm':courseForm})
    #except:
        return render(request,'ilmsapp/404page.html')

def cto_view_course_view(request):
    try:
        if str(request.session['utype']) == 'cto':
            courses = QMODEL.Course.objects.all()
            return render(request,'cto/cto_view_course.html',{'courses':courses})
    except:
        return render(request,'ilmsapp/404page.html')
def cto_delete_course_view(request,pk):
    try:
        if str(request.session['utype']) == 'cto':  
            course=QMODEL.Course.objects.get(id=pk)
            course.delete()
            return HttpResponseRedirect('/cto/cto-view-course')
        courses = QMODEL.Course.objects.all()
        return render(request,'cto/cto_view_course.html',{'courses':courses})
    except:
        return render(request,'ilmsapp/404page.html')