from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from lxpapp import models as LXPModel
from lxpapp import forms as LXPFORM
from django.contrib import messages

@login_required    
def trainer_dashboard_view(request):
    try:
        if str(request.session['utype']) == 'trainer':
            notification = LXPModel.TrainerNotification.objects.all().filter(trainer_id = request.user.id,status = False)
            dict={
            'total_course':0,
            'total_exam':0,
            'total_shortExam':0, 
            'total_question':0,
            'total_learner':0,
            'notifications':notification,
            }
        return render(request,'trainer/trainer_dashboard.html',context=dict)
    except:
        return render(request,'lxpapp/404page.html')
 
@login_required
def trainer_material_view(request):
    try:
        if str(request.session['utype']) == 'trainer':
            return render(request,'trainer/material/trainer_material.html')
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def trainer_add_material_view(request):
    try:
        if str(request.session['utype']) == 'trainer':
            if request.method=='POST':
                materialForm=LXPFORM.MaterialForm(request.POST)
                subject = request.POST.get('subject')
                module = request.POST.get('module')
                chapter = request.POST.get('chapter')
                topic = request.POST.get('topic')
                mtype = request.POST.get('mtype')
                urlvalue = request.POST.get('urlvalue')
                description = request.POST.get('description')
                material = LXPModel.Material.objects.create(subject_id = subject,module_id = module,chapter_id = chapter,topic_id = topic,mtype = mtype,urlvalue = urlvalue,description = description)
                material.save()
                
            materialForm=LXPFORM.MaterialForm()
            return render(request,'trainer/material/trainer_add_material.html',{'materialForm':materialForm})
    except:
        return render(request,'lxpapp/404page.html')
    
@login_required
def trainer_update_material_view(request,pk):
    try:
        if str(request.session['utype']) == 'trainer':
            material = LXPModel.Video.objects.get(id=pk)
            materialForm=LXPFORM.MaterialForm(request.POST,instance=material)
            if request.method=='POST':
                if materialForm.is_valid(): 
                    materialtext = materialForm.cleaned_data["name"]
                    subjecttext = materialForm.cleaned_data["subjectID"]
                    
                    material = LXPModel.Video.objects.all().filter(name__iexact = materialtext).exclude(id=pk)
                    if material:
                        messages.info(request, 'Material Name Already Exist')
                        return render(request,'trainer/material/trainer_update_material.html',{'materialForm':materialForm})
                    else:
                        subject = LXPModel.Playlist.objects.get(name=subjecttext)
                        
                        material = LXPModel.Video.objects.get(id=pk)
                        oldsubject =LXPModel.PlaylistItem.objects.get(video_id=pk)
                        material.name = materialtext
                        material.save()
                        PLItems = LXPModel.PlaylistItem.objects.get(video_id=pk,playlist_id = oldsubject.playlist_id)
                        PLItems.playlist_id =subject.id
                        PLItems.save()
                        c_list = LXPModel.Video.objects.raw('SELECT   lxpapp_video.id,  lxpapp_video.name,  lxpapp_video.video_id,  lxpapp_playlist.name AS plname FROM  lxpapp_playlistitem  INNER JOIN lxpapp_video ON (lxpapp_playlistitem.video_id = lxpapp_video.id)  INNER JOIN lxpapp_playlist ON (lxpapp_playlistitem.playlist_id = lxpapp_playlist.id)')
                        return render(request,'trainer/material/trainer_view_material.html',{'materials':c_list})
            return render(request,'trainer/material/trainer_update_material.html',{'materialForm':materialForm,'sub':material.name})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def trainer_view_material_view(request):
    #try:
        if str(request.session['utype']) == 'trainer':
            materials = LXPModel.Material.objects.all()
            return render(request,'trainer/material/trainer_view_material.html',{'materials':materials})
    #except:
        return render(request,'lxpapp/404page.html')

@login_required
def trainer_delete_material_view(request,pk):
    try:
        if str(request.session['utype']) == 'trainer':  
            material=LXPModel.Material.objects.get(id=pk)
            material.delete()
            materials = LXPModel.Material.objects.all()
            return render(request,'trainer/material/trainer_view_material.html',{'materials':materials})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def trainer_show_material_view(request,materialtype,pk):
    #try:
        if str(request.session['utype']) == 'trainer':
            details= LXPModel.Material.objects.all().filter(id=pk)
            if materialtype == 'HTML':
                return render(request,'trainer/material/trainer_material_htmlshow.html',{'details':details})
            if materialtype == 'URL':
                return render(request,'trainer/material/trainer_material_urlshow.html',{'details':details})
            if materialtype == 'PDF':
                return render(request,'trainer/material/trainer_material_pdfshow.html',{'details':details})
            if materialtype == 'Video':
                return render(request,'trainer/material/trainer_material_videoshow.html',{'details':details})
    #except:
        return render(request,'lxpapp/404page.html')

@login_required
def trainer_material_upload_file_view(request):
    subjects = LXPModel.Playlist.objects.all()
    context = {'subjects': subjects}
    return render(request,'trainer/uploadpdf/trainer_material_upload_file.html',context)

from django.conf import settings
from datetime import datetime
import boto3, botocore
ALLOWED_EXTENSIONS = set(['pdf'])
def allowed_file(name):
    return "." in name and name.split(".")[1].lower() in ALLOWED_EXTENSIONS
# Connect to the s3 service
s3 = boto3.client(
    "s3",
    aws_access_key_id=settings.AWS_ACCESS_KEY,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
)
#upload file to s3 w/ acl as public

@login_required  
def upload_material_file_to_s3(request,file, bucket_name, acl="public-read"):
    try:
        filename = datetime.now().strftime("%Y%m%d%H%M%S.pdf")
        print("intered in function")
        s3.upload_fileobj(
            file,
            bucket_name,
            filename,
            ExtraArgs={
                "ACL": acl,
                "ContentType": file.content_type
            }
        )
    except Exception as e:
        print("Something Unexpected Happened: ", e)
        return e
    # returns the webling to file upload to view
    url=settings.AWS_DOMAIN + '' + filename
    subject = request.POST.getlist('subject')
    chapter = request.POST.getlist('chapters')
    mtype = '3'
    description = 'file uploaded'
    for x in subject:
        subject = x
    for x in chapter:
        chapter = x
    for x in mtype:
        mtype = x
    if subject == 'Choose your Subject':
        messages.info(request, 'Please Select Subject')
    if chapter == 'Choose your Chapter':
        messages.info(request, 'Please Select Chapter')
    if mtype == 'Choose your Type':
        messages.info(request, 'Please Select Material Type')
    if description is None:
        messages.info(request, 'Please Enter Description')

    if description is not None and subject !='Choose your Subject' and  chapter !='Choose your Chapter' and mtype !='Choose your Type' :
        material = LXPModel.Material.objects.create(
            subject_id = subject,
            chapter_id = chapter,
            mtype = mtype,
            urlvalue=url,
            description=description
        ).save()
    
    subjects = LXPModel.Playlist.objects.all()
    context = {'subjects': subjects}
    return render(request,'trainer/uploadpdf/trainer_material_upload_file.html',context)

@login_required
def trainer_material_start_upload_file_view(request):
    if request.method=="POST":
        file=request.FILES["select_file"]
        if file == "":
            return "Please return to previous page and select a file"
        if file:
            output = upload_material_file_to_s3(request, file, settings.AWS_BUCKET_NAME)
            return output
        else:
            return redirect("/")
