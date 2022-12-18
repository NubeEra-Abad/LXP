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
from youtubemanager import PlaylistManager
from cto import models as CTOModel
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
from django.http import HttpResponse
from django.template import loader
@login_required
def ctoclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'cto/ctoclick.html')

@login_required    
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

@login_required
def cto_subject_view(request):
    try:
        if str(request.session['utype']) == 'cto':
            return render(request,'cto/subject/cto_subject.html')
    except:
        return render(request,'ilmsapp/404page.html')

@login_required
def cto_add_subject_view(request):
    #try:
        if str(request.session['utype']) == 'cto':
            if request.method=='POST':
                subjectForm=ILMSFORM.SubjectForm(request.POST)
                if subjectForm.is_valid(): 
                    subjecttext = subjectForm.cleaned_data["name"]
                    subject = iLMSModel.Playlist.objects.all().filter(name__iexact = subjecttext)
                    if subject:
                        messages.info(request, 'Subject Name Already Exist')
                        subjectForm=ILMSFORM.SubjectForm()
                        return render(request,'cto/subject/cto_add_subject.html',{'subjectForm':subjectForm})                  
                    else:
                        plobj = iLMSModel.Playlist.objects.create(name =subjecttext)
                        plobj.channel_id = ''
                        plobj.channel_name = ''
                        plobj.is_yt_mix = False
                        plobj.playlist_id = ''
                        plobj.thumbnail_url = ''
                        plobj.description = ''
                        plobj.video_count = 0
                        plobj.published_at = datetime.now()
                        plobj.is_private_on_yt = False
                        plobj.playlist_yt_player_HTML = ''
                        plobj.playlist_duration = ''
                        plobj.playlist_duration_in_seconds = 0
                        plobj.last_watched = datetime.now()
                        plobj.started_on = datetime.now()
                        plobj.user_notes = ''
                        plobj.user_label = ''
                        plobj.marked_as = ''
                        plobj.is_favorite = False
                        plobj.num_of_accesses = 0
                        plobj.last_accessed_on = datetime.now()
                        plobj.is_user_owned = False
                        plobj.auto_check_for_updates = False
                        plobj.is_in_db = False
                        plobj.has_playlist_changed = False
                        plobj.has_new_updates = False
                        plobj.untube_user = request.user
                        plobj.save()
                else:
                    print("form is invalid")
            subjectForm=ILMSFORM.SubjectForm()
            return render(request,'cto/subject/cto_add_subject.html',{'subjectForm':subjectForm})
    #except:
        return render(request,'ilmsapp/404page.html')

@login_required
def cto_update_subject_view(request,pk):
    #try:
        if str(request.session['utype']) == 'cto':
            subject = iLMSModel.Playlist.objects.get(id=pk)
            subjectForm=ILMSFORM.SubjectForm(request.POST,instance=subject)
            if request.method=='POST':
                if subjectForm.is_valid(): 
                    subjecttext = subjectForm.cleaned_data["name"]
                    subject = iLMSModel.Playlist.objects.all().filter(name__iexact = subjecttext).exclude(id=pk)
                    if subject:
                        messages.info(request, 'Subject Name Already Exist')
                        return render(request,'cto/subject/cto_update_subject.html',{'subjectForm':subjectForm})
                    else:
                        subjectForm.save()
                        subjects = iLMSModel.Playlist.objects.all().filter(playlist_id = '')
                        return render(request,'cto/subject/cto_view_subject.html',{'subjects':subjects})
            return render(request,'cto/subject/cto_update_subject.html',{'subjectForm':subjectForm,'sub':subject.name,'pl':subject.playlist_id})
    #except:
        return render(request,'ilmsapp/404page.html')

@login_required
def cto_view_subject_view(request):
    try:
        if str(request.session['utype']) == 'cto':
            subjects = iLMSModel.Playlist.objects.all().filter(playlist_id = '')
            return render(request,'cto/subject/cto_view_subject.html',{'subjects':subjects})
    except:
        return render(request,'ilmsapp/404page.html')

@login_required
def cto_delete_subject_view(request,pk):
    try:
        if str(request.session['utype']) == 'cto':  
            subject=iLMSModel.Playlist.objects.get(id=pk)
            subject.delete()
            return HttpResponseRedirect('/cto/subject/cto-view-subject')
        subjects = iLMSModel.Playlist.objects.all().filter(playlist_id = '')
        return render(request,'cto/subject/cto_view_subject.html',{'subjects':subjects})
    except:
        return render(request,'ilmsapp/404page.html')

@login_required
def cto_chapter_view(request):
    try:
        if str(request.session['utype']) == 'cto':
            return render(request,'cto/chapter/cto_chapter.html')
    except:
        return render(request,'ilmsapp/404page.html')

@login_required
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

                        subject=iLMSModel.Playlist.objects.get(id=request.POST.get('subjectID'))
                        chapter = iLMSModel.Chapter.objects.create(subject_id = subject.id,chapter_name = chaptertext)
                        chapter.save()
                else:
                    print("form is invalid")
            chapterForm=ILMSFORM.ChapterForm()
            return render(request,'cto/chapter/cto_add_chapter.html',{'chapterForm':chapterForm})
    #except:
        return render(request,'ilmsapp/404page.html')

@login_required
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
                        subject = iLMSModel.Playlist.objects.get(name=subjecttext)
                        chapter = iLMSModel.Chapter.objects.get(id=pk)
                        chapter.chapter_name = chaptertext
                        chapter.subject_id = subject.id
                        chapter.save()
                        c_list = iLMSModel.Chapter.objects.filter(subject_id__in=iLMSModel.Playlist.objects.all())
                        return render(request,'cto/chapter/cto_view_chapter.html',{'chapters':c_list})
            return render(request,'cto/chapter/cto_update_chapter.html',{'chapterForm':chapterForm,'sub':chapter.chapter_name})
    #except:
        return render(request,'ilmsapp/404page.html')

@login_required
def cto_view_chapter_view(request):
    #try:
        if str(request.session['utype']) == 'cto':
            c_list = iLMSModel.Chapter.objects.filter(subject_id__in=iLMSModel.Playlist.objects.all())
            return render(request,'cto/chapter/cto_view_chapter.html',{'chapters':c_list})
    #except:
        return render(request,'ilmsapp/404page.html')

@login_required
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

@login_required
def cto_topic_view(request):
    try:
        if str(request.session['utype']) == 'cto':
            return render(request,'cto/topic/cto_topic.html')
    except:
        return render(request,'ilmsapp/404page.html')

@login_required
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
                        subject=iLMSModel.Playlist.objects.get(id=request.POST.get('subjectID'))
                        topic = iLMSModel.Topic.objects.create(subject_id = subject.id,chapter_id = chapter.id,topic_name = topictext)
                        topic.save()
                else:
                    print("form is invalid")
            topicForm=ILMSFORM.TopicForm()
            return render(request,'cto/topic/cto_add_topic.html',{'topicForm':topicForm})
    #except:
        return render(request,'ilmsapp/404page.html')

@login_required
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
                        subject = iLMSModel.Playlist.objects.get(subject_name=subjecttext)
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

@login_required
def cto_view_topic_view(request):
    #try:
        if str(request.session['utype']) == 'cto':
            c_list = iLMSModel.Topic.objects.filter(chapter_id__in=iLMSModel.Chapter.objects.all(),subject_id__in=iLMSModel.Playlist.objects.all())
            return render(request,'cto/topic/cto_view_topic.html',{'topics':c_list})
    #except:
        return render(request,'ilmsapp/404page.html')

@login_required
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
        from django.forms import modelformset_factory
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
                            refid = form.cleaned_data['subjectID']
                            if refid:
                                subject=iLMSModel.Playlist.objects.get(id=refid.id)
                            refid = form.cleaned_data['chapterID']
                            
                            if refid:
                                chapter=iLMSModel.Chapter.objects.get(id=refid.id)
                            refid = form.cleaned_data['topicID']
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
            c_list = iLMSModel.CourseDetails.objects.filter(course_id__in=iLMSModel.Course.objects.all().filter(course_name=cname),chapter_id__in=iLMSModel.Chapter.objects.all(),subject_id__in=iLMSModel.Playlist.objects.all(),topic_id__in=iLMSModel.Topic.objects.all())
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

@login_required
def cto_print_course_view(request):
    try:
        courses = iLMSModel.Course.objects.all()
        return render(request,'cto/course/cto_print_course.html',{'courses':courses})
    except:
        return render(request,'ilmsapp/404page.html')

@login_required
def cto_print_course_preview_view(request,cname):
    try:
        coursedetails = iLMSModel.CourseDetails.objects.filter(course_id__in=iLMSModel.Course.objects.all().filter(course_name =cname),chapter_id__in=iLMSModel.Chapter.objects.all(),subject_id__in=iLMSModel.Playlist.objects.all(),topic_id__in=iLMSModel.Topic.objects.all())
        return render(request,'cto/course/cto_print_course_preview.html',{'coursedetails':coursedetails,'cname':cname})
    except:
        return render(request,'ilmsapp/404page.html')

@login_required
def cto_passionateskill_view(request):
    try:
        if str(request.session['utype']) == 'cto':
            return render(request,'cto/passionateskill/cto_passionateskill.html')
    except:
        return render(request,'ilmsapp/404page.html')

@login_required
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

@login_required
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

@login_required
def cto_view_passionateskill_view(request):
    try:
        if str(request.session['utype']) == 'cto':
            passionateskills = iLMSModel.PassionateSkill.objects.all()
            return render(request,'cto/passionateskill/cto_view_passionateskill.html',{'passionateskills':passionateskills})
    except:
        return render(request,'ilmsapp/404page.html')

@login_required
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

@login_required
def cto_knownskill_view(request):
    try:
        if str(request.session['utype']) == 'cto':
            return render(request,'cto/knownskill/cto_knownskill.html')
    except:
        return render(request,'ilmsapp/404page.html')

@login_required
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

@login_required
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

@login_required
def cto_view_knownskill_view(request):
    try:
        if str(request.session['utype']) == 'cto':
            knownskills = iLMSModel.KnownSkill.objects.all()
            return render(request,'cto/knownskill/cto_view_knownskill.html',{'knownskills':knownskills})
    except:
        return render(request,'ilmsapp/404page.html')

@login_required
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

@login_required
def getcredentials():
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
    client_secrets_file = "GoogleCredV1.json"

    # Get credentials and create an API client
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes)
    flow.run_local_server()
    credentials = flow.credentials
    return credentials

@login_required
def cto_sync_youtube_view(request):
    pllist = iLMSModel.Playlist.objects.all().order_by('name')
    return render(request,'cto/youtube/cto_sync_youtube.html',{'pllist':pllist})

@login_required
def cto_sync_youtube_start_view(request):
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
                HttpResponse(loader.get_template('cto/youtube/cto_sync_youtube.html').render(
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
        return render(request,'cto/cto_dashboard.html',context=dict)
    pllist = iLMSModel.Playlist.objects.all().order_by('name')
    return render(request,'cto/youtube/cto_sync_youtube.html',{'pllist':pllist})    
######################################################################

@login_required
def cto_sync_youtube_byselected_playlist_start_view(request):
    if request.method=='POST':
        if 'dblist' in request.POST:
            pllist = iLMSModel.Playlist.objects.all().order_by('name')
            return render(request,'cto/youtube/cto_sync_youtube.html',{'pllist':pllist})
        elif 'cloudlist' in request.POST:
            pm = PlaylistManager()
            credentials = getcredentials()
            pl =  pm.initializePlaylist(credentials)
            pllist = iLMSModel.Playlist.objects.all().order_by('name')
            return render(request,'cto/youtube/cto_sync_youtube.html',{'pllist':pllist})
        elif 'startselected' in request.POST:
            pm = PlaylistManager()
            selectedlist = request.POST.getlist('playlist[]')
            maxcount = selectedlist.__len__()
            plcount = 1
            credentials = getcredentials()
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
    return render(request,'cto/cto_dashboard.html',context=dict)

@login_required
def get_message_from_httperror(e):
    return e.error_details[0]['message']