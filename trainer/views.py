from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from lxpapp import models as LXPModel
from lxpapp import forms as LXPFORM
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Sum,Count,Q
from django.urls import reverse

@login_required    
def trainer_dashboard_view(request):
    try:
        if str(request.session['utype']) == 'trainer':
            notification = LXPModel.TrainerNotification.objects.all().filter(trainer_id = request.user.id,status = False)
            mco = LXPModel.Exam.objects.filter(questiontpye='MCQ').count()
            short = LXPModel.Exam.objects.filter(questiontpye='ShortAnswer').count()
            mcqques= LXPModel.McqQuestion.objects.all().count()
            sques= LXPModel.ShortQuestion.objects.all().count()
            dict={
            'total_course':0,
            'total_exam':0,
            'total_shortExam':0, 
            'total_question':0,
            'total_short':0,
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

@login_required
def trainer_exam_view(request):
    try:
        if str(request.session['utype']) == 'trainer':
            return render(request,'trainer/exam/trainer_exam.html')
    except:
        return render(request,'lxpapp/404page.html')


@login_required
def trainer_add_exam_view(request):
    #try:
        if str(request.session['utype']) == 'trainer':
            form = LXPFORM.ExamForm(request.POST or None)
            breadcrumblink = []
            btrnr={}
            btrnr["head"]='Dashboard'
            btrnr["link"]='../../../../trainer/trainer-dashboard'
            breadcrumblink.append(btrnr)

            btrnr={}
            btrnr["head"]='View Exam'
            btrnr["link"]='../../../../trainer/trainer-view-exam'
            breadcrumblink.append(btrnr)
            
            btrnr={}
            btrnr["head"]='Active'
            btrnr["link"]='Add Exam'
            breadcrumblink.append(btrnr)
            
            context = {
                'form': form,
                'breadcrumbsetting':breadcrumblink,
                'page_title': 'Add Exam'
            }
            if request.method == 'POST':
                if form.is_valid():
                    name = form.cleaned_data.get('exam_name')
                    exam = LXPModel.Exam.objects.all().filter(exam_name__iexact = name)
                    if exam:
                        messages.info(request, 'Exam Name Already Exist')
                        return redirect(reverse('trainer-add-exam'))
                    try:
                        qtype = form.cleaned_data.get('questiontpye')
                        batch = form.cleaned_data.get('batchID')
                        exam = LXPModel.Exam.objects.create(
                                                    exam_name = name,questiontpye=qtype,batch=batch)
                        exam.save()
                        messages.success(request, "Successfully Updated")
                        return redirect(reverse('trainer-add-exam'))
                    except Exception as e:
                        messages.error(request, "Could Not Add " + str(e))
                else:
                    messages.error(request, "Fill Form Properly")
            return render(request, 'trainer/exam/add_edit_exam.html', context)
    #except:
        return render(request,'lxpapp/404page.html')

@login_required
def trainer_update_exam_view(request,pk):
    try:
        if str(request.session['utype']) == 'trainer':
            instance = get_object_or_404(LXPModel.Exam, id=pk)
            form = LXPFORM.ExamForm(request.POST or None, instance=instance)
            breadcrumblink = []
            btrnr={}
            btrnr["head"]='Dashboard'
            btrnr["link"]='../../../../trainer/trainer-dashboard'
            breadcrumblink.append(btrnr)
            
            btrnr={}
            btrnr["head"]='Add Exam'
            btrnr["link"]='../../../../trainer/trainer-add-exam'
            breadcrumblink.append(btrnr)
            
            btrnr={}
            btrnr["head"]='View Exam'
            btrnr["link"]='../../../../trainer/trainer-view-exam'
            breadcrumblink.append(btrnr)
            
            btrnr={}
            btrnr["head"]='Active'
            btrnr["link"]='Update Exam'
            breadcrumblink.append(btrnr)
            
            context = {
                'form': form,
                'exam_id': pk,
                'breadcrumbsetting':breadcrumblink,
                'page_title': 'Update Exam'
            }
            if request.method == 'POST':
                if form.is_valid():
                    name = form.cleaned_data.get('exam_name')
                    batch = form.cleaned_data.get('batch').pk
                    qtype = form.cleaned_data.get('questiontpye')
                    exam = LXPModel.Exam.objects.all().filter(exam_name__iexact = name).exclude(id=pk)
                    if exam:
                        messages.info(request, 'Exam Name Already Exist')
                        return redirect(reverse('trainer-update-exam', args=[pk]))
                    try:
                        exam = LXPModel.Exam.objects.get(id=pk)
                        exam.exam_name = name
                        exam.batch_id = batch
                        exam.questiontpye = qtype
                        exam.save()
                        messages.success(request, "Successfully Updated")
                        exams = LXPModel.Exam.objects.all()
                        return render(request,'trainer/exam/trainer_view_exam.html',{'exams':exams})
                    except Exception as e:
                        messages.error(request, "Could Not Add " + str(e))
                else:
                    messages.error(request, "Fill Form Properly")

            return render(request, 'trainer/exam/add_edit_exam.html', context,{'a':'imran'})
    except:
        return render(request,'lxpapp/404page.html')
@login_required
def trainer_upload_exam_csv_view(request):
    if request.method=='POST':
        file=request.FILES["select_file"]
        examtext=request.POST.get('exam_name')
        batch=request.POST.get('batch')
        qtype=request.POST.get('examtype')
        exam = LXPModel.Exam.objects.all().filter(exam_name__iexact = examtext)
        if exam:
            messages.info(request, 'Exam Name Already Exist')
        else:
            if qtype=='0':
                qtype = 'MCQ'
            else:
                qtype = 'ShortAnswer'
            exam = LXPModel.Exam.objects.create(batch_id = batch,exam_name = examtext,questiontpye = qtype)
            exam.save()   
            csv_file = request.FILES["select_file"]
            file_data = csv_file.read().decode("utf-8")		
            lines = file_data.split("\n")
            no = 0
            for line in lines:						
                no = no + 1
                if no > 1:
                    fields = line.split(",")
                    if qtype == 'MCQ':
                        question = LXPModel.McqQuestion.objects.create(
                            question = fields[0],
                            option1 = fields[1],
                            option2 = fields[2],
                            option3 = fields[3],
                            option4 = fields[4],
                            answer = fields[5],
                            marks = fields[6],
                            exam_id = exam.id
                        )
                        question.save()
                    elif qtype == 'ShortAnswer':
                        question = LXPModel.ShortQuestion.objects.create(
                            question = fields[0],
                            marks = fields[1],
                            exam_id = exam.id
                        )
                        question.save()
    batch = LXPModel.Batch.objects.all()
    context = {'batch': batch}
    return render(request,'trainer/exam/trainer_upload_exam_csv.html',context)

def upload_csv(request):
	data = {}
	if "GET" == request.method:
		return render(request, "myapp/upload_csv.html", data)
    # if not GET, then proceed
	try:
		csv_file = request.FILES["csv_file"]
		file_data = csv_file.read().decode("utf-8")		
		lines = file_data.split("\n")
		#loop over the lines and save them in db. If error , store as string and then display
		for line in lines:						
			fields = line.split(",")
			data_dict = {}
			data_dict["name"] = fields[0]
			data_dict["start_date_time"] = fields[1]
			data_dict["end_date_time"] = fields[2]
			data_dict["notes"] = fields[3]
			

	except Exception as e:
		messages.error(request,"Unable to upload file. "+repr(e))

@login_required
def trainer_view_exam_view(request):
    try:
        if str(request.session['utype']) == 'trainer':
            exams = LXPModel.Exam.objects.all().filter(batch_id__in = LXPModel.Batch.objects.all())
            return render(request,'trainer/exam/trainer_view_exam.html',{'exams':exams})
    except:
        return render(request,'lxpapp/404page.html')

def trainer_view_filter_exam_view(request,type):
    try:
        if str(request.session['utype']) == 'trainer':
            exams = LXPModel.Exam.objects.all().filter(batch_id__in = LXPModel.Batch.objects.all(),questiontpye = type)
            return render(request,'trainer/exam/trainer_view_exam.html',{'exams':exams})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def trainer_delete_exam_view(request,pk):
    try:
        if str(request.session['utype']) == 'trainer':  
            exam=LXPModel.Exam.objects.get(id=pk)
            exam.delete()
            return HttpResponseRedirect('/trainer/trainer-view-exam')
        exams = LXPModel.Exam.objects.all()
        return render(request,'trainer/exam/trainer_view_exam.html',{'exams':exams})
    except:
        return render(request,'lxpapp/404page.html')
 
@login_required
def trainer_mcqquestion_view(request):
    try:
        if str(request.session['utype']) == 'trainer':
            return render(request,'trainer/mcqquestion/trainer_mcqquestion.html')
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def trainer_add_mcqquestion_view(request):
    try:
        if str(request.session['utype']) == 'trainer':
            if request.method=='POST':
                mcqquestionForm=LXPFORM.McqQuestionForm(request.POST)
                if mcqquestionForm.is_valid(): 
                    questiontext = mcqquestionForm.cleaned_data["question"]
                    mcqquestion = LXPModel.McqQuestion.objects.all().filter(question__iexact = questiontext)
                    if mcqquestion:
                        messages.info(request, 'Mcq Question Name Already Exist')
                        mcqquestionForm=LXPFORM.McqQuestionForm()
                        return render(request,'trainer/mcqquestion/trainer_add_mcqquestion.html',{'mcqquestionForm':mcqquestionForm})                  
                    else:
                        exam=LXPModel.Exam.objects.get(id=request.POST.get('examID'))
                        mcqquestion = LXPModel.McqQuestion.objects.create(exam_id = exam.id,question = questiontext,option1=request.POST.get('option1'),option2=request.POST.get('option2'),option3=request.POST.get('option3'),option4=request.POST.get('option4'),answer=request.POST.get('answer'),marks=request.POST.get('marks'))
                        mcqquestion.save()
                else:
                    print("form is invalid")
            mcqquestionForm=LXPFORM.McqQuestionForm()
            return render(request,'trainer/mcqquestion/trainer_add_mcqquestion.html',{'mcqquestionForm':mcqquestionForm})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def trainer_update_mcqquestion_view(request,pk):
    try:
        if str(request.session['utype']) == 'trainer':
            mcqquestion = LXPModel.McqQuestion.objects.get(id=pk)
            mcqquestionForm=LXPFORM.McqQuestionForm(request.POST,instance=mcqquestion)
            if request.method=='POST':
                if mcqquestionForm.is_valid(): 
                    mcqquestiontext = mcqquestionForm.cleaned_data["mcqquestion_name"]
                    mcqquestion = LXPModel.McqQuestion.objects.all().filter(mcqquestion_name__iexact = mcqquestiontext).exclude(id=pk)
                    if mcqquestion:
                        messages.info(request, 'McqQuestion Name Already Exist')
                        return render(request,'trainer/mcqquestion/trainer_update_mcqquestion.html',{'mcqquestionForm':mcqquestionForm})
                    else:
                        mcqquestionForm.save()
                        mcqquestions = LXPModel.McqQuestion.objects.all()
                        return render(request,'trainer/mcqquestion/trainer_view_mcqquestion.html',{'mcqquestions':mcqquestions})
            return render(request,'trainer/mcqquestion/trainer_update_mcqquestion.html',{'mcqquestionForm':mcqquestionForm,'ex':mcqquestion.mcqquestion_name,'sub':mcqquestion.questiontpye})
    except:
        return render(request,'lxpapp/404page.html')
@login_required
def trainer_view_mcqquestion_exams_view(request):
    try:
        if str(request.session['utype']) == 'trainer':
            exams = LXPModel.Exam.objects.all().filter(questiontpye='MCQ')
            return render(request,'trainer/mcqquestion/trainer_view_mcqquestion_exams.html',{'exams':exams})
    except:
        return render(request,'lxpapp/404page.html')
@login_required
def trainer_view_mcqquestion_view(request,examid):
    try:
        if str(request.session['utype']) == 'trainer':
            mcqquestions = LXPModel.McqQuestion.objects.all().filter(exam_id__in = LXPModel.Exam.objects.all().filter(id=examid))
            return render(request,'trainer/mcqquestion/trainer_view_mcqquestion.html',{'mcqquestions':mcqquestions})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def trainer_delete_mcqquestion_view(request,pk):
    try:
        if str(request.session['utype']) == 'trainer':  
            mcqquestion=LXPModel.McqQuestion.objects.get(id=pk)
            mcqquestion.delete()
            return HttpResponseRedirect('/trainer/trainer-view-mcqquestion')
        mcqquestions = LXPModel.McqQuestion.objects.all()
        return render(request,'trainer/mcqquestion/trainer_view_mcqquestion.html',{'mcqquestions':mcqquestions})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def trainer_shortquestion_view(request):
    try:
        if str(request.session['utype']) == 'trainer':
            return render(request,'trainer/shortquestion/trainer_shortquestion.html')
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def trainer_add_shortquestion_view(request):
    try:
        if str(request.session['utype']) == 'trainer':
            if request.method=='POST':
                shortquestionForm=LXPFORM.ShortQuestionForm(request.POST)
                if shortquestionForm.is_valid(): 
                    questiontext = shortquestionForm.cleaned_data["question"]
                    shortquestion = LXPModel.ShortQuestion.objects.all().filter(question__iexact = questiontext)
                    if shortquestion:
                        messages.info(request, 'Short Question Already Exist')
                        shortquestionForm=LXPFORM.ShortQuestionForm()
                        return render(request,'trainer/shortquestion/trainer_add_shortquestion.html',{'shortquestionForm':shortquestionForm})                  
                    else:
                        exam=LXPModel.Exam.objects.get(id=request.POST.get('examID'))
                        shortquestion = LXPModel.ShortQuestion.objects.create(exam_id = exam.id,question = questiontext,marks=request.POST.get('marks'))
                        shortquestion.save()
                else:
                    print("form is invalid")
            shortquestionForm=LXPFORM.ShortQuestionForm()
            return render(request,'trainer/shortquestion/trainer_add_shortquestion.html',{'shortquestionForm':shortquestionForm})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def trainer_update_shortquestion_view(request,pk):
    try:
        if str(request.session['utype']) == 'trainer':
            shortquestion = LXPModel.ShortQuestion.objects.get(id=pk)
            shortquestionForm=LXPFORM.ShortQuestionForm(request.POST,instance=shortquestion)
            if request.method=='POST':
                if shortquestionForm.is_valid(): 
                    shortquestiontext = shortquestionForm.cleaned_data["question"]
                    shortquestion = LXPModel.ShortQuestion.objects.all().filter(question__iexact = shortquestiontext).exclude(id=pk)
                    if shortquestion:
                        messages.info(request, 'ShortQuestion Name Already Exist')
                        return render(request,'trainer/shortquestion/trainer_update_shortquestion.html',{'shortquestionForm':shortquestionForm})
                    else:
                        examid = LXPModel.Exam.objects.all().filter(id=request.POST['examID'])
                        shortquestionForm.examID=examid
                        shortquestionForm.save()
                        shortquestions = LXPModel.ShortQuestion.objects.all()
                        return render(request,'trainer/shortquestion/trainer_view_shortquestion.html',{'shortquestions':shortquestions})
            return render(request,'trainer/shortquestion/trainer_update_shortquestion.html',{'shortquestionForm':shortquestionForm,'ex':shortquestion.question})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def trainer_view_shortquestion_view(request):
    try:
        if str(request.session['utype']) == 'trainer':
            shortquestions = LXPModel.ShortQuestion.objects.all().filter(exam_id__in = LXPModel.Exam.objects.all())
            return render(request,'trainer/shortquestion/trainer_view_shortquestion.html',{'shortquestions':shortquestions})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def trainer_delete_shortquestion_view(request,pk):
    try:
        if str(request.session['utype']) == 'trainer':  
            shortquestion=LXPModel.ShortQuestion.objects.get(id=pk)
            shortquestion.delete()
            return HttpResponseRedirect('/trainer/trainer-view-shortquestion')
        shortquestions = LXPModel.ShortQuestion.objects.all()
        return render(request,'trainer/shortquestion/trainer_view_shortquestion.html',{'shortquestions':shortquestions})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def trainer_pending_short_exam_result_view(request):
    #try:
        if str(request.session['utype']) == 'trainer':
            pending = LXPModel.ShortResult.objects.all().filter( learner_id__in = User.objects.all(),exam_id__in = LXPModel.Exam.objects.all(),status = False)
            return render(request,'trainer/shortexam/trainer_pending_short_exam_reuslt.html',{'pending':pending})
    #except:
        return render(request,'lxpapp/404page.html')

@login_required
def trainer_update_short_question_result_view(request,pk):
    try:
        if str(request.session['utype']) == 'trainer':
            resultdetails = LXPModel.ShortResultDetails.objects.all().filter( question_id__in = LXPModel.ShortQuestion.objects.all(),shortresult_id = pk)
            return render(request,'trainer/shortexam/trainer_update_short_question_result.html',{'resultdetails':resultdetails})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def trainer_save_short_question_result_view(request,pk):
    try:
        if str(request.session['utype']) == 'trainer':
            if request.method=="POST":
                feedback=request.POST['newfeedback']
                marks=request.POST['newmarks']
                rid=request.POST['newid']
                qid=request.POST['newqid']
                answer=request.POST['newanswer']
                mainid=request.POST['newmainid']
                resupdate = LXPModel.ShortResultDetails.objects.all().filter(id=pk)
                resupdate.delete()
                resupdate = LXPModel.ShortResultDetails.objects.create(id=pk,marks=marks,feedback=feedback,question_id=qid,answer=answer,shortresult_id=mainid)
                resupdate.save()
                
                totmarks=LXPModel.ShortResultDetails.objects.all().filter(shortresult_id=mainid).aggregate(stars=Sum('marks'))['stars']
                maintbl=LXPModel.ShortResult.objects.get(id=mainid)
                tot=LXPModel.ShortResultDetails.objects.all().filter(shortresult_id=mainid).aggregate(stars=Count('marks'))['stars']
                totgiven=LXPModel.ShortResultDetails.objects.all().filter(shortresult_id=mainid,marks__gt=0).aggregate(stars=Count('marks'))['stars']
                if tot == totgiven:
                    maintbl.status=True
                maintbl.marks = totmarks
                maintbl.save()
                if tot == totgiven:
                    resultdetails = LXPModel.ShortResultDetails.objects.all().filter( question_id__in = LXPModel.ShortQuestion.objects.all(),shortresult_id = pk)
                    return render(request,'trainer/shortexam/trainer_update_short_question_result.html',{'resultdetails':resultdetails})
                else:
                    resultdetails = LXPModel.ShortResultDetails.objects.all().filter( question_id__in = LXPModel.ShortQuestion.objects.all(),shortresult_id = mainid)
                    return render(request,'trainer/shortexam/trainer_update_short_question_result.html',{'resultdetails':resultdetails})
    except:
        return render(request,'lxpapp/404page.html') 

@login_required
def trainer_ytexamquestion_view(request):
    try:
        if str(request.session['utype']) == 'trainer':
            return render(request,'trainer/ytexamquestion/trainer_ytexamquestion.html')
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def trainer_add_ytexamquestion_view(request):
    #try:
        if str(request.session['utype']) == 'trainer':
            if request.method=='POST':
                ytexamquestionForm=LXPFORM.YTExamQuestionForm(request.POST)
                if ytexamquestionForm.is_valid(): 
                    questiontext = ytexamquestionForm.cleaned_data["question"]
                    ytexamquestion = LXPModel.YTExamQuestion.objects.all().filter(question__iexact = questiontext)
                    if ytexamquestion:
                        messages.info(request, 'Mcq Question Name Already Exist')
                        ytexamquestionForm=LXPFORM.YTExamQuestionForm()
                        return render(request,'trainer/ytexamquestion/trainer_add_ytexamquestion.html',{'ytexamquestionForm':ytexamquestionForm})                  
                    else:
                        playlist=LXPModel.Playlist.objects.get(id=ytexamquestionForm.cleaned_data["playlistID"].pk)
                        video=LXPModel.Video.objects.get(id=ytexamquestionForm.cleaned_data["videoID"].pk)
                        ytexamquestion = LXPModel.YTExamQuestion.objects.create(
                            playlist_id = playlist.id,
                            video_id = video.id,
                            question = questiontext,
                            option1=request.POST.get('option1'),
                            option2=request.POST.get('option2'),
                            option3=request.POST.get('option3'),
                            option4=request.POST.get('option4'),
                            answer=request.POST.get('answer'),
                            marks=request.POST.get('marks'))
                        ytexamquestion.save()
                else:
                    print("form is invalid")
            ytexamquestionForm=LXPFORM.YTExamQuestionForm()
            return render(request,'trainer/ytexamquestion/trainer_add_ytexamquestion.html',{'ytexamquestionForm':ytexamquestionForm})
    #except:
        return render(request,'lxpapp/404page.html')

@login_required
def trainer_update_ytexamquestion_view(request,pk):
    try:
        if str(request.session['utype']) == 'trainer':
            ytexamquestion = LXPModel.YTExamQuestion.objects.get(id=pk)
            ytexamquestionForm=LXPFORM.YTExamQuestionForm(request.POST,instance=ytexamquestion)
            if request.method=='POST':
                if ytexamquestionForm.is_valid(): 
                    ytexamquestiontext = ytexamquestionForm.cleaned_data["ytexamquestion_name"]
                    ytexamquestion = LXPModel.YTExamQuestion.objects.all().filter(ytexamquestion_name__iexact = ytexamquestiontext).exclude(id=pk)
                    if ytexamquestion:
                        messages.info(request, 'Question Already Exist')
                        return render(request,'trainer/ytexamquestion/trainer_update_ytexamquestion.html',{'ytexamquestionForm':ytexamquestionForm})
                    else:
                        ytexamquestionForm.save()
                        ytexamquestions = LXPModel.YTExamQuestion.objects.all()
                        return render(request,'trainer/ytexamquestion/trainer_view_ytexamquestion.html',{'ytexamquestions':ytexamquestions})
            return render(request,'trainer/ytexamquestion/trainer_update_ytexamquestion.html',{'ytexamquestionForm':ytexamquestionForm,'ex':ytexamquestion.ytexamquestion_name,'sub':ytexamquestion.questiontpye})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def trainer_view_ytexamquestion_view(request):
    try:
        if str(request.session['utype']) == 'trainer':
            ytexamquestions = LXPModel.YTExamQuestion.objects.all().filter(playlist_id__in = LXPModel.Playlist.objects.all())
            return render(request,'trainer/ytexamquestion/trainer_view_ytexamquestion.html',{'ytexamquestions':ytexamquestions})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def trainer_delete_ytexamquestion_view(request,pk):
    try:
        if str(request.session['utype']) == 'trainer':  
            ytexamquestion=LXPModel.YTExamQuestion.objects.get(id=pk)
            ytexamquestion.delete()
            return HttpResponseRedirect('/trainer/trainer-view-ytexamquestion')
        ytexamquestions = LXPModel.YTExamQuestion.objects.all()
        return render(request,'trainer/ytexamquestion/trainer_view_ytexamquestion.html',{'ytexamquestions':ytexamquestions})
    except:
        return render(request,'lxpapp/404page.html')