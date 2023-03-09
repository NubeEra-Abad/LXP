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
            materialForm=LXPFORM.MaterialForm(request.POST)
            if request.method=='POST':
                subject = request.POST.get('subject')
                module = request.POST.get('module')
                chapter = request.POST.get('chapter')
                topic = request.POST.get('topic')
                mtype = request.POST.get('mtype')
                urlvalue = request.POST.get('urlvalue')
                description = request.POST.get('description')
                
                material = LXPModel.Material.objects.get(id=pk)
                material.subject_id = subject
                material.module_id = module
                material.chapter_id = chapter
                material.topic_id = topic
                material.mtype = mtype
                material.urlvalue = urlvalue
                material.description = description
                material.save()
                materials = LXPModel.Material.objects.all()
                return render(request,'trainer/material/trainer_view_material.html',{'materials':materials})
            return render(request,'trainer/material/trainer_update_material.html',{'materialForm':materialForm})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def trainer_view_material_view(request):
    try:
        if str(request.session['utype']) == 'trainer':
            materials = LXPModel.Material.objects.all()
            return render(request,'trainer/material/trainer_view_material.html',{'materials':materials})
    except:
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
    try:
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
    except:
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

@login_required
def trainer_upload_material_details_csv_view(request):
    if request.method=='POST':
        if request.POST.get('select_file') == '':
            messages.info(request, 'Please select CSV file for upload')
        else:
            csv_file = request.FILES["select_file"]
            file_data = csv_file.read().decode("utf-8")		
            lines = file_data.split("\n")
            mat_type =''
            mat_url =''
            mat_desc =''
            oldsub =''
            oldmod=''
            oldchap=''
            oldtop=''
            corsetid =0
            subid =0
            modid=0
            chapid=0
            topid=0
            tochk=''
            no = 0
            for line in lines:						
                no = no + 1
                if no > 1:
                    fields = line.split(",")
                    mat_type = str(fields[4]).replace('///',',').replace('\r','')
                    mat_url = str(fields[5]).replace('///',',').replace('\r','')
                    mat_desc = str(fields[6]).replace('///',',').replace('\r','')
                    tochk = str(fields[0]).replace('///',',').replace('\r','')
                    if tochk != oldsub:
                        oldsub = tochk
                        sub = LXPModel.Subject.objects.all().filter(subject_name__exact = oldsub )
                        if not sub:
                            sub = LXPModel.Subject.objects.create(subject_name = oldsub )
                            sub.save()
                            subid=sub.id
                        else:
                            for x in sub:
                                subid=x.id  
                    tochk = str(fields[1]).replace('///',',').replace('\r','')
                    if tochk != oldmod:
                        oldmod = tochk
                        mod = LXPModel.Module.objects.all().filter(module_name__exact = oldmod,subject_id=subid)
                        if not mod:
                            mod = LXPModel.Module.objects.create(module_name = oldmod,subject_id=subid)
                            mod.save()
                            modid=mod.id
                        else:
                            for x in mod:
                                modid=x.id 
                    tochk = str(fields[2]).replace('///',',').replace('\r','')
                    if tochk != oldchap:
                        oldchap = tochk
                        chap = LXPModel.Chapter.objects.all().filter(chapter_name__exact = oldchap,module_id=modid)
                        if not chap:
                            chap = LXPModel.Chapter.objects.create(chapter_name = oldchap,module_id=modid)
                            chap.save()
                            chapid=chap.id
                        else:
                            for x in chap:
                                chapid=x.id 
                    tochk = str(fields[3]).replace('///',',').replace('\r','')
                    if tochk != oldtop:
                        oldtop = tochk
                        top = LXPModel.Topic.objects.all().filter(topic_name__exact = oldtop,chapter_id=chapid)
                        if not top:
                            top = LXPModel.Topic.objects.create(topic_name = oldtop,chapter_id=chapid)
                            top.save()
                            topid1=top.id 
                        else:
                            for x in top:
                                topid1=x.id 
                    mat = LXPModel.Material.objects.create(
                                subject_id=subid,
                                module_id=modid,
                                chapter_id=chapid,
                                topic_id=topid1,
                                mtype = mat_type,
                                urlvalue = mat_url,
                                description = mat_desc
                                )
                    mat.save()
    return render(request,'trainer/material/trainer_upload_material_details_csv.html')