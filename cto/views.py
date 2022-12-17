import os
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from urllib.parse import parse_qs, urlparse
import googleapiclient.discovery
scopes = ["https://www.googleapis.com/auth/youtube.readonly"]
from django.core.mail import send_mail
from django.forms.models import BaseInlineFormSet, inlineformset_factory
from django.forms import formset_factory
from django.shortcuts import render,redirect
from django.urls import reverse_lazy
from time import gmtime, strftime
from . import models
from ilmsapp import models as iLMSModel
from ilmsapp import forms as ILMSFORM
from django.db.models import Sum
from django.db import transaction
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required,user_passes_test
from django.conf import settings
from datetime import datetime
from django.contrib import messages
from django.views.generic import CreateView, DeleteView, ListView, UpdateView
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
    #try:
        if str(request.session['utype']) == 'cto':
            if request.method=='POST':
                subjectForm=ILMSFORM.SubjectForm(request.POST)
                if subjectForm.is_valid(): 
                    subjecttext = subjectForm.cleaned_data["subject_name"]
                    subject = iLMSModel.Subject.objects.all().filter(subject_name__iexact = subjecttext)
                    if subject:
                        messages.info(request, 'Subject Name Already Exist')
                        subjectForm=ILMSFORM.SubjectForm()
                        return render(request,'cto/subject/cto_add_subject.html',{'subjectForm':subjectForm})                  
                    else:
                        subjectForm.save()
                else:
                    print("form is invalid")
            subjectForm=ILMSFORM.SubjectForm()
            return render(request,'cto/subject/cto_add_subject.html',{'subjectForm':subjectForm})
    #except:
        return render(request,'ilmsapp/404page.html')

def cto_update_subject_view(request,pk):
    #try:
        if str(request.session['utype']) == 'cto':
            subject = iLMSModel.Subject.objects.get(id=pk)
            subjectForm=ILMSFORM.SubjectForm(request.POST,instance=subject)
            if request.method=='POST':
                if subjectForm.is_valid(): 
                    subjecttext = subjectForm.cleaned_data["subject_name"]
                    subject = iLMSModel.Subject.objects.all().filter(subject_name__iexact = subjecttext).exclude(id=pk)
                    if subject:
                        messages.info(request, 'Subject Name Already Exist')
                        return render(request,'cto/subject/cto_update_subject.html',{'subjectForm':subjectForm})
                    else:
                        subjectForm.save()
                        subjects = iLMSModel.Subject.objects.all()
                        return render(request,'cto/subject/cto_view_subject.html',{'subjects':subjects})
            return render(request,'cto/subject/cto_update_subject.html',{'subjectForm':subjectForm,'sub':subject.subject_name,'pl':subject.playlist_id})
    #except:
        return render(request,'ilmsapp/404page.html')

def cto_view_subject_view(request):
    try:
        if str(request.session['utype']) == 'cto':
            subjects = iLMSModel.Subject.objects.all()
            return render(request,'cto/subject/cto_view_subject.html',{'subjects':subjects})
    except:
        return render(request,'ilmsapp/404page.html')

def cto_delete_subject_view(request,pk):
    try:
        if str(request.session['utype']) == 'cto':  
            subject=iLMSModel.Subject.objects.get(id=pk)
            subject.delete()
            return HttpResponseRedirect('/cto/subject/cto-view-subject')
        subjects = iLMSModel.Subject.objects.all()
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
                chapterForm=ILMSFORM.ChapterForm(request.POST)
                if chapterForm.is_valid(): 
                    chaptertext = chapterForm.cleaned_data["chapter_name"]
                    chapter = iLMSModel.Chapter.objects.all().filter(chapter_name__iexact = chaptertext)
                    if chapter:
                        messages.info(request, 'Chapter Name Already Exist')
                        chapterForm=ILMSFORM.ChapterForm()
                        return render(request,'cto/chapter/cto_add_chapter.html',{'chapterForm':chapterForm})                  
                    else:

                        subject=iLMSModel.Subject.objects.get(id=request.POST.get('subjectID'))
                        chapter = iLMSModel.Chapter.objects.create(subject_id = subject.id,chapter_name = chaptertext)
                        chapter.save()
                else:
                    print("form is invalid")
            chapterForm=ILMSFORM.ChapterForm()
            return render(request,'cto/chapter/cto_add_chapter.html',{'chapterForm':chapterForm})
    #except:
        return render(request,'ilmsapp/404page.html')

def cto_update_chapter_view(request,pk):
    #try:
        if str(request.session['utype']) == 'cto':
            chapter = iLMSModel.Chapter.objects.get(id=pk)
            chapterForm=ILMSFORM.ChapterForm(request.POST,instance=chapter)
            if request.method=='POST':
                if chapterForm.is_valid(): 
                    chaptertext = chapterForm.cleaned_data["chapter_name"]
                    subjecttext = chapterForm.cleaned_data["subjectID"]
                    
                    chapter = iLMSModel.Chapter.objects.all().filter(chapter_name__iexact = chaptertext).exclude(id=pk)
                    if chapter:
                        messages.info(request, 'Chapter Name Already Exist')
                        return render(request,'cto/chapter/cto_update_chapter.html',{'chapterForm':chapterForm})
                    else:
                        subject = iLMSModel.Subject.objects.get(subject_name=subjecttext)
                        chapter = iLMSModel.Chapter.objects.get(id=pk)
                        chapter.chapter_name = chaptertext
                        chapter.subject_id = subject.id
                        chapter.save()
                        c_list = iLMSModel.Chapter.objects.filter(subject_id__in=iLMSModel.Subject.objects.all())
                        return render(request,'cto/chapter/cto_view_chapter.html',{'chapters':c_list})
            return render(request,'cto/chapter/cto_update_chapter.html',{'chapterForm':chapterForm,'sub':chapter.chapter_name})
    #except:
        return render(request,'ilmsapp/404page.html')

def cto_view_chapter_view(request):
    #try:
        if str(request.session['utype']) == 'cto':
            c_list = iLMSModel.Chapter.objects.filter(subject_id__in=iLMSModel.Subject.objects.all())
            return render(request,'cto/chapter/cto_view_chapter.html',{'chapters':c_list})
    #except:
        return render(request,'ilmsapp/404page.html')

def cto_delete_chapter_view(request,pk):
    try:
        if str(request.session['utype']) == 'cto':  
            chapter=iLMSModel.Chapter.objects.get(id=pk)
            chapter.delete()
            return HttpResponseRedirect('/cto/chapter/cto-view-chapter')
        chapters = iLMSModel.Chapter.objects.all()
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
                topicForm=ILMSFORM.TopicForm(request.POST)
                if topicForm.is_valid(): 
                    topictext = topicForm.cleaned_data["topic_name"]
                    topic = iLMSModel.Topic.objects.all().filter(topic_name__iexact = topictext)
                    if topic:
                        messages.info(request, 'Topic Name Already Exist')
                        topicForm=ILMSFORM.TopicForm()
                        return render(request,'cto/topic/cto_add_topic.html',{'topicForm':topicForm})                  
                    else:

                        chapter=iLMSModel.Chapter.objects.get(id=request.POST.get('chapterID'))
                        subject=iLMSModel.Subject.objects.get(id=request.POST.get('subjectID'))
                        topic = iLMSModel.Topic.objects.create(subject_id = subject.id,chapter_id = chapter.id,topic_name = topictext)
                        topic.save()
                else:
                    print("form is invalid")
            topicForm=ILMSFORM.TopicForm()
            return render(request,'cto/topic/cto_add_topic.html',{'topicForm':topicForm})
    #except:
        return render(request,'ilmsapp/404page.html')

def cto_update_topic_view(request,pk):
    #try:
        if str(request.session['utype']) == 'cto':
            topic = iLMSModel.Topic.objects.get(id=pk)
            topicForm=ILMSFORM.TopicForm(request.POST,instance=topic)
            if request.method=='POST':
                if topicForm.is_valid(): 
                    topictext = topicForm.cleaned_data["topic_name"]
                    chaptertext = topicForm.cleaned_data["chapterID"]
                    subjecttext = topicForm.cleaned_data["subjectID"]
                    topic = iLMSModel.Topic.objects.all().filter(topic_name__iexact = topictext).exclude(id=pk)
                    if topic:
                        messages.info(request, 'Topic Name Already Exist')
                        return render(request,'cto/topic/cto_update_topic.html',{'topicForm':topicForm})
                    else:
                        chapter = iLMSModel.Chapter.objects.get(chapter_name=chaptertext)
                        subject = iLMSModel.Subject.objects.get(subject_name=subjecttext)
                        topic = iLMSModel.Topic.objects.get(id=pk)
                        topic.topic_name = topictext
                        topic.subject_id = subject.id
                        topic.chapter_id = chapter.id
                        topic.save()
                        c_list = iLMSModel.Topic.objects.filter(chapter_id__in=iLMSModel.Chapter.objects.all())
                        return render(request,'cto/topic/cto_view_topic.html',{'topics':c_list})
            return render(request,'cto/topic/cto_update_topic.html',{'topicForm':topicForm,'sub':topic.topic_name})
    #except:
        return render(request,'ilmsapp/404page.html')

def cto_view_topic_view(request):
    #try:
        if str(request.session['utype']) == 'cto':
            c_list = iLMSModel.Topic.objects.filter(chapter_id__in=iLMSModel.Chapter.objects.all(),subject_id__in=iLMSModel.Subject.objects.all())
            return render(request,'cto/topic/cto_view_topic.html',{'topics':c_list})
    #except:
        return render(request,'ilmsapp/404page.html')

def cto_delete_topic_view(request,pk):
    try:
        if str(request.session['utype']) == 'cto':  
            topic=iLMSModel.Topic.objects.get(id=pk)
            topic.delete()
            return HttpResponseRedirect('/cto/topic/cto-view-topic')
        topics = iLMSModel.Topic.objects.all()
        return render(request,'cto/topic/cto_view_topic.html',{'topics':topics})
    except:
        return render(request,'ilmsapp/404page.html')


def cto_course_view(request):
    try:
        if str(request.session['utype']) == 'cto':
            return render(request,'cto/course/cto_course.html')
    except:
        return render(request,'ilmsapp/404page.html')

def cto_add_course_view(request):
    #try:
        if str(request.session['utype']) == 'cto':
            if request.method=='POST':
                courseForm=ILMSFORM.CourseForm(request.POST)
                coursedetailsForm=ILMSFORM.CourseDetailsFormset(request.POST)
                if courseForm.is_valid() and coursedetailsForm.is_valid() : 
                    coursetext = courseForm.cleaned_data["course_name"]
                    course = iLMSModel.Course.objects.all().filter(course_name__iexact = coursetext)
                    if course:
                        messages.info(request, 'Course Name Already Exist')
                        courseForm=ILMSFORM.CourseForm()
                        coursedetailsForm=ILMSFORM.CourseDetailsFormset()
                        return render(request,'cto/course/cto_add_course.html',{'courseForm':courseForm,'coursedetailsForm':coursedetailsForm})
                    else:
                        course = courseForm.save(commit=False)
                        course.save()
                        for form in coursedetailsForm.forms:
                            refid = None
                            subject = None
                            chapter = None
                            topic = None
                            refid = form.cleaned_data['subject']
                            if refid:
                                subject=iLMSModel.Subject.objects.get(id=refid.id)
                            refid = form.cleaned_data['chapter']
                            
                            if refid:
                                chapter=iLMSModel.Chapter.objects.get(id=refid.id)
                            refid = form.cleaned_data['topic']
                            if refid:
                                topic=iLMSModel.Topic.objects.get(id=refid.id)
                            if subject and chapter and topic :
                                coursedetails = iLMSModel.CourseDetails.objects.create(subject_id = subject.id,chapter_id = chapter.id,topic_id = topic.id,course_id =course.id )
                                coursedetails.save()
                        messages.info(request, 'Course saved')
                else:
                    print("form is invalid")
            courseForm=ILMSFORM.CourseForm()
            coursedetailsForm=ILMSFORM.CourseDetailsFormset()
            return render(request,'cto/course/cto_add_course.html',{'courseForm':courseForm,'coursedetailsForm':coursedetailsForm})
    #except:
        return render(request,'ilmsapp/404page.html')
def cto_view_course_view(request):
    #try:
        if str(request.session['utype']) == 'cto':
            c_list = iLMSModel.Course.objects.all()
            return render(request,'cto/course/cto_view_course.html',{'courses':c_list})
    #except:
        return render(request,'ilmsapp/404page.html')

def cto_view_course_details_view(request,cname):
    #try:
        if str(request.session['utype']) == 'cto':
            c_list = iLMSModel.CourseDetails.objects.filter(course_id__in=iLMSModel.Course.objects.all().filter(course_name=cname),chapter_id__in=iLMSModel.Chapter.objects.all(),subject_id__in=iLMSModel.Subject.objects.all(),topic_id__in=iLMSModel.Topic.objects.all())
            return render(request,'cto/course/cto_view_course_details.html',{'courses':c_list,'cname':cname})
    #except:
        return render(request,'ilmsapp/404page.html')

def cto_delete_course_view(request,pk):
    #try:
        if str(request.session['utype']) == 'cto':  
            course=iLMSModel.Course.objects.get(id=pk)
            course.delete()
            c_list = iLMSModel.Course.objects.all()
            return render(request,'cto/course/cto_view_course.html',{'courses':c_list})
    #except:
        return render(request,'ilmsapp/404page.html')

class CourseList(ListView):
    model = iLMSModel.Course
class courseCreate(CreateView):
    model = iLMSModel.Course
    fields = ['course_name']

class CDetailsCreate(CreateView):
    model = iLMSModel.Course
    fields = ['course_name']
    success_url = reverse_lazy('course-list')

    def get_context_data(self, **kwargs):
        data = super(CDetailsCreate, self).get_context_data(**kwargs)
        if self.request.POST:
            data['cdetails'] = ILMSFORM.CourseDetailsFormset(self.request.POST)
        else:
            data['cdetails'] = ILMSFORM.CourseDetailsFormset
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        cdetails = context['cdetails']
        with transaction.atomic():
            self.object = form.save()
            if cdetails.is_valid():
                cdetails.instance = self.object
                cdetails.save()
        return super(CDetailsCreate, self).form_valid(form)

class courseUpdate(UpdateView):
    model = iLMSModel.Course
    success_url = '/'
    fields = ['course_name']

class CDetailsUpdate(UpdateView):
    model = iLMSModel.Course
    fields = ['course_name']
    success_url = reverse_lazy('course-list')
    def get_context_data(self, **kwargs):
        data = super(CDetailsUpdate, self).get_context_data(**kwargs)
        if self.request.POST:
            data['cdetails'] = ILMSFORM.CourseDetailsFormset(self.request.POST, instance=self.object)
        else:
            data['cdetails'] = ILMSFORM.CourseDetailsFormset(instance=self.object)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        cdetails = context['cdetails']
        with transaction.atomic():
            self.object = form.save()
            if cdetails.is_valid():
                cdetails.instance = self.object
                cdetails.save()
        return super(CDetailsUpdate, self).form_valid(form)

class courseDelete(DeleteView):
    model = iLMSModel.Course
    success_url = reverse_lazy('course-list')

def cto_print_course_view(request):
    try:
        courses = iLMSModel.Course.objects.all()
        return render(request,'cto/course/cto_print_course.html',{'courses':courses})
    except:
        return render(request,'ilmsapp/404page.html')

def cto_print_course_preview_view(request,cname):
    try:
        coursedetails = iLMSModel.CourseDetails.objects.filter(course_id__in=iLMSModel.Course.objects.all().filter(course_name =cname),chapter_id__in=iLMSModel.Chapter.objects.all(),subject_id__in=iLMSModel.Subject.objects.all(),topic_id__in=iLMSModel.Topic.objects.all())
        return render(request,'cto/course/cto_print_course_preview.html',{'coursedetails':coursedetails,'cname':cname})
    except:
        return render(request,'ilmsapp/404page.html')

def cto_passionateskill_view(request):
    try:
        if str(request.session['utype']) == 'cto':
            return render(request,'cto/passionateskill/cto_passionateskill.html')
    except:
        return render(request,'ilmsapp/404page.html')

def cto_add_passionateskill_view(request):
    try:
        if str(request.session['utype']) == 'cto':
            if request.method=='POST':
                passionateskillForm=ILMSFORM.PassionateSkillForm(request.POST)
                if passionateskillForm.is_valid(): 
                    passionateskilltext = passionateskillForm.cleaned_data["passionateskill_name"]
                    passionateskill = iLMSModel.PassionateSkill.objects.all().filter(passionateskill_name__iexact = passionateskilltext)
                    if passionateskill:
                        messages.info(request, 'PassionateSkill Name Already Exist')
                        passionateskillForm=ILMSFORM.PassionateSkillForm()
                        return render(request,'cto/passionateskill/cto_add_passionateskill.html',{'passionateskillForm':passionateskillForm})                  
                    else:
                        passionateskillForm.save()
                else:
                    print("form is invalid")
            passionateskillForm=ILMSFORM.PassionateSkillForm()
            return render(request,'cto/passionateskill/cto_add_passionateskill.html',{'passionateskillForm':passionateskillForm})
    except:
        return render(request,'ilmsapp/404page.html')

def cto_update_passionateskill_view(request,pk):
    #try:
        if str(request.session['utype']) == 'cto':
            passionateskill = iLMSModel.PassionateSkill.objects.get(id=pk)
            passionateskillForm=ILMSFORM.PassionateSkillForm(request.POST,instance=passionateskill)
            if request.method=='POST':
                if passionateskillForm.is_valid(): 
                    passionateskilltext = passionateskillForm.cleaned_data["passionateskill_name"]
                    passionateskill = iLMSModel.PassionateSkill.objects.all().filter(passionateskill_name__iexact = passionateskilltext).exclude(id=pk)
                    if passionateskill:
                        messages.info(request, 'PassionateSkill Name Already Exist')
                        return render(request,'cto/passionateskill/cto_update_passionateskill.html',{'passionateskillForm':passionateskillForm})
                    else:
                        passionateskillForm.save()
                        passionateskills = iLMSModel.PassionateSkill.objects.all()
                        return render(request,'cto/passionateskill/cto_view_passionateskill.html',{'passionateskills':passionateskills})
            return render(request,'cto/passionateskill/cto_update_passionateskill.html',{'passionateskillForm':passionateskillForm,'sub':passionateskill.passionateskill_name})
    #except:
        return render(request,'ilmsapp/404page.html')

def cto_view_passionateskill_view(request):
    try:
        if str(request.session['utype']) == 'cto':
            passionateskills = iLMSModel.PassionateSkill.objects.all()
            return render(request,'cto/passionateskill/cto_view_passionateskill.html',{'passionateskills':passionateskills})
    except:
        return render(request,'ilmsapp/404page.html')

def cto_delete_passionateskill_view(request,pk):
    try:
        if str(request.session['utype']) == 'cto':  
            passionateskill=iLMSModel.PassionateSkill.objects.get(id=pk)
            passionateskill.delete()
            return HttpResponseRedirect('/cto/passionateskill/cto-view-passionateskill')
        passionateskills = iLMSModel.PassionateSkill.objects.all()
        return render(request,'cto/passionateskill/cto_view_passionateskill.html',{'passionateskills':passionateskills})
    except:
        return render(request,'ilmsapp/404page.html')


def cto_knownskill_view(request):
    try:
        if str(request.session['utype']) == 'cto':
            return render(request,'cto/knownskill/cto_knownskill.html')
    except:
        return render(request,'ilmsapp/404page.html')

def cto_add_knownskill_view(request):
    try:
        if str(request.session['utype']) == 'cto':
            if request.method=='POST':
                knownskillForm=ILMSFORM.KnownSkillForm(request.POST)
                if knownskillForm.is_valid(): 
                    knownskilltext = knownskillForm.cleaned_data["knownskill_name"]
                    knownskill = iLMSModel.KnownSkill.objects.all().filter(knownskill_name__iexact = knownskilltext)
                    if knownskill:
                        messages.info(request, 'KnownSkill Name Already Exist')
                        knownskillForm=ILMSFORM.KnownSkillForm()
                        return render(request,'cto/knownskill/cto_add_knownskill.html',{'knownskillForm':knownskillForm})                  
                    else:
                        knownskillForm.save()
                else:
                    print("form is invalid")
            knownskillForm=ILMSFORM.KnownSkillForm()
            return render(request,'cto/knownskill/cto_add_knownskill.html',{'knownskillForm':knownskillForm})
    except:
        return render(request,'ilmsapp/404page.html')

def cto_update_knownskill_view(request,pk):
    #try:
        if str(request.session['utype']) == 'cto':
            knownskill = iLMSModel.KnownSkill.objects.get(id=pk)
            knownskillForm=ILMSFORM.KnownSkillForm(request.POST,instance=knownskill)
            if request.method=='POST':
                if knownskillForm.is_valid(): 
                    knownskilltext = knownskillForm.cleaned_data["knownskill_name"]
                    knownskill = iLMSModel.KnownSkill.objects.all().filter(knownskill_name__iexact = knownskilltext).exclude(id=pk)
                    if knownskill:
                        messages.info(request, 'KnownSkill Name Already Exist')
                        return render(request,'cto/knownskill/cto_update_knownskill.html',{'knownskillForm':knownskillForm})
                    else:
                        knownskillForm.save()
                        knownskills = iLMSModel.KnownSkill.objects.all()
                        return render(request,'cto/knownskill/cto_view_knownskill.html',{'knownskills':knownskills})
            return render(request,'cto/knownskill/cto_update_knownskill.html',{'knownskillForm':knownskillForm,'sub':knownskill.knownskill_name})
    #except:
        return render(request,'ilmsapp/404page.html')

def cto_view_knownskill_view(request):
    try:
        if str(request.session['utype']) == 'cto':
            knownskills = iLMSModel.KnownSkill.objects.all()
            return render(request,'cto/knownskill/cto_view_knownskill.html',{'knownskills':knownskills})
    except:
        return render(request,'ilmsapp/404page.html')

def cto_delete_knownskill_view(request,pk):
    try:
        if str(request.session['utype']) == 'cto':  
            knownskill=iLMSModel.KnownSkill.objects.get(id=pk)
            knownskill.delete()
            return HttpResponseRedirect('/cto/knownskill/cto-view-knownskill')
        knownskills = iLMSModel.KnownSkill.objects.all()
        return render(request,'cto/knownskill/cto_view_knownskill.html',{'knownskills':knownskills})
    except:
        return render(request,'ilmsapp/404page.html')

def cto_playlist_view(request):
    try:
        if str(request.session['utype']) == 'cto':
            return render(request,'cto/playlist/cto_playlist.html')
    except:
        return render(request,'ilmsapp/404page.html')

def cto_add_playlist_view(request):
    try:
        if str(request.session['utype']) == 'cto':
            if request.method=='POST':
                playlistForm=ILMSFORM.PlayListForm(request.POST)
                if playlistForm.is_valid(): 
                    playlisttext = playlistForm.cleaned_data["playlist_name"]
                    playlist = iLMSModel.PlayList.objects.all().filter(playlist_name__iexact = playlisttext)
                    if playlist:
                        messages.info(request, 'PlayList Name Already Exist')
                        playlistForm=ILMSFORM.PlayListForm()
                        return render(request,'cto/playlist/cto_add_playlist.html',{'playlistForm':playlistForm})                  
                    else:
                        playlistForm.save()
                else:
                    print("form is invalid")
            playlistForm=ILMSFORM.PlayListForm()
            return render(request,'cto/playlist/cto_add_playlist.html',{'playlistForm':playlistForm})
    except:
        return render(request,'ilmsapp/404page.html')

def cto_update_playlist_view(request,pk):
    #try:
        if str(request.session['utype']) == 'cto':
            playlist = iLMSModel.PlayList.objects.get(id=pk)
            playlistForm=ILMSFORM.PlayListForm(request.POST,instance=playlist)
            if request.method=='POST':
                if playlistForm.is_valid(): 
                    playlisttext = playlistForm.cleaned_data["playlist_name"]
                    playlist = iLMSModel.PlayList.objects.all().filter(playlist_name__iexact = playlisttext).exclude(id=pk)
                    if playlist:
                        messages.info(request, 'PlayList Name Already Exist')
                        return render(request,'cto/playlist/cto_update_playlist.html',{'playlistForm':playlistForm})
                    else:
                        playlistForm.save()
                        playlists = iLMSModel.PlayList.objects.all()
                        return render(request,'cto/playlist/cto_view_playlist.html',{'playlists':playlists})
            return render(request,'cto/playlist/cto_update_playlist.html',{'playlistForm':playlistForm,'sub':playlist.playlist_name})
    #except:
        return render(request,'ilmsapp/404page.html')

def cto_view_playlist_view(request):
    try:
        if str(request.session['utype']) == 'cto':
            playlists = iLMSModel.PlayList.objects.all()
            return render(request,'cto/playlist/cto_view_playlist.html',{'playlists':playlists})
    except:
        return render(request,'ilmsapp/404page.html')

def cto_delete_playlist_view(request,pk):
    try:
        if str(request.session['utype']) == 'cto':  
            playlist=iLMSModel.PlayList.objects.get(id=pk)
            playlist.delete()
            return HttpResponseRedirect('/cto/playlist/cto-view-playlist')
        playlists = iLMSModel.PlayList.objects.all()
        return render(request,'cto/playlist/cto_view_playlist.html',{'playlists':playlists})
    except:
        return render(request,'ilmsapp/404page.html')

def cto_sync_youtube_view(request):
    pllist = iLMSModel.Subject.objects.all().order_by('subject_name')
    return render(request,'cto/youtube/cto_sync_youtube.html',{'pllist':pllist})

def cto_sync_youtube_start_view(request):
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
    client_secrets_file = "GoogleCredV1.json"
    # Get credentials and create an API client
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
            published = t["snippet"]["publishedAt"]
            if tochk:
                a=''
            else:
                y = models.VideoLinks.objects.create(SrNo=xxx,TopicName=t["snippet"]['title'],Url='https://www.youtube.com/embed/' + t["snippet"]["resourceId"]["videoId"],CourseName=playlistname,TopicCovered=0)
                y.save()
    print ('all done')
    learner = models.Question.objects.raw("SELECT id, count(id) as _count FROM social_auth_usersocialauth WHERE utype = 0")
    a = 0
    b=0
    for countA in learner:
            a=countA._count
    for countA in learner:
            b=countA._count
    dict={
    'total_learner':a,
    'total_trainer':b,
    'total_exam':models.Exam.objects.all().count(),
    'total_question':models.Question.objects.all().count(),
    }
    return render(request,'ilmsapp/admin_dashboard.html',context=dict)

######################################################################
def cto_sync_youtube_byselected_playlist_start_view(request):
    if request.method=='POST':
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
        api_service_name = "youtube"
        api_version = "v3"
        client_secrets_file = "GoogleCredV1.json"
        # Get credentials and create an API client
        xxx = 0
        flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
            client_secrets_file, scopes)
        flow.run_local_server()
        credentials = flow.credentials
        youtube = googleapiclient.discovery.build(
            api_service_name, api_version, credentials=credentials)
        subject_id = None
        selectedlist = request.POST.getlist('playlist[]')
        for plyLstitem in selectedlist:
            print(plyLstitem)
            pllist = iLMSModel.Subject.objects.all().filter(subject_name=plyLstitem)
            playlist_id=''
            for xxyy in pllist:
                playlist_id = xxyy.playlist_id
                subject_id= xxyy.id
            youtube = googleapiclient.discovery.build(
            api_service_name, api_version, credentials=credentials)
            request1 = youtube.playlistItems().list(
                part = "snippet",
                playlistId = playlist_id,
                maxResults = 5000
            )
            response1 = request1.execute()
            playlist_items = []
            playlistname = plyLstitem
            while request1 is not None:
                playlist_items += response1["items"]
                request1 = youtube.playlistItems().list_next(request1, response1)
            for t in playlist_items:
                xxx += 1
                currenturl = 'https://www.youtube.com/embed/' + t["snippet"]["resourceId"]["videoId"]
                print(t["snippet"]["title"])
                tochk= iLMSModel.Chapter.objects.all().filter(chapter_name=t["snippet"]["title"],subject_id=subject_id)
                published = t["snippet"]["publishedAt"]
                if tochk:
                    a=''
                else:
                    chapter= iLMSModel.Chapter.objects.create(chapter_name=t["snippet"]["title"],subject_id=subject_id)
                    chapter.save()
                    y = iLMSModel.VideoLinks.objects.create(subject_id=subject_id,chapter_id=chapter.id,SrNo=xxx,Url='https://www.youtube.com/embed/' + t["snippet"]["resourceId"]["videoId"],TopicCovered=0,video_id=t["snippet"]["resourceId"]["videoId"])
                    y.save()
    print ('all done')
    dict={
    'total_learner':0,
    'total_trainer':0,
    'total_exam':0,
    'total_question':0,
    }
    return render(request,'cto/cto_dashboard.html',context=dict)
