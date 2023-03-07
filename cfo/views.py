from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from lxpapp import models as LXPModel
from lxpapp import forms as LXPFORM
from django.shortcuts import render, redirect
from django.shortcuts import (HttpResponse, HttpResponseRedirect,
                              get_object_or_404, redirect, render)
from django.urls import reverse
from django.contrib import messages

@login_required
def cfoclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('indexpage')
    return render(request,'cfo/cfoclick.html')
 
@login_required    
def cfo_dashboard_view(request):
    try:
        if str(request.session['utype']) == 'cfo':
            dict={
            'total_course':0,
            'total_exam':0,
            'total_shortExam':0,
            'total_question':0,
            'total_learner':0
            }
        return render(request,'cfo/cfo_dashboard.html',context=dict)
    except:
        return render(request,'lxpapp/404page.html')
 

@login_required
def cfo_coursetype_view(request):
    try:
        if str(request.session['utype']) == 'cfo':
            return render(request,'cfo/coursetype/cfo_coursetype.html')
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def cfo_add_coursetype_view(request):
    form = LXPFORM.CourseTypeForm(request.POST or None)
    

    context = {
        'form': form,
        'page_title': 'Add Course Type'
    }
    if request.method == 'POST':
        if form.is_valid():
            name = form.cleaned_data.get('coursetype_name')
            coursetype = LXPModel.CourseType.objects.all().filter(coursetype_name__iexact = name)
            if coursetype:
                messages.info(request, 'Course Type Name Already Exist')
                return redirect(reverse('cfo-add-coursetype'))
            try:
                coursetype = LXPModel.CourseType.objects.create(
                                            coursetype_name = name)
                coursetype.save()
                messages.success(request, "Successfully Updated")
                return redirect(reverse('cfo-add-coursetype'))
            except Exception as e:
                messages.error(request, "Could Not Add " + str(e))
        else:
            messages.error(request, "Fill Form Properly")
    return render(request, 'cfo/coursetype/add_edit_coursetype.html', context)

@login_required
def cfo_update_coursetype_view(request, pk):
    instance = get_object_or_404(LXPModel.CourseType, id=pk)
    form = LXPFORM.CourseTypeForm(request.POST or None, instance=instance)
    context = {
        'form': form,
        'coursetype_id': pk,
        'page_title': 'Edit CourseType'
    }
    if request.method == 'POST':
        if form.is_valid():
            name = form.cleaned_data.get('coursetype_name')
            coursetype = LXPModel.CourseType.objects.all().filter(coursetype_name__iexact = name).exclude(id=pk)
            if coursetype:
                messages.info(request, 'Course Type Name Already Exist')
                return redirect(reverse('cfo-update-coursetype', args=[pk]))
            try:
                coursetype = LXPModel.CourseType.objects.get(id=pk)
                coursetype.coursetype_name = name
                coursetype.save()
                messages.success(request, "Successfully Updated")
                return redirect(reverse('cfo-update-coursetype', args=[pk]))
            except Exception as e:
                messages.error(request, "Could Not Add " + str(e))
        else:
            messages.error(request, "Fill Form Properly")
    return render(request, 'cfo/coursetype/add_edit_coursetype.html', context)


@login_required
def cfo_view_coursetype_view(request):
    try:
        if str(request.session['utype']) == 'cfo':
            coursetypes = LXPModel.CourseType.objects.all()
            return render(request,'cfo/coursetype/cfo_view_coursetype.html',{'coursetypes':coursetypes})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def cfo_delete_coursetype_view(request,pk):
    try:
        if str(request.session['utype']) == 'cfo':  
            coursetype=LXPModel.CourseType.objects.get(id=pk)
            coursetype.delete()
            return HttpResponseRedirect('/cfo/coursetype/cfo-view-coursetype')
        coursetypes = LXPModel.CourseType.objects.all()
        return render(request,'cfo/coursetype/cfo_view_coursetype.html',{'coursetypes':coursetypes})
    except:
        return render(request,'lxpapp/404page.html')