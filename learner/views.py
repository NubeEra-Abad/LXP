from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from lxpapp import models as LXPModel
from lxpapp import forms as LXPFORM
@login_required
def learnerclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('indexpage')
    return render(request,'learner/learnerclick.html')

@login_required
def learner_dashboard_view(request):
    try:    
        if str(request.session['utype']) == 'learner':
            dict={
            'total_Video':0,
            'total_exam':0,
            }
            return render(request,'learner/learner_dashboard.html',context=dict)
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def learner_exam_view(request):
    try:    
        if str(request.session['utype']) == 'learner':
            exams=LXPModel.Exam.objects.raw("SELECT  lxpapp_exam.id,  lxpapp_batch.batch_name,  lxpapp_exam.exam_name FROM  lxpapp_batch  INNER JOIN lxpapp_batchlearner ON (lxpapp_batch.id = lxpapp_batchlearner.batch_id)  INNER JOIN lxpapp_exam ON (lxpapp_batch.id = lxpapp_exam.batch_id) WHERE lxpapp_exam.questiontpye = 'MCQ' AND lxpapp_batchlearner.learner_id = " + str(request.user.id)) 
            return render(request,'learner/exam/learner_exam.html',{'exams':exams})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def learner_take_exam_view(request,pk):
    try:    
        if str(request.session['utype']) == 'learner':
            exam = LXPModel.Exam.objects.all().filter(id=pk)
            mcqquestion= LXPModel.McqQuestion.objects.filter(exam_id=pk)
            total_marks = 0
            total_questions = 0
            for x in mcqquestion:
                total_marks = total_marks + x.marks
                total_questions = total_questions + 1
            return render(request,'learner/exam/learner_take_exam.html',{'exam':exam,'total_questions':total_questions,'total_marks':total_marks})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def learner_start_exam_view(request,pk):
    try:    
        if str(request.session['utype']) == 'learner':
            if request.method == 'POST':
                mcqresult = LXPModel.McqResult.objects.create(learner_id = request.user.id,exam_id =pk,marks=0,wrong=0,correct=0)
                mcqresult.save()
                questions=LXPModel.McqQuestion.objects.all().filter(exam_id=pk).order_by('?')
                score=0
                wrong=0
                correct=0
                total=0
                r_id = 0
                q_id = 0
                r_id = mcqresult.id
                for q in questions:
                    total+=1
                    question = LXPModel.McqQuestion.objects.all().filter(question=q.question)
                    for i in question:
                        q_id = i.id
                    resdet = LXPModel.McqResultDetails.objects.create(mcqresult_id = r_id,question_id =q_id,selected =str(request.POST.get(q.question)).replace('option',''))
                    resdet.save()
                    if 'option' + q.answer ==  request.POST.get(q.question):
                        score+= q.marks
                        correct+=1
                        
                    else:
                        wrong+=1
                percent = score/(total) *100
                context = {
                    'score':score,
                    'time': request.POST.get('timer'),
                    'correct':correct,
                    'wrong':wrong,
                    'percent':percent,
                    'total':total
                }
                mcqresult.marks = score
                mcqresult.wrong = wrong
                mcqresult.correct = correct
                mcqresult.timetaken = request.POST.get('timer')
                mcqresult.save()
                resdetobj = LXPModel.McqResultDetails.objects.raw("SELECT 1 as id,  lxpapp_mcqquestion.question as q,  lxpapp_mcqquestion.option1 as o1,  lxpapp_mcqquestion.option2 as o2,  lxpapp_mcqquestion.option3 as o3,  lxpapp_mcqquestion.option4 as o4,  lxpapp_mcqquestion.answer AS Correct,  lxpapp_mcqquestion.marks,  lxpapp_mcqresultdetails.selected AS answered  FROM  lxpapp_mcqresultdetails  INNER JOIN lxpapp_mcqresult ON (lxpapp_mcqresultdetails.mcqresult_id = lxpapp_mcqresult.id)  INNER JOIN lxpapp_mcqquestion ON (lxpapp_mcqresultdetails.question_id = lxpapp_mcqquestion.id) WHERE lxpapp_mcqresult.id = " + str(r_id) + " AND lxpapp_mcqresult.learner_id = " + str(request.user.id) + " ORDER BY lxpapp_mcqquestion.id" )
                return render(request,'learner/exam/learner_exam_result.html',{'total':total,'percent':percent, 'wrong':wrong,'correct':correct,'time': request.POST.get('timer'),'score':score,'resdetobj':resdetobj})
            else:
                questions=LXPModel.McqQuestion.objects.all()
                context = {
                    'questions':questions
                }
            exam=LXPModel.Exam.objects.get(id=pk)
            questions=LXPModel.McqQuestion.objects.all().filter(exam_id=exam.id).order_by('?')
            return render(request,'learner/exam/learner_start_exam.html',{'exam':exam,'questions':questions})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def learner_show_exam_reuslt_view(request,pk):
    try:    
        if str(request.session['utype']) == 'learner':
            exams=LXPModel.McqResult.objects.all().filter(exam_id__in = LXPModel.Exam.objects.all(), learner_id=request.user.id,exam_id = pk)
            return render(request,'learner/exam/learner_show_exam_reuslt.html',{'exams':exams})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def learner_show_exam_reuslt_details_view(request,pk):
    try:    
        if str(request.session['utype']) == 'learner':
            exams=LXPModel.McqResultDetails.objects.all().filter(question_id__in = LXPModel.McqQuestion.objects.all(), mcqresult_id = pk)
            return render(request,'learner/exam/learner_exam_result_details.html',{'exams':exams})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def learner_short_exam_view(request):
    try:    
        if str(request.session['utype']) == 'learner':
            shortexams=LXPModel.Exam.objects.raw("SELECT  lxpapp_exam.id,  lxpapp_batch.batch_name,  lxpapp_exam.exam_name FROM  lxpapp_batch  INNER JOIN lxpapp_batchlearner ON (lxpapp_batch.id = lxpapp_batchlearner.batch_id)  INNER JOIN lxpapp_exam ON (lxpapp_batch.id = lxpapp_exam.batch_id) WHERE lxpapp_exam.questiontpye = 'ShortAnswer' AND lxpapp_batchlearner.learner_id = " + str(request.user.id)) 
            return render(request,'learner/shortexam/learner_short_exam.html',{'shortexams':shortexams})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def learner_take_short_exam_view(request,pk):
    try:    
        if str(request.session['utype']) == 'learner':
            shortexam = LXPModel.Exam.objects.all().filter(id=pk)
            mcqquestion= LXPModel.ShortQuestion.objects.filter(exam_id=pk)
            total_marks = 0
            total_questions = 0
            for x in mcqquestion:
                total_marks = total_marks + x.marks
                total_questions = total_questions + 1
            return render(request,'learner/shortexam/learner_take_short_exam.html',{'shortexam':shortexam,'total_questions':total_questions,'total_marks':total_marks})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def learner_start_short_exam_view(request,pk):
    try:    
        if str(request.session['utype']) == 'learner':
            if request.method == 'POST':
                shortresult = LXPModel.ShortResult.objects.create(learner_id = request.user.id,exam_id =pk,marks=0)
                shortresult.save()
                questions=LXPModel.ShortQuestion.objects.all().filter(exam_id=pk).order_by('?')
                r_id = 0
                q_id = 0
                r_id = shortresult.id
                for q in questions:
                    question = LXPModel.ShortQuestion.objects.all().filter(question=q.question)
                    for i in question:
                        q_id = i.id
                    a=request.POST.get(str(q_id))
                    resdet = LXPModel.ShortResultDetails.objects.create(shortresult_id = r_id,question_id =q_id,answer =a,feedback ='',marks=0)
                    resdet.save()
                    
                shortresult.timetaken = request.POST.get('timer')
                shortresult.save()
                
                shortexams=LXPModel.Exam.objects.raw("SELECT  lxpapp_exam.id,  lxpapp_batch.batch_name,  lxpapp_exam.exam_name FROM  lxpapp_batch  INNER JOIN lxpapp_batchlearner ON (lxpapp_batch.id = lxpapp_batchlearner.batch_id)  INNER JOIN lxpapp_exam ON (lxpapp_batch.id = lxpapp_exam.batch_id) WHERE lxpapp_exam.questiontpye = 'ShortAnswer' AND lxpapp_batchlearner.learner_id = " + str(request.user.id)) 
                return render(request,'learner/shortexam/learner_short_exam.html',{'shortexams':shortexams})
            shortexam=LXPModel.Exam.objects.get(id=pk)
            questions=LXPModel.ShortQuestion.objects.all().filter(exam_id=shortexam.id).order_by('?')
            return render(request,'learner/shortexam/learner_start_short_exam.html',{'shortexam':shortexam,'questions':questions})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def learner_show_short_exam_reuslt_view(request,pk):
    try:    
        if str(request.session['utype']) == 'learner':
            #shortexams=LXPModel.ShortResult.objects.all().filter(exam_id__in = LXPModel.Exam.objects.all(), learner_id=request.user.id,exam_id = pk)
            shortexams=LXPModel.ShortResult.objects.raw("SELECT DISTINCT  lxpapp_exam.exam_name,  lxpapp_shortresult.datecreate,  SUM(DISTINCT lxpapp_shortresult.marks) AS Obtained,  Sum(lxpapp_shortquestion.marks) AS Tot,  lxpapp_shortresult.learner_id,  lxpapp_shortresult.timetaken,  lxpapp_shortresult.status,  lxpapp_shortresult.id FROM  lxpapp_shortquestion  LEFT OUTER JOIN lxpapp_exam ON (lxpapp_shortquestion.exam_id = lxpapp_exam.id)  LEFT OUTER JOIN lxpapp_shortresult ON (lxpapp_exam.id = lxpapp_shortresult.exam_id) WHERE  lxpapp_exam.id = " + str(pk) + " AND  lxpapp_shortresult.learner_id = " + str(request.user.id) + " GROUP BY  lxpapp_exam.exam_name,  lxpapp_shortresult.datecreate,  lxpapp_shortresult.learner_id,  lxpapp_shortresult.timetaken,  lxpapp_shortresult.status,  lxpapp_shortresult.id")
            return render(request,'learner/shortexam/learner_show_short_exam_reuslt.html',{'shortexams':shortexams})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def learner_show_short_exam_reuslt_details_view(request,pk):
    try:    
        if str(request.session['utype']) == 'learner':
            shortexams=LXPModel.ShortResultDetails.objects.all().filter(question_id__in = LXPModel.ShortQuestion.objects.all(), shortresult_id = pk)
            return render(request,'learner/shortexam/learner_short_exam_result_details.html',{'shortexams':shortexams})
    except:
        return render(request,'lxpapp/404page.html')
    
@login_required
def learner_video_Course_view(request):
    try:    
        if str(request.session['utype']) == 'learner':
            videos1 = LXPModel.BatchCourseSet.objects.raw('SELECT DISTINCT lxpapp_courseset.id,  lxpapp_courseset.courseset_name FROM  lxpapp_batchcourseset   INNER JOIN lxpapp_courseset ON (lxpapp_batchcourseset.courseset_id = lxpapp_courseset.id)   INNER JOIN lxpapp_batch ON (lxpapp_batchcourseset.batch_id = lxpapp_batch.id)   INNER JOIN lxpapp_batchlearner ON (lxpapp_batchlearner.batch_id = lxpapp_batch.id) WHERE   lxpapp_batchlearner.learner_id = ' + str(request.user.id))
            return render(request,'learner/video/learner_video_course.html',{'videos':videos1})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def learner_video_Course_subject_view(request):
    try:    
        if str(request.session['utype']) == 'learner':
            subject = LXPModel.Playlist.objects.raw('SELECT ID AS id, NAME, VTOTAL, Mtotal, SUM(VWATCHED) AS VWatched,((100*VWATCHED)/VTOTAL) as per, THUMBNAIL_URL FROM (SELECT YYY.ID, YYY.NAME, YYY.THUMBNAIL_URL, ( SELECT COUNT(XX.ID) FROM LXPAPP_PLAYLISTITEM XX WHERE XX.PLAYLIST_ID = YYY.ID ) AS Vtotal, ( SELECT COUNT(zz.ID) FROM LXPAPP_sessionmaterial zz WHERE zz.PLAYLIST_ID = YYY.ID ) AS Mtotal, (SELECT COUNT (LXPAPP_VIDEOWATCHED.ID) AS a FROM LXPAPP_PLAYLISTITEM GHGH LEFT OUTER JOIN LXPAPP_VIDEOWATCHED ON ( GHGH.VIDEO_ID = LXPAPP_VIDEOWATCHED.VIDEO_ID ) WHERE GHGH.PLAYLIST_ID = YYY.ID AND LXPAPP_VIDEOWATCHED.LEARNER_ID = ' + str(request.user.id) + ') AS VWatched FROM LXPAPP_BATCHLEARNER INNER JOIN LXPAPP_BATCH ON (LXPAPP_BATCHLEARNER.BATCH_ID = LXPAPP_BATCH.ID) INNER JOIN LXPAPP_BATCHRECORDEDVDOLIST ON (LXPAPP_BATCH.ID = LXPAPP_BATCHRECORDEDVDOLIST.BATCH_ID) INNER JOIN LXPAPP_PLAYLIST YYY ON (LXPAPP_BATCHRECORDEDVDOLIST.PLAYLIST_ID = YYY.ID) WHERE LXPAPP_BATCHLEARNER.LEARNER_ID = ' + str(request.user.id) + ') GROUP BY ID, NAME, VTOTAL ORDER BY NAME')
            videocount = LXPModel.LearnerPlaylistCount.objects.all().filter(learner_id = request.user.id)
            countpresent =False
            if videocount:
                countpresent = True
            per = 0
            tc = 0
            wc = 0
            for x in subject:
                if not videocount:
                    countsave = LXPModel.LearnerPlaylistCount.objects.create(playlist_id = x.id, learner_id = request.user.id,count =x.Vtotal )
                    countsave.save()
                tc += x.Vtotal
                wc += x.VWatched
            try:
                per = (100*int(wc))/int(tc)
            except:
                per =0
            dif = tc- wc

            return render(request,'learner/video/learner_video_course_subject.html',{'subject':subject,'dif':dif,'per':per,'wc':wc,'tc':tc})
    except:
        return render(request,'lxpapp/404page.html')
 
@login_required
def learner_video_list_view(request,subject_id):
#    try:     
        if str(request.session['utype']) == 'learner':
            subjectname = LXPModel.Playlist.objects.only('name').get(id=subject_id).name
            list = LXPModel.PlaylistItem.objects.raw("SELECT DISTINCT MAINVID.ID, MAINVID.NAME, IFNULL((SELECT LXPAPP_VIDEOWATCHED.VIDEO_ID FROM LXPAPP_VIDEOWATCHED WHERE LXPAPP_VIDEOWATCHED.LEARNER_ID = " + str(request.user.id) + " AND LXPAPP_VIDEOWATCHED.VIDEO_ID = MAINVID.ID), 0 ) AS watched, IFNULL((SELECT LXPAPP_VIDEOTOUNLOCK.VIDEO_ID FROM LXPAPP_VIDEOTOUNLOCK WHERE LXPAPP_VIDEOTOUNLOCK.LEARNER_ID = " + str(request.user.id) + " AND LXPAPP_VIDEOTOUNLOCK.VIDEO_ID = MAINVID.ID), 0) AS unlocked, IFNULL((SELECT LXPAPP_SESSIONMATERIAL.ID FROM LXPAPP_SESSIONMATERIAL WHERE LXPAPP_SESSIONMATERIAL.playlist_id = MAINLIST.PLAYLIST_ID AND LXPAPP_SESSIONMATERIAL.VIDEO_ID = MAINVID.ID), 0) AS matid FROM LXPAPP_PLAYLISTITEM MAINLIST INNER JOIN LXPAPP_VIDEO MAINVID ON ( MAINLIST.VIDEO_ID = MAINVID.ID ) WHERE MAINLIST.PLAYLIST_ID = " + str (subject_id) + " AND MAINVID.NAME <> 'Deleted video' ORDER BY MAINVID.NAME")  
            return render(request,'learner/video/learner_video_list.html',{'list':list,'subjectname':subjectname,'subject_id':subject_id})
 #   except:
        return render(request,'lxpapp/404page.html')

@login_required
def learner_video_sesseionmaterial_list_view(request,subject_id,video_id):
    try:     
        if str(request.session['utype']) == 'learner':
            subjectname = LXPModel.Playlist.objects.only('name').get(id=subject_id).name
            list = LXPModel.SessionMaterial.objects.all().filter(playlist_id = str (subject_id),video_id = str (video_id))  
            return render(request,'learner/video/learner_video_sesseionmaterial_list.html',{'list':list,'subjectname':subjectname,'subject_id':subject_id,'video_id':video_id})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def learner_show_video_view(request,subject_id,video_id):
    try:    
        if str(request.session['utype']) == 'learner':
            subjectname = LXPModel.Playlist.objects.only('name').get(id=subject_id).name
            Videos=LXPModel.Video.objects.all().filter(id=video_id)
            vunlock=LXPModel.VideoToUnlock.objects.all().filter(video_id__gt= video_id, playlist_id = subject_id)
            vunlock=LXPModel.VideoToUnlock.objects.raw('SELECT lxpapp_videotounlock.id FROM  lxpapp_videotounlock  WHERE lxpapp_videotounlock.playlist_id = ' + str(subject_id) + ' and lxpapp_videotounlock.video_id > ' + str(video_id) + ' AND  lxpapp_videotounlock.learner_id = ' + str(request.user.id) )

            nextvalue = LXPModel.PlaylistItem.objects.raw('SELECT  1 AS id,  lxpapp_playlistitem.video_id FROM  lxpapp_playlistitem  INNER JOIN lxpapp_video ON (lxpapp_playlistitem.video_id = lxpapp_video.id) WHERE  lxpapp_playlistitem.video_id > ' + str(video_id) + ' AND  lxpapp_playlistitem.playlist_id = ' + str(subject_id) + ' ORDER BY  lxpapp_video.name LIMIT 1')
            topicname =''
            url=''
            for x in Videos:
                videocount = LXPModel.VideoWatched.objects.all().filter(video_id = video_id,learner_id=request.user.id)
                topicname =x.name
                url = "https://www.youtube.com/embed/" + x.video_id
                
            if not videocount:
                for x in Videos:
                    vw=  LXPModel.VideoWatched.objects.create(video_id = video_id,learner_id=request.user.id)
                    vw.save()
                    for x in nextvalue:
                        vu=  LXPModel.VideoToUnlock.objects.create(video_id = x.video_id ,playlist_id = subject_id ,learner_id=request.user.id)
                        vu.save()

            return render(request,'learner/video/learner_show_video.html',{'topicname':topicname,'url':url,'subjectname':subjectname,'subject_id':subject_id,"video_id":video_id})
    except:
        return render(request,'LXPapp/404page.html')

@login_required
def learner_see_sesseionmaterial_view(request,subject_id,video_id,pk):
    try:
        if str(request.session['utype']) == 'learner':
            details= LXPModel.SessionMaterial.objects.all().filter(id=pk)
            subjectname = LXPModel.Playlist.objects.only('name').get(id=subject_id).name
            chaptername = LXPModel.Video.objects.only('name').get(id=video_id).name

            materialtype = 0
            for x in details:
                materialtype = x.mtype

            if materialtype == "HTML":
                return render(request,'learner/sessionmaterial/learner_sessionmaterial_htmlshow.html',{'details':details,'subjectname':subjectname,'chaptername':chaptername,'subject_id':subject_id})
            if materialtype == "URL":
                return render(request,'learner/sessionmaterial/learner_sessionmaterial_urlshow.html',{'details':details,'subjectname':subjectname,'chaptername':chaptername,'subject_id':subject_id})
            if materialtype == "PDF":
                return render(request,'learner/sessionmaterial/learner_sessionmaterial_pdfshow.html',{'details':details,'subjectname':subjectname,'chaptername':chaptername,'subject_id':subject_id,'video_id':video_id})
            if materialtype == "Video":
                return render(request,'learner/sessionmaterial/learner_sessionmaterial_pdfshow.html',{'details':details,'subjectname':subjectname,'chaptername':chaptername,'subject_id':subject_id})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def learner_studymaterial_course_view(request):
    #try:    
        if str(request.session['utype']) == 'learner':
            subject = LXPModel.Playlist.objects.raw('SELECT lxpapp_courseset.id, lxpapp_courseset.courseset_name   FROM  lxpapp_batchcourseset  INNER JOIN lxpapp_batch ON (lxpapp_batchcourseset.batch_id = lxpapp_batch.id)  INNER JOIN lxpapp_batchlearner ON (lxpapp_batch.id = lxpapp_batchlearner.batch_id)  INNER JOIN lxpapp_courseset ON (lxpapp_batchcourseset.courseset_id = lxpapp_courseset.id) WHERE lxpapp_batchlearner.learner_id = ' + str(request.user.id))
            return render(request,'learner/studymaterial/learner_studymaterial_course.html',{'subject':subject})
    #except:
        return render(request,'lxpapp/404page.html')

def learner_studymaterial_course_subject_view(request,coursename,courseset_id):
#    try:     
        if str(request.session['utype']) == 'learner':
            list = LXPModel.Subject.objects.raw("SELECT id, CASE WHEN srno != 1 THEN '' ELSE srno END as srno ,subject_name, chapter_name FROM (    SELECT DISTINCT  lxpapp_subject.id,    lxpapp_subject.subject_name,  lxpapp_chapter.chapter_name,ROW_NUMBER() OVER(PARTITION BY lxpapp_subject.subject_name) as srno FROM  lxpapp_coursesetdetails  INNER JOIN lxpapp_subject ON (lxpapp_coursesetdetails.subject_id = lxpapp_subject.id)  INNER JOIN lxpapp_chapter ON (lxpapp_coursesetdetails.chapter_id = lxpapp_chapter.id) WHERE lxpapp_coursesetdetails.courseset_id = " + str(courseset_id) + " group by lxpapp_subject.subject_name,  lxpapp_chapter.chapter_name ORDER BY  lxpapp_subject.subject_name,  lxpapp_chapter.chapter_name )" )
            return render(request,'learner/studymaterial/learner_studymaterial_course_subject.html',{'list':list,'coursename':coursename,'courseset_id':courseset_id})
 #   except:
        return render(request,'lxpapp/404page.html')

def learner_studymaterial_subject_chapter_view(request,coursename,subjectname,subject_id,courseset_id):
#    try:     
        if str(request.session['utype']) == 'learner': 
            list = LXPModel.Subject.objects.raw("SELECT   lxpapp_chapter.id,  lxpapp_topic.id as topicid,  lxpapp_chapter.chapter_name,  lxpapp_topic.topic_name,  ROW_NUMBER()OVER (PARTITION BY lxpapp_chapter.chapter_name) AS srno FROM  lxpapp_coursesetdetails  LEFT OUTER JOIN lxpapp_chapter ON (lxpapp_coursesetdetails.chapter_id = lxpapp_chapter.id)  LEFT OUTER JOIN lxpapp_topic ON (lxpapp_coursesetdetails.topic_id = lxpapp_topic.id) WHERE  lxpapp_coursesetdetails.subject_id = " + str(subject_id) + " AND  lxpapp_coursesetdetails.courseset_id = " + str(courseset_id) + " GROUP BY  lxpapp_chapter.chapter_name,  lxpapp_topic.topic_name  ORDER BY  lxpapp_chapter.chapter_name,  lxpapp_topic.topic_name")
            #list = LXPModel.Topic.objects.all().filter(chapter_id__in = LXPModel.Chapter.objects.all().distinct().filter(id__in = LXPModel.CourseSetDetails.objects.all().filter(subject_id=subject_id,courseset_id=courseset_id))).distinct()
            return render(request,'learner/studymaterial/learner_studymaterial_subject_chapter.html',{'list':list,'coursename':coursename,'subjectname':subjectname,'subject_id':subject_id,'courseset_id':courseset_id})
 #   except:
        return render(request,'lxpapp/404page.html')

def learner_studymaterial_chapter_topic_view(request,coursename,subjectname,chaptername,subject_id,chapter_id,courseset_id):
#    try:     
        if str(request.session['utype']) == 'learner':
            list = LXPModel.Subject.objects.raw("SELECT DISTINCT lxpapp_topic.topic_name, lxpapp_material.mtype, lxpapp_material.urlvalue, lxpapp_material.description, lxpapp_material.chapter_id, lxpapp_material.subject_id, lxpapp_material.id AS matid, lxpapp_topic.id, ROW_NUMBER()OVER (PARTITION BY lxpapp_topic.topic_name) AS srno FROM lxpapp_topic INNER JOIN lxpapp_material ON (lxpapp_material.topic_id = lxpapp_topic.id) AND (lxpapp_material.subject_id = " + str(subject_id) + ") WHERE lxpapp_topic.chapter_id = " + str(chapter_id))
            return render(request,'learner/studymaterial/learner_studymaterial_chapter_topic.html',{'list':list,'coursename':coursename,'subjectname':subjectname,'chaptername':chaptername,'subject_id':subject_id,'chapter_id':chapter_id})
 #   except:
        return render(request,'lxpapp/404page.html')