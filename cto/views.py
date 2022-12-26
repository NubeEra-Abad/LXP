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
from lxpapp import models as LXPModel
from youtubemanager import PlaylistManager
from cto import models as CTOModel
from lxpapp import forms as ILMSFORM
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
        return render(request,'lxpapp/404page.html')

@login_required
def cto_subject_view(request):
    try:
        if str(request.session['utype']) == 'cto':
            return render(request,'cto/subject/cto_subject.html')
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def cto_add_subject_view(request):
    #try:
        if str(request.session['utype']) == 'cto':
            if request.method=='POST':
                subjectForm=ILMSFORM.SubjectForm(request.POST)
                if subjectForm.is_valid(): 
                    subjecttext = subjectForm.cleaned_data["name"]
                    subject = LXPModel.Playlist.objects.all().filter(name__iexact = subjecttext)
                    if subject:
                        messages.info(request, 'Subject Name Already Exist')
                        subjectForm=ILMSFORM.SubjectForm()
                        return render(request,'cto/subject/cto_add_subject.html',{'subjectForm':subjectForm})                  
                    else:
                        plobj = LXPModel.Playlist.objects.create(name =subjecttext)
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
                        plobj.save()
                else:
                    print("form is invalid")
            subjectForm=ILMSFORM.SubjectForm()
            return render(request,'cto/subject/cto_add_subject.html',{'subjectForm':subjectForm})
    #except:
        return render(request,'lxpapp/404page.html')

@login_required
def cto_update_subject_view(request,pk):
    #try:
        if str(request.session['utype']) == 'cto':
            subject = LXPModel.Playlist.objects.get(id=pk)
            subjectForm=ILMSFORM.SubjectForm(request.POST,instance=subject)
            if request.method=='POST':
                if subjectForm.is_valid(): 
                    subjecttext = subjectForm.cleaned_data["name"]
                    subject = LXPModel.Playlist.objects.all().filter(name__iexact = subjecttext).exclude(id=pk)
                    if subject:
                        messages.info(request, 'Subject Name Already Exist')
                        return render(request,'cto/subject/cto_update_subject.html',{'subjectForm':subjectForm})
                    else:
                        subjectForm.save()
                        subjects = LXPModel.Playlist.objects.all()
                        return render(request,'cto/subject/cto_view_subject.html',{'subjects':subjects})
            return render(request,'cto/subject/cto_update_subject.html',{'subjectForm':subjectForm,'sub':subject.name,'pl':subject.playlist_id})
    #except:
        return render(request,'lxpapp/404page.html')

@login_required
def cto_view_subject_view(request):
    try:
        if str(request.session['utype']) == 'cto':
            subjects = LXPModel.Playlist.objects.all()
            return render(request,'cto/subject/cto_view_subject.html',{'subjects':subjects})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def cto_delete_subject_view(request,pk):
    try:
        if str(request.session['utype']) == 'cto':  
            subject=LXPModel.Playlist.objects.get(id=pk)
            subject.delete()
            return HttpResponseRedirect('/cto/subject/cto-view-subject')
        subjects = LXPModel.Playlist.objects.all().filter(playlist_id = '')
        return render(request,'cto/subject/cto_view_subject.html',{'subjects':subjects})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def cto_chapter_view(request):
    try:
        if str(request.session['utype']) == 'cto':
            return render(request,'cto/chapter/cto_chapter.html')
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def cto_add_chapter_view(request):
    #try:
        if str(request.session['utype']) == 'cto':
            if request.method=='POST':
                chapterForm=ILMSFORM.ChapterForm(request.POST)
                if chapterForm.is_valid(): 
                    chaptertext = chapterForm.cleaned_data["name"]
                    chapter = LXPModel.Video.objects.all().filter(name__iexact = chaptertext)
                    if chapter:
                        messages.info(request, 'Chapter Name Already Exist')
                        chapterForm=ILMSFORM.ChapterForm()
                        return render(request,'cto/chapter/cto_add_chapter.html',{'chapterForm':chapterForm})                  
                    else:
                        subject=LXPModel.Playlist.objects.get(id=request.POST.get('subjectID'))
                        chapter = LXPModel.Video.objects.create(
                            video_id = '',
                            name = chaptertext,
                            duration = '',
                            duration_in_seconds = 0,
                            thumbnail_url = '',
                            published_at = datetime.now(),
                            description = '',
                            has_cc = False,
                            liked = False,
                            public_stats_viewable = False,
                            view_count = 0,
                            like_count = 0,
                            dislike_count = 0,
                            comment_count = 0,
                            yt_player_HTML = '',
                            channel_id = '',
                            channel_name = '',
                            is_unavailable_on_yt = False,
                            was_deleted_on_yt = False,
                            is_planned_to_watch = False,
                            is_marked_as_watched = False,
                            is_favorite = False,
                            num_of_accesses = 0,
                            user_label = '',
                            user_notes = '',
                            video_details_modified = False,
                            )
                        chapter.save()
                        PLItems = LXPModel.PlaylistItem.objects.create(
                            playlist_item_id = '',
                            video_position = 0,
                            published_at = datetime.now(),
                            channel_id = '',
                            channel_name = '',
                            is_duplicate = False,
                            is_marked_as_watched = False,
                            num_of_accesses = 0,
                            playlist_id = subject.id,
                            video_id = chapter.id
                        )
                        PLItems.save()
                else:
                    print("form is invalid")
            chapterForm=ILMSFORM.ChapterForm()
            return render(request,'cto/chapter/cto_add_chapter.html',{'chapterForm':chapterForm})
    #except:
        return render(request,'lxpapp/404page.html')

@login_required
def cto_update_chapter_view(request,pk):
    #try:
        if str(request.session['utype']) == 'cto':
            chapter = LXPModel.Video.objects.get(id=pk)
            chapterForm=ILMSFORM.ChapterForm(request.POST,instance=chapter)
            if request.method=='POST':
                if chapterForm.is_valid(): 
                    chaptertext = chapterForm.cleaned_data["name"]
                    subjecttext = chapterForm.cleaned_data["subjectID"]
                    
                    chapter = LXPModel.Video.objects.all().filter(name__iexact = chaptertext).exclude(id=pk)
                    if chapter:
                        messages.info(request, 'Chapter Name Already Exist')
                        return render(request,'cto/chapter/cto_update_chapter.html',{'chapterForm':chapterForm})
                    else:
                        subject = LXPModel.Playlist.objects.get(name=subjecttext)
                        
                        chapter = LXPModel.Video.objects.get(id=pk)
                        oldsubject =LXPModel.PlaylistItem.objects.get(video_id=pk)
                        chapter.name = chaptertext
                        chapter.save()
                        PLItems = LXPModel.PlaylistItem.objects.get(video_id=pk,playlist_id = oldsubject.playlist_id)
                        PLItems.playlist_id =subject.id
                        PLItems.save()
                        c_list = LXPModel.Video.objects.raw('SELECT   lxpapp_video.id,  lxpapp_video.name,  lxpapp_video.video_id,  lxpapp_playlist.name AS plname FROM  lxpapp_playlistitem  INNER JOIN lxpapp_video ON (lxpapp_playlistitem.video_id = lxpapp_video.id)  INNER JOIN lxpapp_playlist ON (lxpapp_playlistitem.playlist_id = lxpapp_playlist.id)')
                        return render(request,'cto/chapter/cto_view_chapter.html',{'chapters':c_list})
            return render(request,'cto/chapter/cto_update_chapter.html',{'chapterForm':chapterForm,'sub':chapter.name})
    #except:
        return render(request,'lxpapp/404page.html')

@login_required
def cto_view_chapter_view(request):
    #try:
        if str(request.session['utype']) == 'cto':
            c_list = LXPModel.Video.objects.raw('SELECT   lxpapp_video.id,  lxpapp_video.name,  lxpapp_video.video_id,  lxpapp_playlist.name AS plname FROM  lxpapp_playlistitem  INNER JOIN lxpapp_video ON (lxpapp_playlistitem.video_id = lxpapp_video.id)  INNER JOIN lxpapp_playlist ON (lxpapp_playlistitem.playlist_id = lxpapp_playlist.id)')
            return render(request,'cto/chapter/cto_view_chapter.html',{'chapters':c_list})
    #except:
        return render(request,'lxpapp/404page.html')

@login_required
def cto_delete_chapter_view(request,pk):
    try:
        if str(request.session['utype']) == 'cto':  
            chapter=LXPModel.Video.objects.get(id=pk)
            chapter.delete()
            PLItem = LXPModel.PlaylistItem.objects.get(video_id = pk)
            PLItem.delete()
            return HttpResponseRedirect('/cto/chapter/cto-view-chapter')
        chapters = LXPModel.Video.objects.all()
        return render(request,'cto/chapter/cto_view_chapter.html',{'chapters':chapters})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def cto_topic_view(request):
    try:
        if str(request.session['utype']) == 'cto':
            return render(request,'cto/topic/cto_topic.html')
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def cto_add_topic_view(request):
    #try:
        if str(request.session['utype']) == 'cto':
            if request.method=='POST':
                topicForm=ILMSFORM.TopicForm(request.POST)
                if topicForm.is_valid(): 
                    topictext = topicForm.cleaned_data["topic_name"]
                    topic = LXPModel.Topic.objects.all().filter(topic_name__iexact = topictext)
                    if topic:
                        messages.info(request, 'Topic Name Already Exist')
                        topicForm=ILMSFORM.TopicForm()
                        return render(request,'cto/topic/cto_add_topic.html',{'topicForm':topicForm})                  
                    else:

                        chapter=LXPModel.Video.objects.get(id=request.POST.get('chapterID'))
                        subject=LXPModel.Playlist.objects.get(id=request.POST.get('subjectID'))
                        topic = LXPModel.Topic.objects.create(subject_id = subject.id,chapter_id = chapter.id,topic_name = topictext)
                        topic.save()
                else:
                    print("form is invalid")
            topicForm=ILMSFORM.TopicForm()
            return render(request,'cto/topic/cto_add_topic.html',{'topicForm':topicForm})
    #except:
        return render(request,'lxpapp/404page.html')

@login_required
def cto_update_topic_view(request,pk):
    #try:
        if str(request.session['utype']) == 'cto':
            topic = LXPModel.Topic.objects.get(id=pk)
            topicForm=ILMSFORM.TopicForm(request.POST,instance=topic)
            if request.method=='POST':
                if topicForm.is_valid(): 
                    topictext = topicForm.cleaned_data["topic_name"]
                    chaptertext = topicForm.cleaned_data["chapterID"]
                    subjecttext = topicForm.cleaned_data["subjectID"]
                    topic = LXPModel.Topic.objects.all().filter(topic_name__iexact = topictext).exclude(id=pk)
                    if topic:
                        messages.info(request, 'Topic Name Already Exist')
                        return render(request,'cto/topic/cto_update_topic.html',{'topicForm':topicForm})
                    else:
                        chapter = LXPModel.Video.objects.get(chapter_name=chaptertext)
                        subject = LXPModel.Playlist.objects.get(subject_name=subjecttext)
                        topic = LXPModel.Topic.objects.get(id=pk)
                        topic.topic_name = topictext
                        topic.subject_id = subject.id
                        topic.chapter_id = chapter.id
                        topic.save()
                        c_list = LXPModel.Topic.objects.filter(chapter_id__in=LXPModel.Video.objects.all())
                        return render(request,'cto/topic/cto_view_topic.html',{'topics':c_list})
            return render(request,'cto/topic/cto_update_topic.html',{'topicForm':topicForm,'sub':topic.topic_name})
    #except:
        return render(request,'lxpapp/404page.html')

@login_required
def cto_view_topic_view(request):
    #try:
        if str(request.session['utype']) == 'cto':
            c_list = LXPModel.Topic.objects.filter(chapter_id__in=LXPModel.Video.objects.all(),subject_id__in=LXPModel.Playlist.objects.all())
            return render(request,'cto/topic/cto_view_topic.html',{'topics':c_list})
    #except:
        return render(request,'lxpapp/404page.html')

@login_required
def cto_delete_topic_view(request,pk):
    try:
        if str(request.session['utype']) == 'cto':  
            topic=LXPModel.Topic.objects.get(id=pk)
            topic.delete()
            return HttpResponseRedirect('/cto/topic/cto-view-topic')
        topics = LXPModel.Topic.objects.all()
        return render(request,'cto/topic/cto_view_topic.html',{'topics':topics})
    except:
        return render(request,'lxpapp/404page.html')


def cto_course_view(request):
    try:
        if str(request.session['utype']) == 'cto':
            return render(request,'cto/course/cto_course.html')
    except:
        return render(request,'lxpapp/404page.html')

def cto_add_course_view(request):
    #try:
        from django.forms import modelformset_factory
        if str(request.session['utype']) == 'cto':
            if request.method=='POST':
                det_formset = ILMSFORM.CourseDetFormSet(data=request.POST)
                courseForm=ILMSFORM.CourseForm(request.POST)
                if courseForm.is_valid() : 
                    coursetext = courseForm.cleaned_data["course_name"]
                    course = LXPModel.Course.objects.all().filter(course_name__iexact = coursetext)
                    if course:
                        messages.info(request, 'Course Name Already Exist')
                        courseForm=ILMSFORM.CourseForm()
                        det_formset = ILMSFORM.CourseDetFormSet(queryset=LXPModel.CourseDetails.objects.none())
                        return render(request,'cto/course/cto_add_course.html',{'courseForm':courseForm,'det_formset':det_formset})
                    else:
                        course = courseForm.save(commit=False)
                        course.save()
                        det_formset = ILMSFORM.CourseDetFormSet(data=request.POST)
                        counter = 0
                        for form in det_formset.forms:
                            refid = None
                            subject = None
                            chapter = None
                            topic = None
                            refid = form.data['form-'+str(counter)+'-subject']
                            if refid:
                                subject=LXPModel.Playlist.objects.get(id=refid)
                            refid = form.data['form-'+str(counter)+'-chapter']
                            
                            if refid:
                                chapter=LXPModel.Video.objects.get(id=refid)
                            refid = form.data['form-'+str(counter)+'-topic']
                            if refid:
                                topic=LXPModel.Topic.objects.get(id=refid)
                            if subject and chapter and topic :
                                coursedetails = LXPModel.CourseDetails.objects.create(subject_id = subject.id,chapter_id = chapter.id,topic_id = topic.id,course_id =course.id )
                                coursedetails.save()
                        messages.info(request, 'Course saved')
                else:
                    print("form is invalid")
            courseForm=ILMSFORM.CourseForm()
            det_formset = ILMSFORM.CourseDetFormSet(queryset=LXPModel.CourseDetails.objects.none())
            return render(request,'cto/course/cto_add_course.html',{'courseForm':courseForm,'det_formset':det_formset})
    #except:
        return render(request,'lxpapp/404page.html')

def cto_view_course_view(request):
    #try:
        if str(request.session['utype']) == 'cto':
            c_list = LXPModel.Course.objects.all()
            return render(request,'cto/course/cto_view_course.html',{'courses':c_list})
    #except:
        return render(request,'lxpapp/404page.html')

def cto_view_course_details_view(request,cname):
    #try:
        if str(request.session['utype']) == 'cto':
            c_list = LXPModel.CourseDetails.objects.filter(course_id__in=LXPModel.Course.objects.all().filter(course_name=cname),chapter_id__in=LXPModel.Video.objects.all(),subject_id__in=LXPModel.Playlist.objects.all(),topic_id__in=LXPModel.Topic.objects.all())
            return render(request,'cto/course/cto_view_course_details.html',{'courses':c_list,'cname':cname})
    #except:
        return render(request,'lxpapp/404page.html')

def cto_delete_course_view(request,pk):
    #try:
        if str(request.session['utype']) == 'cto':  
            course=LXPModel.Course.objects.get(id=pk)
            course.delete()
            c_list = LXPModel.Course.objects.all()
            return render(request,'cto/course/cto_view_course.html',{'courses':c_list})
    #except:
        return render(request,'lxpapp/404page.html')

def cto_add_course_by_playlist_view(request):
    #try:
        from django.forms import modelformset_factory
        if str(request.session['utype']) == 'cto':
            if request.method=='POST':
                courseForm=ILMSFORM.CourseForm(request.POST)
                if courseForm.is_valid() : 
                    coursetext = courseForm.cleaned_data["course_name"]
                    course = LXPModel.Course.objects.all().filter(course_name__iexact = coursetext)
                    if course:
                        messages.info(request, 'Course Name Already Exist')
                    else:
                        course = courseForm.save(commit=False)
                        course.save()
                        selectedlist = request.POST.getlist('playlist[]')
                        for PLID in selectedlist:
                            topics =LXPModel.Topic.objects.all().filter(subject_id=PLID)
                            for det in topics:
                                LXPModel.CourseDetails.objects.create(
                                    course_id= course.id,
                                    subject_id= det.subject_id,
                                    chapter_id= det.chapter_id,
                                    topic_id= det.id
                                ).save()
                        messages.info(request, 'Course saved')
                else:
                    print("form is invalid")
            courseForm=ILMSFORM.CourseForm()
            subject=LXPModel.Playlist.objects.all().order_by('name')
            return render(request,'cto/course/cto_add_course_by_playlist.html',{'courseForm':courseForm,'subject':subject})
    #except:
        return render(request,'lxpapp/404page.html')

class CourseList(ListView):
    model = LXPModel.Course

class courseCreate(CreateView):
    model = LXPModel.Course
    fields = ['course_name']


class CDetailsCreate(CreateView):
    model = LXPModel.Course
    fields = ['course_name']
    success_url = reverse_lazy('course-list')

    def get_context_data(self, **kwargs):
        data = super(CDetailsCreate, self).get_context_data(**kwargs)
        if self.request.POST:
            data['cdetails'] = ILMSFORM.CourseDetFormSet(self.request.POST)
        else:
            data['cdetails'] = ILMSFORM.CourseDetFormSet
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
    model = LXPModel.Course
    success_url = '/'
    fields = ['course_name']


class CDetailsUpdate(UpdateView):
    model = LXPModel.Course
    fields = ['course_name']
    success_url = reverse_lazy('course-list')
    def get_context_data(self, **kwargs):
        data = super(CDetailsUpdate, self).get_context_data(**kwargs)
        if self.request.POST:
            data['cdetails'] = ILMSFORM.CourseDetFormSet(self.request.POST, instance=self.object)
        else:
            data['cdetails'] = ILMSFORM.CourseDetFormSet(instance=self.object)
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
    model = LXPModel.Course
    success_url = reverse_lazy('course-list')

@login_required
def cto_print_course_view(request):
    try:
        courses = LXPModel.Course.objects.all()
        return render(request,'cto/course/cto_print_course.html',{'courses':courses})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def cto_print_course_preview_view(request,cname):
    try:
        coursedetails = LXPModel.CourseDetails.objects.filter(course_id__in=LXPModel.Course.objects.all().filter(course_name =cname),chapter_id__in=LXPModel.Video.objects.all(),subject_id__in=LXPModel.Playlist.objects.all(),topic_id__in=LXPModel.Topic.objects.all())
        return render(request,'cto/course/cto_print_course_preview.html',{'coursedetails':coursedetails,'cname':cname})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def cto_passionateskill_view(request):
    try:
        if str(request.session['utype']) == 'cto':
            return render(request,'cto/passionateskill/cto_passionateskill.html')
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def cto_add_passionateskill_view(request):
    try:
        if str(request.session['utype']) == 'cto':
            if request.method=='POST':
                passionateskillForm=ILMSFORM.PassionateSkillForm(request.POST)
                if passionateskillForm.is_valid(): 
                    passionateskilltext = passionateskillForm.cleaned_data["passionateskill_name"]
                    passionateskill = LXPModel.PassionateSkill.objects.all().filter(passionateskill_name__iexact = passionateskilltext)
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
        return render(request,'lxpapp/404page.html')

@login_required
def cto_update_passionateskill_view(request,pk):
    #try:
        if str(request.session['utype']) == 'cto':
            passionateskill = LXPModel.PassionateSkill.objects.get(id=pk)
            passionateskillForm=ILMSFORM.PassionateSkillForm(request.POST,instance=passionateskill)
            if request.method=='POST':
                if passionateskillForm.is_valid(): 
                    passionateskilltext = passionateskillForm.cleaned_data["passionateskill_name"]
                    passionateskill = LXPModel.PassionateSkill.objects.all().filter(passionateskill_name__iexact = passionateskilltext).exclude(id=pk)
                    if passionateskill:
                        messages.info(request, 'PassionateSkill Name Already Exist')
                        return render(request,'cto/passionateskill/cto_update_passionateskill.html',{'passionateskillForm':passionateskillForm})
                    else:
                        passionateskillForm.save()
                        passionateskills = LXPModel.PassionateSkill.objects.all()
                        return render(request,'cto/passionateskill/cto_view_passionateskill.html',{'passionateskills':passionateskills})
            return render(request,'cto/passionateskill/cto_update_passionateskill.html',{'passionateskillForm':passionateskillForm,'sub':passionateskill.passionateskill_name})
    #except:
        return render(request,'lxpapp/404page.html')

@login_required
def cto_view_passionateskill_view(request):
    try:
        if str(request.session['utype']) == 'cto':
            passionateskills = LXPModel.PassionateSkill.objects.all()
            return render(request,'cto/passionateskill/cto_view_passionateskill.html',{'passionateskills':passionateskills})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def cto_delete_passionateskill_view(request,pk):
    try:
        if str(request.session['utype']) == 'cto':  
            passionateskill=LXPModel.PassionateSkill.objects.get(id=pk)
            passionateskill.delete()
            return HttpResponseRedirect('/cto/passionateskill/cto-view-passionateskill')
        passionateskills = LXPModel.PassionateSkill.objects.all()
        return render(request,'cto/passionateskill/cto_view_passionateskill.html',{'passionateskills':passionateskills})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def cto_knownskill_view(request):
    try:
        if str(request.session['utype']) == 'cto':
            return render(request,'cto/knownskill/cto_knownskill.html')
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def cto_add_knownskill_view(request):
    try:
        if str(request.session['utype']) == 'cto':
            if request.method=='POST':
                knownskillForm=ILMSFORM.KnownSkillForm(request.POST)
                if knownskillForm.is_valid(): 
                    knownskilltext = knownskillForm.cleaned_data["knownskill_name"]
                    knownskill = LXPModel.KnownSkill.objects.all().filter(knownskill_name__iexact = knownskilltext)
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
        return render(request,'lxpapp/404page.html')

@login_required
def cto_update_knownskill_view(request,pk):
    #try:
        if str(request.session['utype']) == 'cto':
            knownskill = LXPModel.KnownSkill.objects.get(id=pk)
            knownskillForm=ILMSFORM.KnownSkillForm(request.POST,instance=knownskill)
            if request.method=='POST':
                if knownskillForm.is_valid(): 
                    knownskilltext = knownskillForm.cleaned_data["knownskill_name"]
                    knownskill = LXPModel.KnownSkill.objects.all().filter(knownskill_name__iexact = knownskilltext).exclude(id=pk)
                    if knownskill:
                        messages.info(request, 'KnownSkill Name Already Exist')
                        return render(request,'cto/knownskill/cto_update_knownskill.html',{'knownskillForm':knownskillForm})
                    else:
                        knownskillForm.save()
                        knownskills = LXPModel.KnownSkill.objects.all()
                        return render(request,'cto/knownskill/cto_view_knownskill.html',{'knownskills':knownskills})
            return render(request,'cto/knownskill/cto_update_knownskill.html',{'knownskillForm':knownskillForm,'sub':knownskill.knownskill_name})
    #except:
        return render(request,'lxpapp/404page.html')

@login_required
def cto_view_knownskill_view(request):
    try:
        if str(request.session['utype']) == 'cto':
            knownskills = LXPModel.KnownSkill.objects.all()
            return render(request,'cto/knownskill/cto_view_knownskill.html',{'knownskills':knownskills})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def cto_delete_knownskill_view(request,pk):
    try:
        if str(request.session['utype']) == 'cto':  
            knownskill=LXPModel.KnownSkill.objects.get(id=pk)
            knownskill.delete()
            return HttpResponseRedirect('/cto/knownskill/cto-view-knownskill')
        knownskills = LXPModel.KnownSkill.objects.all()
        return render(request,'cto/knownskill/cto_view_knownskill.html',{'knownskills':knownskills})
    except:
        return render(request,'lxpapp/404page.html')

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
    pllist = LXPModel.Playlist.objects.all().order_by('name')
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
                PL_NAME = ''#LXPModel.Playlist.objects.values('name').filter(playlist_id = PL_ID)
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
    pllist = LXPModel.Playlist.objects.all().order_by('name')
    return render(request,'cto/youtube/cto_sync_youtube.html',{'pllist':pllist})    
######################################################################

@login_required
def cto_sync_youtube_byselected_playlist_start_view(request):
    if request.method=='POST':
        if 'dblist' in request.POST:
            pllist = LXPModel.Playlist.objects.all().order_by('name')
            return render(request,'cto/youtube/cto_sync_youtube.html',{'pllist':pllist})
        elif 'cloudlist' in request.POST:
            pm = PlaylistManager()
            credentials = pm.getCredentials()
            pl =  pm.initializePlaylist(credentials)
            pllist = LXPModel.Playlist.objects.all().order_by('name')
            return render(request,'cto/youtube/cto_sync_youtube.html',{'pllist':pllist})
        elif 'startselected' in request.POST:
            pm = PlaylistManager()
            selectedlist = request.POST.getlist('playlist[]')
            maxcount = selectedlist.__len__()
            plcount = 1
            credentials = pm.getCredentials()
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
    return render(request,'cto/cto_dashboard.html',context=dict)

@login_required
def get_message_from_httperror(e):
    return e.error_details[0]['message']


def courses(request):
    if request.method=='POST':
        course = request.POST.getlist('course')
        modules = request.POST.getlist('modules')
        for x in course:
            course = x
        for x in modules:
            modules = x
        print(course)
        print(modules)
    courses = LXPModel.Playlist.objects.all()
    context = {'courses': courses}
    return render(request, 'cto/university.html', context)

@login_required
def modules(request):
    course = request.GET.get('course')
    modules = LXPModel.Video.objects.all().filter(id__in = LXPModel.PlaylistItem.objects.all().filter( playlist_id=course))
    context = {'modules': modules}
    return render(request, 'cto/modules.html', context)




