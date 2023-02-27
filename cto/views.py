import os
import google_auth_oauthlib.flow
scopes = ["https://www.googleapis.com/auth/youtube.readonly"]
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from lxpapp import models as LXPModel
from lxpapp import forms as LXPFORM
from youtubemanager import PlaylistManager
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from django.template import loader
from django.http import HttpResponseRedirect
from django.views.generic import ListView, CreateView, UpdateView
from django.shortcuts import (HttpResponse, HttpResponseRedirect,
                              get_object_or_404, redirect, render)
from django.urls import reverse

@login_required
def ctoclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'cto/ctoclick.html')

@login_required    
def cto_dashboard_view(request):
    try:
        if str(request.session['utype']) == 'cto':
            dict={
            'total_course':0,
            'total_exam':0,
            'total_shortCourse':0,
            'total_question':0,
            'total_learner':0
            }
        return render(request,'cto/cto_dashboard.html',context=dict)
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
                passionateskillForm=LXPFORM.PassionateSkillForm(request.POST)
                if passionateskillForm.is_valid(): 
                    passionateskilltext = passionateskillForm.cleaned_data["passionateskill_name"]
                    passionateskill = LXPModel.PassionateSkill.objects.all().filter(passionateskill_name__iexact = passionateskilltext)
                    if passionateskill:
                        messages.info(request, 'PassionateSkill Name Already Exist')
                        passionateskillForm=LXPFORM.PassionateSkillForm()
                        return render(request,'cto/passionateskill/cto_add_passionateskill.html',{'passionateskillForm':passionateskillForm})                  
                    else:
                        passionateskillForm.save()
                else:
                    print("form is invalid")
            passionateskillForm=LXPFORM.PassionateSkillForm()
            return render(request,'cto/passionateskill/cto_add_passionateskill.html',{'passionateskillForm':passionateskillForm})
            #return HttpResponseRedirect('/cto/cto-add-passionateskill')
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def cto_update_passionateskill_view(request,pk):
    try:
        if str(request.session['utype']) == 'cto':
            passionateskill = LXPModel.PassionateSkill.objects.get(id=pk)
            passionateskillForm=LXPFORM.PassionateSkillForm(request.POST,instance=passionateskill)
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
    except:
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
                knownskillForm=LXPFORM.KnownSkillForm(request.POST)
                if knownskillForm.is_valid(): 
                    knownskilltext = knownskillForm.cleaned_data["knownskill_name"]
                    knownskill = LXPModel.KnownSkill.objects.all().filter(knownskill_name__iexact = knownskilltext)
                    if knownskill:
                        messages.info(request, 'KnownSkill Name Already Exist')
                        knownskillForm=LXPFORM.KnownSkillForm()
                        return render(request,'cto/knownskill/cto_add_knownskill.html',{'knownskillForm':knownskillForm})                  
                    else:
                        knownskillForm.save()
                else:
                    print("form is invalid")
            knownskillForm=LXPFORM.KnownSkillForm()
            return render(request,'cto/knownskill/cto_add_knownskill.html',{'knownskillForm':knownskillForm})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def cto_update_knownskill_view(request,pk):
    try:
        if str(request.session['utype']) == 'cto':
            knownskill = LXPModel.KnownSkill.objects.get(id=pk)
            knownskillForm=LXPFORM.KnownSkillForm(request.POST,instance=knownskill)
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
    except:
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
def cto_subject_view(request):
    try:
        if str(request.session['utype']) == 'cto':
            return render(request,'cto/subject/cto_subject.html')
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def cto_add_subject_view(request):
    form = LXPFORM.SubjectForm(request.POST or None)
    

    context = {
        'form': form,
        'page_title': 'Add Subject'
    }
    if request.method == 'POST':
        if form.is_valid():
            name = form.cleaned_data.get('subject_name')
            subject = LXPModel.Subject.objects.all().filter(subject_name__iexact = name)
            if subject:
                messages.info(request, 'Subject Name Already Exist')
                return redirect(reverse('cto-add-subject'))
            try:
                subject = LXPModel.Subject.objects.create(
                                            subject_name = name)
                subject.save()
                messages.success(request, "Successfully Updated")
                return redirect(reverse('cto-add-subject'))
            except Exception as e:
                messages.error(request, "Could Not Add " + str(e))
        else:
            messages.error(request, "Fill Form Properly")
    return render(request, 'cto/subject/add_edit_subject.html', context)

@login_required
def cto_update_subject_view(request, pk):
    instance = get_object_or_404(LXPModel.Subject, id=pk)
    form = LXPFORM.SubjectForm(request.POST or None, instance=instance)
    context = {
        'form': form,
        'subject_id': pk,
        'page_title': 'Edit Subject'
    }
    if request.method == 'POST':
        if form.is_valid():
            name = form.cleaned_data.get('subject_name')
            subject = LXPModel.Subject.objects.all().filter(subject_name__iexact = name).exclude(id=pk)
            if subject:
                messages.info(request, 'Subject Name Already Exist')
                return redirect(reverse('cto-update-subject', args=[pk]))
            try:
                subject = LXPModel.Subject.objects.get(id=pk)
                subject.subject_name = name
                subject.save()
                messages.success(request, "Successfully Updated")
                return redirect(reverse('cto-update-subject', args=[pk]))
            except Exception as e:
                messages.error(request, "Could Not Add " + str(e))
        else:
            messages.error(request, "Fill Form Properly")
    return render(request, 'cto/subject/add_edit_subject.html', context)


@login_required
def cto_view_subject_view(request):
    try:
        if str(request.session['utype']) == 'cto':
            subjects = LXPModel.Subject.objects.all()
            return render(request,'cto/subject/cto_view_subject.html',{'subjects':subjects})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def cto_delete_subject_view(request,pk):
    try:
        if str(request.session['utype']) == 'cto':  
            subject=LXPModel.Subject.objects.get(id=pk)
            subject.delete()
            return HttpResponseRedirect('/cto/subject/cto-view-subject')
        subjects = LXPModel.Subject.objects.all()
        return render(request,'cto/subject/cto_view_subject.html',{'subjects':subjects})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def cto_upload_subject_details_csv_view(request):
    if request.method=='POST':
        file=request.FILES["select_file"]
        csv_file = request.FILES["select_file"]
        file_data = csv_file.read().decode("utf-8")		
        lines = file_data.split("\n")
        oldsub =''
        oldmod=''
        oldchap=''
        oldtop=''
        subid =0
        modid=0
        chapid=0
        topid=0
        no = 0
        for line in lines:						
            no = no + 1
            if no > 1:
                fields = line.split(",")
                if fields[0] != oldsub:
                    oldsub = fields[0]
                    sub = LXPModel.Subject.objects.all().filter(subject_name__exact = oldsub )
                    if not sub:
                        sub = LXPModel.Subject.objects.create(subject_name = oldsub )
                        sub.save()
                        subid=sub.id
                    else:
                        for x in sub:
                          subid=x.id  
                if fields[1] != oldmod:
                    oldmod = fields[1] 
                    mod = LXPModel.Module.objects.all().filter(module_name__exact = oldmod,subject_id=subid)
                    if not mod:
                        mod = LXPModel.Module.objects.create(module_name = oldmod,subject_id=subid)
                        mod.save()
                        modid=mod.id
                    else:
                        for x in mod:
                          modid=x.id 
                if fields[2] != oldchap:
                    oldchap = fields[2] 
                    chap = LXPModel.Chapter.objects.all().filter(chapter_name__exact = oldchap,module_id=modid)
                    if not chap:
                        chap = LXPModel.Chapter.objects.create(chapter_name = oldchap,module_id=modid)
                        chap.save()
                        chapid=chap.id
                    else:
                       for x in chap:
                          chapid=x.id 
                if fields[3] != oldtop:
                    oldtop = fields[3] 
                    top = LXPModel.Topic.objects.all().filter(topic_name__exact = oldtop,chapter_id=chapid)
                    if not top:
                        top = LXPModel.Topic.objects.create(topic_name = oldtop,chapter_id=chapid)
                        top.save()
                        topid=top.id

    return render(request,'cto/subject/cto_upload_subject_details_csv.html')

@login_required
def cto_module_view(request):
    try:
        if str(request.session['utype']) == 'cto':
            return render(request,'cto/module/cto_module.html')
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def cto_add_module_view(request):
    form = LXPFORM.ModuleForm(request.POST or None)
    context = {
        'form': form,
        'page_title': 'Add Module'
    }
    if request.method == 'POST':
        if form.is_valid():
            name = form.cleaned_data.get('module_name')
            subject = form.cleaned_data.get('subject').pk
            module = LXPModel.Module.objects.all().filter(module_name__iexact = name)
            if module:
                messages.info(request, 'Module Name Already Exist')
                return redirect(reverse('cto-add-module'))
            try:
                module = LXPModel.Module.objects.create(
                                            module_name = name,
                                            subject_id = subject)
                module.save()
                messages.success(request, "Successfully Updated")
                return redirect(reverse('cto-add-module'))
            except Exception as e:
                messages.error(request, "Could Not Add " + str(e))
        else:
            messages.error(request, "Fill Form Properly")
    return render(request, 'cto/module/add_edit_module.html', context)

@login_required
def cto_update_module_view(request, pk):
    instance = get_object_or_404(LXPModel.Module, id=pk)
    form = LXPFORM.ModuleForm(request.POST or None, instance=instance)
    context = {
        'form': form,
        'module_id': pk,
        'page_title': 'Edit Module'
    }
    if request.method == 'POST':
        if form.is_valid():
            name = form.cleaned_data.get('module_name')
            subject = form.cleaned_data.get('subject').pk
            module = LXPModel.Module.objects.all().filter(module_name__iexact = name).exclude(id=pk)
            if module:
                messages.info(request, 'Module Name Already Exist')
                return redirect(reverse('cto-update-module', args=[pk]))
            try:
                module = LXPModel.Module.objects.get(id=pk)
                module.module_name = name
                module.subject_id = subject
                module.save()
                messages.success(request, "Successfully Updated")
                return redirect(reverse('cto-update-module', args=[pk]))
            except Exception as e:
                messages.error(request, "Could Not Add " + str(e))
        else:
            messages.error(request, "Fill Form Properly")
    return render(request, 'cto/module/add_edit_module.html', context)

@login_required
def cto_view_module_view(request):
    try:
        if str(request.session['utype']) == 'cto':
            c_list = LXPModel.Module.objects.all()
            return render(request,'cto/module/cto_view_module.html',{'modules':c_list})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def cto_delete_module_view(request,pk):
    try:
        if str(request.session['utype']) == 'cto':  
            module=LXPModel.Module.objects.get(id=pk)
            module.delete()
            return HttpResponseRedirect('/cto/module/cto-view-module')
        modules = LXPModel.Module.objects.all()
        return render(request,'cto/module/cto_view_module.html',{'modules':modules})
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
    form = LXPFORM.ChapterForm(request.POST or None)
    context = {
        'form': form,
        'page_title': 'Add Chapter'
    }
    if request.method == 'POST':
        if form.is_valid():
            name = form.cleaned_data.get('chapter_name')
            module = form.cleaned_data.get('module').pk
            chapter = LXPModel.Chapter.objects.all().filter(chapter_name__iexact = name)
            if chapter:
                messages.info(request, 'Chapter Name Already Exist')
                return redirect(reverse('cto-add-chapter'))
            try:
                chapter = LXPModel.Chapter.objects.create(
                                            chapter_name = name,
                                            module_id = module)
                chapter.save()
                messages.success(request, "Successfully Updated")
                return redirect(reverse('cto-add-chapter'))
            except Exception as e:
                messages.error(request, "Could Not Add " + str(e))
        else:
            messages.error(request, "Fill Form Properly")
    return render(request, 'cto/chapter/add_edit_chapter.html', context)

@login_required
def cto_update_chapter_view(request, pk):
    instance = get_object_or_404(LXPModel.Chapter, id=pk)
    form = LXPFORM.ChapterForm(request.POST or None, instance=instance)
    context = {
        'form': form,
        'chapter_id': pk,
        'page_title': 'Edit Chapter'
    }
    if request.method == 'POST':
        if form.is_valid():
            name = form.cleaned_data.get('chapter_name')
            module = form.cleaned_data.get('module').pk
            chapter = LXPModel.Chapter.objects.all().filter(chapter_name__iexact = name).exclude(id=pk)
            if chapter:
                messages.info(request, 'Chapter Name Already Exist')
                return redirect(reverse('cto-update-chapter', args=[pk]))
            try:
                chapter = LXPModel.Chapter.objects.get(id=pk)
                chapter.chapter_name = name
                chapter.module_id = module
                chapter.save()
                messages.success(request, "Successfully Updated")
                return redirect(reverse('cto-update-chapter', args=[pk]))
            except Exception as e:
                messages.error(request, "Could Not Add " + str(e))
        else:
            messages.error(request, "Fill Form Properly")
    return render(request, 'cto/chapter/add_edit_chapter.html', context)

@login_required
def cto_view_chapter_view(request):
    try:
        if str(request.session['utype']) == 'cto':
            c_list = LXPModel.Chapter.objects.all()
            return render(request,'cto/chapter/cto_view_chapter.html',{'chapters':c_list})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def cto_delete_chapter_view(request,pk):
    try:
        if str(request.session['utype']) == 'cto':  
            chapter=LXPModel.Chapter.objects.get(id=pk)
            chapter.delete()
            return HttpResponseRedirect('/cto/chapter/cto-view-chapter')
        chapters = LXPModel.Chapter.objects.all()
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
    form = LXPFORM.TopicForm(request.POST or None)
    context = {
        'form': form,
        'page_title': 'Add Topic'
    }
    if request.method == 'POST':
        if form.is_valid():
            name = form.cleaned_data.get('topic_name')
            chapter = form.cleaned_data.get('chapter').pk
            topic = LXPModel.Topic.objects.all().filter(topic_name__iexact = name)
            if topic:
                messages.info(request, 'Topic Name Already Exist')
                return redirect(reverse('cto-add-topic'))
            try:
                topic = LXPModel.Topic.objects.create(
                                            topic_name = name,
                                            chapter_id = chapter)
                topic.save()
                messages.success(request, "Successfully Updated")
                return redirect(reverse('cto-add-topic'))
            except Exception as e:
                messages.error(request, "Could Not Add " + str(e))
        else:
            messages.error(request, "Fill Form Properly")
    return render(request, 'cto/topic/add_edit_topic.html', context)

@login_required
def cto_update_topic_view(request, pk):
    instance = get_object_or_404(LXPModel.Topic, id=pk)
    form = LXPFORM.TopicForm(request.POST or None, instance=instance)
    context = {
        'form': form,
        'topic_id': pk,
        'page_title': 'Edit Topic'
    }
    if request.method == 'POST':
        if form.is_valid():
            name = form.cleaned_data.get('topic_name')
            chapter = form.cleaned_data.get('chapter').pk
            topic = LXPModel.Topic.objects.all().filter(topic_name__iexact = name).exclude(id=pk)
            if topic:
                messages.info(request, 'Topic Name Already Exist')
                return redirect(reverse('cto-update-topic', args=[pk]))
            try:
                topic = LXPModel.Topic.objects.get(id=pk)
                topic.topic_name = name
                topic.chapter_id = chapter
                topic.save()
                messages.success(request, "Successfully Updated")
                return redirect(reverse('cto-update-topic', args=[pk]))
            except Exception as e:
                messages.error(request, "Could Not Add " + str(e))
        else:
            messages.error(request, "Fill Form Properly")
    return render(request, 'cto/topic/add_edit_topic.html', context)

@login_required
def cto_view_topic_view(request):
    try:
        if str(request.session['utype']) == 'cto':
            c_list = LXPModel.Topic.objects.all()
            return render(request,'cto/topic/cto_view_topic.html',{'topics':c_list})
    except:
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

@login_required
def cto_course_view(request):
    try:
        if str(request.session['utype']) == 'cto':
            return render(request,'cto/course/cto_course.html')
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def cto_add_course_view(request):
    #try:
        if str(request.session['utype']) == 'cto':
            if request.method=='POST':
                courseForm=LXPFORM.CourseForm(request.POST)
                coursetext = request.POST.get('course_name')
                course = LXPModel.Course.objects.all().filter(course_name__iexact = coursetext)
                if course:
                    messages.info(request, 'Course Name Already Exist')
                    courseForm=LXPFORM.CourseForm()
                    return render(request,'cto/course/cto_add_course.html',{'courseForm':courseForm})                  
                else:
                    course_name = request.POST.get('course_name')
                    course = LXPModel.Course.objects.create(course_name = course_name)
                    course.save()
                    import json
                    json_data = json.loads(request.POST.get('myvalue'))
                    for cx in json_data:
                        a=json_data[cx]['subject']
                        b=json_data[cx]['module']
                        c=json_data[cx]['chapter']
                        d=json_data[cx]['topic']
                        x = a.split("-")
                        subid = x[0]
                        x = b.split("-")
                        modid = x[0]
                        x = c.split("-")
                        chapid = x[0]
                        x = d.split("-")
                        topid = x[0]
                        coursedet = LXPModel.CourseDetails.objects.create(
                                course_id = course.id,
                                subject_id = subid,
                                module_id = modid,
                                chapter_id = chapid,
                                topic_id = topid
                                )
                        coursedet.save()
            courseForm=LXPFORM.CourseForm()
            return render(request,'cto/course/cto_add_course.html',{'courseForm':courseForm})
    #except:
        return render(request,'lxpapp/404page.html')

@login_required
def cto_update_course_view(request,coursename,pk):
    #try:
        if str(request.session['utype']) == 'cto':
            course = LXPModel.Course.objects.get(id=pk)
            if request.method=='POST':
                courseForm=LXPFORM.CourseForm(request.POST,instance=course)
                if courseForm.is_valid(): 
                    coursetext = courseForm.cleaned_data["course_name"]
                    course = LXPModel.Course.objects.all().filter(course_name__iexact = coursetext).exclude(id=pk)
                    if course:
                        messages.info(request, 'Course Name Already Exist')
                        return render(request,'cto/course/cto_update_course.html',{'courseForm':courseForm})
                    else:
                        courseForm.save()
                        courses = LXPModel.Course.objects.all()
                        return render(request,'cto/course/cto_view_course.html',{'courses':courses})
            courseForm = LXPFORM.CourseForm()
            courses = LXPModel.Course.objects.raw('SELECT 1 as id,  lxpapp_subject.subject_name,  lxpapp_module.module_name,  lxpapp_chapter.chapter_name,  lxpapp_topic.topic_name FROM  lxpapp_coursedetails  INNER JOIN lxpapp_course ON (lxpapp_coursedetails.course_id = lxpapp_course.id)  INNER JOIN lxpapp_subject ON (lxpapp_coursedetails.subject_id = lxpapp_subject.id)  INNER JOIN lxpapp_module ON (lxpapp_coursedetails.module_id = lxpapp_module.id)  INNER JOIN lxpapp_chapter ON (lxpapp_coursedetails.chapter_id = lxpapp_chapter.id)  INNER JOIN lxpapp_topic ON (lxpapp_coursedetails.topic_id = lxpapp_topic.id) WHERE lxpapp_coursedetails.course_id = ' + str(pk) + ' ORDER BY lxpapp_subject.subject_name,  lxpapp_module.module_name,  lxpapp_chapter.chapter_name,  lxpapp_topic.topic_name')
            return render(request,'cto/course/cto_update_course.html',{'courses':courses,'courseForm':courseForm,'coursename':coursename})
    #except:
        return render(request,'lxpapp/404page.html')

@login_required
def cto_view_course_view(request):
    #try:
        if str(request.session['utype']) == 'cto':
            courses = LXPModel.Course.objects.all()
            return render(request,'cto/course/cto_view_course.html',{'courses':courses})
    #except:
        return render(request,'lxpapp/404page.html')

@login_required
def cto_view_course_details_view(request,coursename,pk):
    #try:
        if str(request.session['utype']) == 'cto':
            courses = LXPModel.Course.objects.raw('SELECT 1 as id,  lxpapp_subject.subject_name,  lxpapp_module.module_name,  lxpapp_chapter.chapter_name,  lxpapp_topic.topic_name FROM  lxpapp_coursedetails  INNER JOIN lxpapp_course ON (lxpapp_coursedetails.course_id = lxpapp_course.id)  INNER JOIN lxpapp_subject ON (lxpapp_coursedetails.subject_id = lxpapp_subject.id)  INNER JOIN lxpapp_module ON (lxpapp_coursedetails.module_id = lxpapp_module.id)  INNER JOIN lxpapp_chapter ON (lxpapp_coursedetails.chapter_id = lxpapp_chapter.id)  INNER JOIN lxpapp_topic ON (lxpapp_coursedetails.topic_id = lxpapp_topic.id) WHERE lxpapp_coursedetails.course_id = ' + str(pk) + ' ORDER BY lxpapp_subject.subject_name,  lxpapp_module.module_name,  lxpapp_chapter.chapter_name,  lxpapp_topic.topic_name')
            return render(request,'cto/course/cto_view_course_details.html',{'courses':courses,'coursename':coursename})
    #except:
        return render(request,'lxpapp/404page.html')

@login_required
def cto_delete_course_view(request,pk):
    #try:
        if str(request.session['utype']) == 'cto':
            coursedet=LXPModel.CourseDetails.objects.get(course_id=pk)
            coursedet.delete()  
            course=LXPModel.Course.objects.get(id=pk)
            course.delete()
        courses = LXPModel.Course.objects.all()
        return render(request,'cto/course/cto_view_course.html',{'courses':courses})
    #except:
        return render(request,'lxpapp/404page.html')

@login_required
def cto_upload_course_details_csv_view(request):
    if request.method=='POST':
        coursetext=request.POST.get('course_name')
        course = LXPModel.Course.objects.all().filter(course_name__iexact = coursetext)
        if course:
            messages.info(request, 'Course Name Already Exist')
        else:
            course = LXPModel.Course.objects.create(course_name = coursetext)
            course.save()     
            csv_file = request.FILES["select_file"]
            file_data = csv_file.read().decode("utf-8")		
            lines = file_data.split("\n")
            oldsub =''
            oldmod=''
            oldchap=''
            oldtop=''
            subid =0
            modid=0
            chapid=0
            topid=0
            no = 0
            for line in lines:						
                no = no + 1
                if no > 1:
                    fields = line.split(",")
                    if fields[0] != oldsub:
                        oldsub = fields[0]
                        sub = LXPModel.Subject.objects.all().filter(subject_name__exact = oldsub )
                        if not sub:
                            sub = LXPModel.Subject.objects.create(subject_name = oldsub )
                            sub.save()
                            subid=sub.id
                        else:
                            for x in sub:
                                subid=x.id  
                    if fields[1] != oldmod:
                        oldmod = fields[1] 
                        mod = LXPModel.Module.objects.all().filter(module_name__exact = oldmod,subject_id=subid)
                        if not mod:
                            mod = LXPModel.Module.objects.create(module_name = oldmod,subject_id=subid)
                            mod.save()
                            modid=mod.id
                        else:
                            for x in mod:
                                modid=x.id 
                    if fields[2] != oldchap:
                        oldchap = fields[2] 
                        chap = LXPModel.Chapter.objects.all().filter(chapter_name__exact = oldchap,module_id=modid)
                        if not chap:
                            chap = LXPModel.Chapter.objects.create(chapter_name = oldchap,module_id=modid)
                            chap.save()
                            chapid=chap.id
                        else:
                            for x in chap:
                                chapid=x.id 
                    if fields[3] != oldtop:
                        oldtop = fields[3] 
                        top = LXPModel.Topic.objects.all().filter(topic_name__exact = oldtop,chapter_id=chapid)
                        if not top:
                            top = LXPModel.Topic.objects.create(topic_name = oldtop,chapter_id=chapid)
                            top.save()
                            topid1=top.id 
                        else:
                            for x in top:
                                topid1=x.id 
                    coursedet = LXPModel.CourseDetails.objects.create(
                                course_id =course.id,
                                subject_id=subid,
                                module_id=modid,
                                chapter_id=chapid,
                                topic_id=topid1
                                )
                    coursedet.save()
    return render(request,'cto/course/cto_upload_course_details_csv.html')

@login_required
def cto_courseset_view(request):
    try:
        if str(request.session['utype']) == 'cto':
            return render(request,'cto/courseset/cto_courseset.html')
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def cto_add_courseset_view(request):
    #try:
        if str(request.session['utype']) == 'cto':

            course = LXPModel.CourseDetails.objects.all().filter(
                    course_id__in = LXPModel.Course.objects.all(),
                    subject_id__in = LXPModel.Subject.objects.all(),
                    module_id__in = LXPModel.Module.objects.all(),
                    chapter_id__in = LXPModel.Chapter.objects.all(),
                    topic_id__in = LXPModel.Topic.objects.all()
                    )
            import json
            
            data = list(course.values())
            result = {}
            for item in data:
                current_dict = result
                for key in list(item.keys())[:-1]:
                    current_dict = current_dict.setdefault(key, {})
                current_dict[list(item.keys())[-1]] = item[list(item.keys())[-1]]

            # Convert the dictionary to a JSON object
            json_data = json.dumps(result, indent=4)
            json_data = json_data.replace('\n','')
           # course = LXPModel.Course.objects.raw(' SELECT 1 as id,  ROW_NUMBER () OVER (        PARTITION BY lxpapp_course.course_name    ) CRow , lxpapp_course.course_name ,    ROW_NUMBER () OVER (        PARTITION BY lxpapp_subject.subject_name    ) SRow ,  lxpapp_subject.subject_name,       ROW_NUMBER () OVER (        PARTITION BY lxpapp_module.module_name    ) MRow ,  lxpapp_module.module_name,         ROW_NUMBER () OVER (        PARTITION BY lxpapp_chapter.chapter_name    ) CHRow ,  lxpapp_chapter.chapter_name,     ROW_NUMBER () OVER (        PARTITION BY lxpapp_topic.topic_name    ) TRow ,  lxpapp_topic.topic_name FROM  lxpapp_coursedetails  INNER JOIN lxpapp_course ON (lxpapp_coursedetails.course_id = lxpapp_course.id)  INNER JOIN lxpapp_subject ON (lxpapp_coursedetails.subject_id = lxpapp_subject.id)  INNER JOIN lxpapp_module ON (lxpapp_coursedetails.module_id = lxpapp_module.id)  INNER JOIN lxpapp_chapter ON (lxpapp_coursedetails.chapter_id = lxpapp_chapter.id)  INNER JOIN lxpapp_topic ON (lxpapp_coursedetails.topic_id = lxpapp_topic.id) ORDER BY  lxpapp_subject.subject_name,  lxpapp_module.module_name,  lxpapp_chapter.chapter_name,  lxpapp_topic.topic_name')
           # course = LXPModel.CourseSetDetails.objects.raw('SELECT   1 as id,lxpapp_course.course_name,  lxpapp_subject.subject_name,  lxpapp_module.module_name,  lxpapp_chapter.chapter_name,  lxpapp_topic.topic_name   FROM  lxpapp_coursedetails  INNER JOIN lxpapp_course ON (lxpapp_coursedetails.course_id = lxpapp_course.id)  INNER JOIN lxpapp_subject ON (lxpapp_coursedetails.subject_id = lxpapp_subject.id)  INNER JOIN lxpapp_module ON (lxpapp_coursedetails.module_id = lxpapp_module.id)  INNER JOIN lxpapp_chapter ON (lxpapp_coursedetails.chapter_id = lxpapp_chapter.id)  INNER JOIN lxpapp_topic ON (lxpapp_coursedetails.topic_id = lxpapp_topic.id) ORDER BY  lxpapp_subject.subject_name,  lxpapp_module.module_name,  lxpapp_chapter.chapter_name,  lxpapp_topic.topic_name')
            courses = LXPModel.Course.objects.raw('SELECT   1 as id,lxpapp_course.course_name,  lxpapp_subject.subject_name,  lxpapp_module.module_name,  lxpapp_chapter.chapter_name,  lxpapp_topic.topic_name   FROM  lxpapp_coursedetails  INNER JOIN lxpapp_course ON (lxpapp_coursedetails.course_id = lxpapp_course.id)  INNER JOIN lxpapp_subject ON (lxpapp_coursedetails.subject_id = lxpapp_subject.id)  INNER JOIN lxpapp_module ON (lxpapp_coursedetails.module_id = lxpapp_module.id)  INNER JOIN lxpapp_chapter ON (lxpapp_coursedetails.chapter_id = lxpapp_chapter.id)  INNER JOIN lxpapp_topic ON (lxpapp_coursedetails.topic_id = lxpapp_topic.id) ORDER BY  lxpapp_subject.subject_name,  lxpapp_module.module_name,  lxpapp_chapter.chapter_name,  lxpapp_topic.topic_name')
            from django.core.serializers import serialize
            people = serialize("json", course)
            import collections
            # data = serialize("json", courses)
            objects_list = []
            for row in courses:
                d = collections.OrderedDict()
                d["course_name"] = row.course_name
                d["subject_name"] = row.subject_name
                d["module_name"] = row.module_name
                d["chapter_name"] = row.chapter_name
                d["topic_name"] = row.topic_name
                objects_list.append(d)
            j = json.dumps(objects_list)
            

            if request.method=='POST':
                coursesetForm=LXPFORM.CourseSetForm(request.POST)
                coursesettext = request.POST.get('courseset_name')
                courseset = LXPModel.CourseSet.objects.all().filter(courseset_name__iexact = coursesettext)
                if courseset:
                    messages.info(request, 'CourseSet Name Already Exist')
                    coursesetForm=LXPFORM.CourseSetForm()
                    return render(request,'cto/courseset/cto_add_courseset.html',{'coursesetForm':coursesetForm})                  
                else:
                    courseset_name = request.POST.get('courseset_name')
                    courseset = LXPModel.CourseSet.objects.create(courseset_name = courseset_name)
                    courseset.save()
                    import json
                    json_data = json.loads(request.POST.get('myvalue'))
                    for cx in json_data:
                        a=json_data[cx]['subject']
                        b=json_data[cx]['module']
                        c=json_data[cx]['chapter']
                        d=json_data[cx]['topic']
                        x = a.split("-")
                        subid = x[0]
                        x = b.split("-")
                        modid = x[0]
                        x = c.split("-")
                        chapid = x[0]
                        x = d.split("-")
                        topid = x[0]
                        coursesetdet = LXPModel.CourseSetDetails.objects.create(
                                courseset_id = courseset.id,
                                subject_id = subid,
                                module_id = modid,
                                chapter_id = chapid,
                                topic_id = topid
                                )
                        coursesetdet.save()
            coursesetForm=LXPFORM.CourseSetForm()
            return render(request,'cto/courseset/cto_add_courseset.html',{'coursesetForm':coursesetForm,'course':course})
    #except:
        return render(request,'lxpapp/404page.html')

@login_required
def cto_update_courseset_view(request,coursesetname,pk):
    #try:
        if str(request.session['utype']) == 'cto':
            courseset = LXPModel.CourseSet.objects.get(id=pk)
            if request.method=='POST':
                coursesetForm=LXPFORM.CourseSetForm(request.POST,instance=courseset)
                if coursesetForm.is_valid(): 
                    coursesettext = coursesetForm.cleaned_data["courseset_name"]
                    courseset = LXPModel.CourseSet.objects.all().filter(courseset_name__iexact = coursesettext).exclude(id=pk)
                    if courseset:
                        messages.info(request, 'CourseSet Name Already Exist')
                        return render(request,'cto/courseset/cto_update_courseset.html',{'coursesetForm':coursesetForm})
                    else:
                        coursesetForm.save()
                        coursesets = LXPModel.CourseSet.objects.all()
                        return render(request,'cto/courseset/cto_view_courseset.html',{'coursesets':coursesets})
            coursesetForm = LXPFORM.CourseSetForm()
            coursesets = LXPModel.CourseSet.objects.raw('SELECT 1 as id,  lxpapp_subject.subject_name,  lxpapp_module.module_name,  lxpapp_chapter.chapter_name,  lxpapp_topic.topic_name FROM  lxpapp_coursesetdetails  INNER JOIN lxpapp_courseset ON (lxpapp_coursesetdetails.courseset_id = lxpapp_courseset.id)  INNER JOIN lxpapp_subject ON (lxpapp_coursesetdetails.subject_id = lxpapp_subject.id)  INNER JOIN lxpapp_module ON (lxpapp_coursesetdetails.module_id = lxpapp_module.id)  INNER JOIN lxpapp_chapter ON (lxpapp_coursesetdetails.chapter_id = lxpapp_chapter.id)  INNER JOIN lxpapp_topic ON (lxpapp_coursesetdetails.topic_id = lxpapp_topic.id) WHERE lxpapp_coursesetdetails.courseset_id = ' + str(pk) + ' ORDER BY lxpapp_subject.subject_name,  lxpapp_module.module_name,  lxpapp_chapter.chapter_name,  lxpapp_topic.topic_name')
            return render(request,'cto/courseset/cto_update_courseset.html',{'coursesets':coursesets,'coursesetForm':coursesetForm,'coursesetname':coursesetname})
    #except:
        return render(request,'lxpapp/404page.html')

@login_required
def cto_view_courseset_view(request):
    #try:
        if str(request.session['utype']) == 'cto':
            coursesets = LXPModel.CourseSet.objects.all()
            return render(request,'cto/courseset/cto_view_courseset.html',{'coursesets':coursesets})
    #except:
        return render(request,'lxpapp/404page.html')

@login_required
def cto_view_courseset_details_view(request,coursesetname,pk):
    #try:
        if str(request.session['utype']) == 'cto':
            coursesets = LXPModel.CourseSet.objects.raw('SELECT 1 as id,  lxpapp_subject.subject_name,  lxpapp_module.module_name,  lxpapp_chapter.chapter_name,  lxpapp_topic.topic_name FROM  lxpapp_coursesetdetails  INNER JOIN lxpapp_courseset ON (lxpapp_coursesetdetails.courseset_id = lxpapp_courseset.id)  INNER JOIN lxpapp_subject ON (lxpapp_coursesetdetails.subject_id = lxpapp_subject.id)  INNER JOIN lxpapp_module ON (lxpapp_coursesetdetails.module_id = lxpapp_module.id)  INNER JOIN lxpapp_chapter ON (lxpapp_coursesetdetails.chapter_id = lxpapp_chapter.id)  INNER JOIN lxpapp_topic ON (lxpapp_coursesetdetails.topic_id = lxpapp_topic.id) WHERE lxpapp_coursesetdetails.courseset_id = ' + str(pk) + ' ORDER BY lxpapp_subject.subject_name,  lxpapp_module.module_name,  lxpapp_chapter.chapter_name,  lxpapp_topic.topic_name')
            return render(request,'cto/courseset/cto_view_courseset_details.html',{'coursesets':coursesets,'coursesetname':coursesetname})
    #except:
        return render(request,'lxpapp/404page.html')

@login_required
def cto_delete_courseset_view(request,pk):
    #try:
        if str(request.session['utype']) == 'cto':
            coursesetdet=LXPModel.CourseSetDetails.objects.get(courseset_id=pk)
            coursesetdet.delete()  
            courseset=LXPModel.CourseSet.objects.get(id=pk)
            courseset.delete()
        coursesets = LXPModel.CourseSet.objects.all()
        return render(request,'cto/courseset/cto_view_courseset.html',{'coursesets':coursesets})
    #except:
        return render(request,'lxpapp/404page.html')

@login_required
def cto_upload_courseset_details_csv_view(request):
    if request.method=='POST':
        coursesettext=request.POST.get('courseset_name')
        courseset = LXPModel.CourseSet.objects.all().filter(courseset_name__iexact = coursesettext)
        if courseset:
            messages.info(request, 'CourseSet Name Already Exist')
        else:
            courseset = LXPModel.CourseSet.objects.create(courseset_name = coursesettext)
            courseset.save()     
            csv_file = request.FILES["select_file"]
            file_data = csv_file.read().decode("utf-8")		
            lines = file_data.split("\n")
            oldsub =''
            oldmod=''
            oldchap=''
            oldtop=''
            subid =0
            modid=0
            chapid=0
            topid=0
            no = 0
            for line in lines:						
                no = no + 1
                if no > 1:
                    fields = line.split(",")
                    if fields[0] != oldsub:
                        oldsub = fields[0]
                        sub = LXPModel.Subject.objects.all().filter(subject_name__exact = oldsub )
                        if not sub:
                            sub = LXPModel.Subject.objects.create(subject_name = oldsub )
                            sub.save()
                            subid=sub.id
                        else:
                            for x in sub:
                                subid=x.id  
                    if fields[1] != oldmod:
                        oldmod = fields[1] 
                        mod = LXPModel.Module.objects.all().filter(module_name__exact = oldmod,subject_id=subid)
                        if not mod:
                            mod = LXPModel.Module.objects.create(module_name = oldmod,subject_id=subid)
                            mod.save()
                            modid=mod.id
                        else:
                            for x in mod:
                                modid=x.id 
                    if fields[2] != oldchap:
                        oldchap = fields[2] 
                        chap = LXPModel.Chapter.objects.all().filter(chapter_name__exact = oldchap,module_id=modid)
                        if not chap:
                            chap = LXPModel.Chapter.objects.create(chapter_name = oldchap,module_id=modid)
                            chap.save()
                            chapid=chap.id
                        else:
                            for x in chap:
                                chapid=x.id 
                    if fields[3] != oldtop:
                        oldtop = fields[3] 
                        top = LXPModel.Topic.objects.all().filter(topic_name__exact = oldtop,chapter_id=chapid)
                        if not top:
                            top = LXPModel.Topic.objects.create(topic_name = oldtop,chapter_id=chapid)
                            top.save()
                            topid1=top.id 
                        else:
                            for x in top:
                                topid1=x.id 
                    coursesetdet = LXPModel.CourseSetDetails.objects.create(
                                courseset_id =courseset.id,
                                subject_id=subid,
                                module_id=modid,
                                chapter_id=chapid,
                                topic_id=topid1
                                )
                    coursesetdet.save()
    return render(request,'cto/courseset/cto_upload_courseset_details_csv.html')

class CourseListView(ListView):
    model = LXPModel.Course
    context_object_name = 'courses'


class CourseCreateView(CreateView):
    model = LXPModel.Course
    form_class = LXPFORM.CourseForm
    success_url = reverse_lazy('course_changelist')
#
#
class CourseUpdateView(UpdateView):
    model = LXPModel.Course
    form_class = LXPFORM.CourseForm
    success_url = reverse_lazy('course_changelist')


def load_modules(request):
    subject_id = request.GET.get('subject')
    modules = LXPModel.Module.objects.filter(subject_id=subject_id).order_by('module_name')
    context = {'modules': modules}
    return render(request, 'hr/module_dropdown_list_options.html', context)

def load_chapters(request):
    module_id = request.GET.get('module')
    chapters = LXPModel.Chapter.objects.filter(module_id=module_id).order_by('chapter_name')
    context = {'chapters': chapters}
    return render(request, 'hr/chapter_dropdown_list_options.html', context)

def load_topics(request):
    chapter_id = request.GET.get('chapter')
    topics = LXPModel.Topic.objects.filter(chapter_id=chapter_id).order_by('topic_name')
    context = {'topics': topics}
    return render(request, 'hr/topic_dropdown_list_options.html', context)



@login_required
def getcredentials(request):
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
    client_secrets_file = "GoogleCredV1.json"

    # Get credentials and create an API client
    flow = None
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes)
    flow.run_local_server()
    credentials = flow.credentials
    return credentials

@login_required
def cto_sync_youtube_view(request):
    pllist = LXPModel.IncludePlaylist.objects.all().filter(playlist_id__in =LXPModel.Playlist.objects.all().order_by('name'))
    return render(request,'cto/youtube/cto_sync_youtube.html',{'pllist':pllist})

@login_required
def cto_include_playlist_view(request):
    pllist = LXPModel.Playlist.objects.all().order_by('name')
    includeplaylist = LXPModel.IncludePlaylist.objects.all().filter(playlist_id__in = LXPModel.Playlist.objects.all().order_by('name'))
    return render(request,'cto/youtube/cto_include_playlist.html',{'pllist':pllist,'includeplaylist':includeplaylist})

@login_required
def cto_include_playlist_save_view(request):
    if request.method=='POST':
        selectedlist = request.POST.getlist('playlist[]')
        incpl = LXPModel.IncludePlaylist.objects.all()
        incpl.delete()
        for PL_NAME in selectedlist:
            PL_ID = LXPModel.Playlist.objects.all().filter(name = PL_NAME)
            for z in PL_ID:
                incpl = LXPModel.IncludePlaylist.objects.create(
                    playlist_id = z.id
                )
                incpl.save()
                break
    pllist = LXPModel.Playlist.objects.all().order_by('name')
    return redirect('cto-include-playlist')

@login_required
def cto_sync_youtube_start_view(request):
    if request.method=='POST':
        pm = PlaylistManager()
        credentials = getcredentials(request)
        
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

@login_required
def cto_sync_youtube_byselected_playlist_start_view(request):
    if request.method=='POST':
        if 'dblist' in request.POST:
            pllist = LXPModel.Playlist.objects.all().order_by('name')
            return render(request,'cto/youtube/cto_sync_youtube.html',{'pllist':pllist})
        elif 'cloudlist' in request.POST:
            pm = PlaylistManager()
            credentials = getcredentials(request)
            pl =  pm.initializePlaylist(credentials)
            pllist = LXPModel.Playlist.objects.all().order_by('name')
            return render(request,'cto/youtube/cto_sync_youtube.html',{'pllist':pllist})
        elif 'startselected' in request.POST:
            pm = PlaylistManager()
            selectedlist = request.POST.getlist('playlist[]')
            maxcount = selectedlist.__len__()
            plcount = 1
            credentials = getcredentials(request)
            for PL_NAME in selectedlist:
                print(str(plcount) + ' of ' + str(maxcount))
                _id = PL_NAME 
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
######################################################################
