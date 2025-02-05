from lxpapiapp.models import *
from .staffserializers import *
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.db.models import Sum, Case, When, Value, Max
from django.db.models.functions import Coalesce
from django.http import JsonResponse
from django.conf import settings
from urllib.parse import quote_plus
import csv

class MaterialAPIView(APIView):
    permission_classes = [IsAuthenticated]  # Ensures only authenticated users can access
    def get(self, request):
        material_id = request.query_params.get('material_id')
        material = Material.objects.all()
        if material_id:
            try:
                material = material.filter(pk=material_id)
            except Material.DoesNotExist:
                return Response({"error": "Material not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = MaterialSerializer(material, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = MaterialSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        try:
            material = Material.objects.get(pk=pk)
        except Material.DoesNotExist:
            return Response({"error": "Material not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = MaterialSerializer(material, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            material = Material.objects.get(pk=pk)
            material.delete()
            return Response({"message": "Material deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Material.DoesNotExist:
            return Response({"error": "Material not found"}, status=status.HTTP_404_NOT_FOUND)

class MaterialUploadDetailsCSVView(APIView):
    permission_classes = [IsAuthenticated]  # Ensures only authenticated users can access

    def post(self, request):
        # Check if file is provided
        if 'select_file' not in request.FILES:
            return Response({'error': 'Please select a CSV file for upload'}, status=status.HTTP_400_BAD_REQUEST)
        
        csv_file = request.FILES["select_file"]
        file_data = csv_file.read().decode("utf-8")
        csv_reader = csv.reader(file_data.splitlines())

        oldsub = ''
        oldchap = ''
        subid = 0
        chapid = 0
        no = 0

        for fields in csv_reader:
            no += 1
            if no == 1:  # Skip header row
                continue

            if len(fields) < 6:
                continue  # Skip invalid rows
            
            mat_type = fields[3].replace('///', ',').strip()
            mat_url = fields[4].replace('///', ',').strip()
            mat_desc = fields[5].replace('///', ',').strip()

            # Handling Subject
            subject_name = fields[0].replace('///', ',').strip()
            subject, created = Subject.objects.get_or_create(subject_name=subject_name)
            subid = subject.id

            # Handling Chapter
            chapter_name = fields[1].replace('///', ',').strip()
            chapter, created = Chapter.objects.get_or_create(chapter_name=chapter_name, subject_id=subid)
            chapid = chapter.id

            # Handling Topic
            topic_name = fields[2].replace('///', ',').strip()
            topic, created = Topic.objects.get_or_create(topic_name=topic_name, chapter_id=chapid)

            # Creating Material Entry
            Material.objects.create(
                subject_id=subid,
                chapter_id=chapid,
                topic=topic_name,
                mtype=mat_type,
                urlvalue=mat_url,
                description=mat_desc
            )

        return Response({'message': 'CSV data uploaded successfully'}, status=status.HTTP_201_CREATED)
    
    
class SessionMaterialAPIView(APIView):
    permission_classes = [IsAuthenticated]  # Ensures only authenticated users can access
    def get(self, request):
        sessionmaterial_id = request.query_params.get('sessionmaterial_id')
        sessionmaterial = SessionMaterial.objects.all()
        if sessionmaterial_id:
            try:
                sessionmaterial = sessionmaterial.filter(pk=sessionmaterial_id)
            except SessionMaterial.DoesNotExist:
                return Response({"error": "Session Material not found"}, status=status.HTTP_404_NOT_FOUND)
            
        serializer = SessionMaterialSerializer(sessionmaterial, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = SessionMaterialSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        try:
            sessionmaterial = SessionMaterial.objects.get(pk=pk)
        except SessionMaterial.DoesNotExist:
            return Response({"error": "Session Material not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = SessionMaterialSerializer(sessionmaterial, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            sessionmaterial = SessionMaterial.objects.get(pk=pk)
            sessionmaterial.delete()
            return Response({"message": "Session Material deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except SessionMaterial.DoesNotExist:
            return Response({"error": "Session Material not found"}, status=status.HTTP_404_NOT_FOUND)

class McqQuestionAPIView(APIView):
    permission_classes = [IsAuthenticated]  # Ensures only authenticated users can access
    def get(self, request):
        question_id = request.query_params.get('question_id')
        questions = McqQuestion.objects.all()
        if question_id:
            try:
                questions = questions.filter(pk=question_id)
            except McqQuestion.DoesNotExist:
                return Response({"error": "MCQ Question not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = McqQuestionSerializer(questions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = McqQuestionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        try:
            question = McqQuestion.objects.get(pk=pk)
        except McqQuestion.DoesNotExist:
            return Response({"error": "MCQ Question not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = McqQuestionSerializer(question, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            question = McqQuestion.objects.get(pk=pk)
            question.delete()
            return Response({"message": "MCQ Question deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except McqQuestion.DoesNotExist:
            return Response({"error": "MCQ Question not found"}, status=status.HTTP_404_NOT_FOUND)

class McqResultAPIView(APIView):
    permission_classes = [IsAuthenticated]  # Ensures only authenticated users can access
    def get(self, request):
        result_id = request.query_params.get('result_id')
        results = McqResult.objects.all()
        if result_id:
            try:
                results = results.filter(pk=result_id)
            except McqResult.DoesNotExist:
                return Response({"error": "MCQ Result not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = McqResultSerializer(results, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = McqResultSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        try:
            result = McqResult.objects.get(pk=pk)
        except McqResult.DoesNotExist:
            return Response({"error": "MCQ Result not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = McqResultSerializer(result, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            result = McqResult.objects.get(pk=pk)
            result.delete()
            return Response({"message": "MCQ Result deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except McqResult.DoesNotExist:
            return Response({"error": "MCQ Result not found"}, status=status.HTTP_404_NOT_FOUND)
        
class McqResultDetailsAPIView(APIView):
    permission_classes = [IsAuthenticated]  # Ensures only authenticated users can access
    def get(self, request):
        result_details_id = request.query_params.get('result_details_id')
        details = McqResultDetails.objects.all()
        if result_details_id:
            try:
                details = details.filter(pk=result_details_id)
            except McqResultDetails.DoesNotExist:
                return Response({"error": "MCQ Result Details not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = McqResultDetailsSerializer(details, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = McqResultDetailsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        try:
            detail = McqResultDetails.objects.get(pk=pk)
        except McqResultDetails.DoesNotExist:
            return Response({"error": "MCQ Result Details not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = McqResultDetailsSerializer(detail, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            detail = McqResultDetails.objects.get(pk=pk)
            detail.delete()
            return Response({"message": "MCQ Result Details deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except McqResultDetails.DoesNotExist:
            return Response({"error": "MCQ Result Details not found"}, status=status.HTTP_404_NOT_FOUND)

class ExamAPIView(APIView):
    permission_classes = [IsAuthenticated]  # Ensures only authenticated users can access
    def get(self, request):
        exam_id = request.query_params.get('exam_id')
        batch_id = request.query_params.get('batch_id')
        exams = Exam.objects.all()
        if exam_id:
            try:
                exams = exams.filter(pk=exam_id)
            except Exam.DoesNotExist:
                return Response({"error": "Exam not found"}, status=status.HTTP_404_NOT_FOUND)
        if batch_id:
            try:
                exams = exams.filter(batch_id=batch_id)
            except Exam.DoesNotExist:
                return Response({"error": "Batch not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = ExamSerializer(exams, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ExamSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        try:
            exam = Exam.objects.get(pk=pk)
        except Exam.DoesNotExist:
            return Response({"error": "Exam not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = ExamSerializer(exam, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            exam = Exam.objects.get(pk=pk)
            exam.delete()
            return Response({"message": "Exam deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Exam.DoesNotExist:
            return Response({"error": "Exam not found"}, status=status.HTTP_404_NOT_FOUND)

class ExamQuestionDetailsAPIView(APIView):
    permission_classes = [IsAuthenticated]  # Ensures only authenticated users can access
    def get(self, request):
        exam_id = request.query_params.get('exam_id')
        details = ExamQuestionDettails.objects.all()
        if exam_id:
            details = details.filter(exam_id=exam_id)

        serializer = ExamQuestionDettailsSerializer(details, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        exam_id = request.data.get('exam')
        mcq_question_id = request.data.get('mcqquestion')
        short_question_id = request.data.get('shortquestion')

        try:
            exam = Exam.objects.get(pk=exam_id)
        except Exam.DoesNotExist:
            return Response({"error": "Exam not found"}, status=status.HTTP_404_NOT_FOUND)

        if exam.questiontpye == 'MCQ' and not mcq_question_id:
            return Response({"error": "MCQ question required for MCQ type exam"}, status=status.HTTP_400_BAD_REQUEST)

        if exam.questiontpye == 'ShortAnswer' and not short_question_id:
            return Response({"error": "Short Answer question required for ShortAnswer type exam"}, status=status.HTTP_400_BAD_REQUEST)

        if mcq_question_id and short_question_id:
            return Response({"error": "Only one type of question (MCQ or Short) can be linked"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = ExamQuestionDettailsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        try:
            detail = ExamQuestionDettails.objects.get(pk=pk)
        except ExamQuestionDettails.DoesNotExist:
            return Response({"error": "Exam Question Detail not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = ExamQuestionDettailsSerializer(detail, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            detail = ExamQuestionDettails.objects.get(pk=pk)
            detail.delete()
            return Response({"message": "Exam Question Detail deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except ExamQuestionDettails.DoesNotExist:
            return Response({"error": "Exam Question Detail not found"}, status=status.HTTP_404_NOT_FOUND)

class ShortResultAPIView(APIView):
    permission_classes = [IsAuthenticated]  # Ensures only authenticated users can access
    def get(self, request):
        learner_id = request.query_params.get('learner_id')
        exam_id = request.query_params.get('exam_id')

        results = ShortResult.objects.all()
        if learner_id:
            results = results.filter(learner_id=learner_id)
        if exam_id:
            results = results.filter(exam_id=exam_id)

        serializer = ShortResultSerializer(results, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ShortResultSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        try:
            result = ShortResult.objects.get(pk=pk)
        except ShortResult.DoesNotExist:
            return Response({"error": "ShortResult not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = ShortResultSerializer(result, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            result = ShortResult.objects.get(pk=pk)
            result.delete()
            return Response({"message": "ShortResult deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except ShortResult.DoesNotExist:
            return Response({"error": "ShortResult not found"}, status=status.HTTP_404_NOT_FOUND)

class ShortResultDetailsAPIView(APIView):
    permission_classes = [IsAuthenticated]  # Ensures only authenticated users can access
    def get(self, request):
        short_result_id = request.query_params.get('short_result_id')
        details = ShortResultDetails.objects.all()

        if short_result_id:
            details = details.filter(shortresult_id=short_result_id)

        serializer = ShortResultDetailsSerializer(details, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ShortResultDetailsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        try:
            detail = ShortResultDetails.objects.get(pk=pk)
        except ShortResultDetails.DoesNotExist:
            return Response({"error": "ShortResultDetails not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = ShortResultDetailsSerializer(detail, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            detail = ShortResultDetails.objects.get(pk=pk)
            detail.delete()
            return Response({"message": "ShortResultDetails deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except ShortResultDetails.DoesNotExist:
            return Response({"error": "ShortResultDetails not found"}, status=status.HTTP_404_NOT_FOUND)
        
class ShortQuestionAPIView(APIView):
    permission_classes = [IsAuthenticated]  # Ensures only authenticated users can access
    def get(self, request):
        question_id = request.query_params.get('question_id')
        questions = ShortQuestion.objects.all()

        if question_id:
            questions = questions.filter(pk=question_id)

        serializer = ShortQuestionSerializer(questions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ShortQuestionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        try:
            question = ShortQuestion.objects.get(pk=pk)
        except ShortQuestion.DoesNotExist:
            return Response({"error": "ShortQuestion not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = ShortQuestionSerializer(question, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            question = ShortQuestion.objects.get(pk=pk)
            question.delete()
            return Response({"message": "ShortQuestion deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except ShortQuestion.DoesNotExist:
            return Response({"error": "ShortQuestion not found"}, status=status.HTTP_404_NOT_FOUND)
        
class PendingShortExamResultAPIView(APIView):
    permission_classes = [IsAuthenticated]  # Ensures only authenticated users can access
    def get(self, request):
            pending_results = ShortResult.objects.filter(
                learner__in=User.objects.all(),  # Filter learners
                exam__in=Exam.objects.all(),     # Filter exams
                status=False                      # Only pending results
            )
            
            # Serialize the results
            serializer = PendingShortExamResultSerializer(pending_results, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

class UpdateShortQuestionResultAPIView(APIView):
    permission_classes = [IsAuthenticated]  # Ensures only authenticated users can access
    def get(self, request, pk):
        # Get the ShortResultDetails associated with the given ShortResult (pk)
        resultdetails = ShortResultDetails.objects.filter(shortresult_id=pk)
        
        # Serialize the result details
        serializer = ShortResultDetailsSerializer(resultdetails, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    
    def put(self, request, pk):
        # Update the ShortResultDetails based on the provided pk (ID)
        resultdetails = ShortResultDetails.objects.get(pk=pk)
        serializer = ShortResultDetailsSerializer(resultdetails, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
class SaveShortQuestionResultAPIView(APIView):
    permission_classes = [IsAuthenticated]  # Ensures only authenticated users can access
    def post(self, request, pk):
        # Extract data from request
        feedback = request.data.get('newfeedback')
        marks = request.data.get('newmarks')
        qid = request.data.get('newqid')
        answer = request.data.get('newanswer')
        mainid = request.data.get('newmainid')

        # Update ShortResultDetails
        resultdetails = ShortResultDetails.objects.filter(id=pk).first()
        if resultdetails:
            resultdetails.delete()  # Delete the existing entry
        resultdetails = ShortResultDetails.objects.create(
            id=pk, marks=marks, feedback=feedback, question_id=qid, answer=answer, shortresult_id=mainid
        )
        resultdetails.save()

        # Recalculate total marks and update ShortResult
        totmarks = ShortResultDetails.objects.filter(shortresult_id=mainid).aggregate(Sum('marks'))['marks__sum']
        tot = ShortResultDetails.objects.filter(shortresult_id=mainid).count()
        totgiven = ShortResultDetails.objects.filter(shortresult_id=mainid, marks__gt=0).count()

        maintbl = ShortResult.objects.get(id=mainid)
        maintbl.marks = totmarks
        if tot == totgiven:
            maintbl.status = True
        maintbl.save()

        # Return response
        if tot == totgiven:
            resultdetails = ShortResultDetails.objects.filter(shortresult_id=mainid)
            serializer = ShortResultDetailsSerializer(resultdetails, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            resultdetails = ShortResultDetails.objects.filter(shortresult_id=mainid)
            serializer = ShortResultDetailsSerializer(resultdetails, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        
class LearnerChapterView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        learner = User.objects.raw('SELECT social_auth_usersocialauth.id, social_auth_usersocialauth.user_id, social_auth_usersocialauth.pic, auth_user.first_name, auth_user.last_name, GROUP_CONCAT(DISTINCT lxpapp_subject.name) AS courseset_name, lxpapp_learnerdetails.mobile FROM social_auth_usersocialauth LEFT OUTER JOIN auth_user ON (social_auth_usersocialauth.user_id = auth_user.id) LEFT OUTER JOIN lxpapp_batchlearner ON (auth_user.id = lxpapp_batchlearner.learner_id) LEFT OUTER JOIN lxpapp_batchrecordedvdolist ON (lxpapp_batchlearner.batch_id = lxpapp_batchrecordedvdolist.batch_id) LEFT OUTER JOIN lxpapp_subject ON (lxpapp_batchrecordedvdolist.subject_id = lxpapp_subject.id) LEFT OUTER JOIN lxpapp_learnerdetails ON (auth_user.id = lxpapp_learnerdetails.learner_id) WHERE (social_auth_usersocialauth.utype = 0 OR social_auth_usersocialauth.utype = 2) AND social_auth_usersocialauth.status = 1 GROUP BY social_auth_usersocialauth.id, social_auth_usersocialauth.user_id, auth_user.first_name, auth_user.last_name, lxpapp_learnerdetails.mobile ')
        
        # Process learner and return a response
        return Response({"learner": learner})

# API View for Learner Course Chapters
class LearnerChapterCourseView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        chapters = Subject.objects.raw('SELECT DISTINCT lxpapp_courseset.id, lxpapp_courseset.courseset_name, lxpapp_batchcourseset.batch_id FROM lxpapp_batchcourseset INNER JOIN lxpapp_courseset ON (lxpapp_batchcourseset.courseset_id = lxpapp_courseset.id) INNER JOIN lxpapp_batch ON (lxpapp_batchcourseset.batch_id = lxpapp_batch.id) INNER JOIN lxpapp_batchlearner ON (lxpapp_batchlearner.batch_id = lxpapp_batch.id) WHERE lxpapp_batchlearner.learner_id = %s', [user_id])
        return Response({"chapters": chapters})

# API View for Learner Course Subjects
class LearnerChapterCourseSubjectView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        subjects = Subject.objects.raw('SELECT ID AS id, NAME, VTOTAL, Mtotal, SUM(VWATCHED) AS VWatched,((100*VWATCHED)/VTOTAL) as per, THUMBNAIL_URL FROM (SELECT YYY.ID, YYY.NAME, YYY.THUMBNAIL_URL, ( SELECT COUNT(XX.ID) FROM LXPAPP_PLAYLISTITEM XX WHERE XX.PLAYLIST_ID = YYY.ID ) AS Vtotal, ( SELECT COUNT(zz.ID) FROM LXPAPP_sessionmaterial zz WHERE zz.PLAYLIST_ID = YYY.ID ) AS Mtotal, (SELECT COUNT (LXPAPP_VIDEOWATCHED.ID) AS a FROM LXPAPP_PLAYLISTITEM GHGH LEFT OUTER JOIN LXPAPP_VIDEOWATCHED ON ( GHGH.VIDEO_ID = LXPAPP_VIDEOWATCHED.VIDEO_ID ) WHERE GHGH.PLAYLIST_ID = YYY.ID AND LXPAPP_VIDEOWATCHED.LEARNER_ID = %s) AS VWatched FROM LXPAPP_BATCHLEARNER INNER JOIN LXPAPP_BATCH ON (LXPAPP_BATCHLEARNER.BATCH_ID = LXPAPP_BATCH.ID) INNER JOIN LXPAPP_BATCHRECORDEDVDOLIST ON (LXPAPP_BATCH.ID = LXPAPP_BATCHRECORDEDVDOLIST.BATCH_ID) INNER JOIN LXPAPP_PLAYLIST YYY ON (LXPAPP_BATCHRECORDEDVDOLIST.PLAYLIST_ID = YYY.ID) WHERE LXPAPP_BATCHLEARNER.LEARNER_ID = %s) GROUP BY ID, NAME, VTOTAL ORDER BY NAME', [user_id, user_id])

        chaptercount = LearnerSubjectCount.objects.all().filter(learner_id=user_id)
        countpresent = False
        if chaptercount:
            countpresent = True
        per = 0
        tc = 0
        wc = 0
        for x in subjects:
            if not chaptercount:
                countsave = LearnerSubjectCount.objects.create(subject_id=x.id, learner_id=user_id, count=x.Vtotal)
                countsave.save()
            tc += x.Vtotal
            wc += x.VWatched

        try:
            per = (100 * int(wc)) / int(tc)
        except:
            per = 0
        
        dif = tc - wc
        return Response({"subjects": subjects, "dif": dif, "per": per, "wc": wc, "tc": tc})

# API View for Learner Chapter List
class LearnerChapterListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, subject_id, user_id):
        subjectname = Subject.objects.only('name').get(id=subject_id).name
        list = Subject.objects.raw('SELECT DISTINCT mainvid.id, mainvid.name, IFNULL((SELECT lxpapp_chapterwatched.chapter_id FROM lxpapp_chapterwatched WHERE lxpapp_chapterwatched.learner_id = %s AND lxpapp_chapterwatched.chapter_id = mainvid.id), 0) AS watched, IFNULL((SELECT lxpapp_chaptertounlock.chapter_id FROM lxpapp_chaptertounlock WHERE lxpapp_chaptertounlock.learner_id = %s AND lxpapp_chaptertounlock.chapter_id = mainvid.id), 0) AS unlocked FROM lxpapp_chapter mainvid INNER JOIN lxpapp_subjectitem ON (mainvid.id = lxpapp_subjectitem.chapter_id) WHERE lxpapp_subjectitem.subject_id = %s AND mainvid.name <> "Deleted chapter"', [user_id, user_id, subject_id])
        return Response({"list": list, "subjectname": subjectname})

# API View for Approving Learner Chapter
class LearnerApproveChapterView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk, studid):
        unlock = ChapterToUnlock.objects.create(learner_id=studid, chapter_id=pk)
        unlock.save()
        return JsonResponse({"message": "Chapter unlocked successfully"})

# API View for Approving All Chapters in Subject
class LearnerApproveAllChapterView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, userid, subject_id):
        chapters = Subject.objects.raw('SELECT lxpapp_chapter.id FROM lxpapp_subjectitem INNER JOIN lxpapp_chapter ON (lxpapp_subjectitem.chapter_id = lxpapp_chapter.id) where lxpapp_subjectitem.subject_id = %s', [subject_id])
        for x in chapters:
            unlock = ChapterToUnlock.objects.create(learner_id=userid, chapter_id=x.id)
            unlock.save()
        return JsonResponse({"message": "All chapters unlocked successfully"})

# API View for Showing Learner Chapter
class LearnerShowChapterView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, subject_id, chapter_id):
        subjectname = Subject.objects.only('name').get(id=subject_id).name
        chapters = Chapter.objects.all().filter(id=chapter_id)
        topicname = ''
        url = ''
        for x in chapters:
            topicname = x.name
            url = "https://www.youtube.com/embed/" + x.chapter_id
        return Response({"topicname": topicname, "url": url, "subjectname": subjectname})

class ChapterQuestionAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        questions = ChapterQuestion.objects.all()
        serializer = ChapterQuestionSerializer(questions, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ChapterQuestionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ChapterQuestionDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            question = ChapterQuestion.objects.get(pk=pk)
        except ChapterQuestion.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        serializer = ChapterQuestionSerializer(question)
        return Response(serializer.data)

    def put(self, request, pk):
        try:
            question = ChapterQuestion.objects.get(pk=pk)
        except ChapterQuestion.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        serializer = ChapterQuestionSerializer(question, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            question = ChapterQuestion.objects.get(pk=pk)
        except ChapterQuestion.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        question.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ChapterResultAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        results = ChapterResult.objects.all()
        serializer = ChapterResultSerializer(results, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ChapterResultSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ChapterResultDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            result = ChapterResult.objects.get(pk=pk)
        except ChapterResult.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        serializer = ChapterResultSerializer(result)
        return Response(serializer.data)

    def put(self, request, pk):
        try:
            result = ChapterResult.objects.get(pk=pk)
        except ChapterResult.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        serializer = ChapterResultSerializer(result, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            result = ChapterResult.objects.get(pk=pk)
        except ChapterResult.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        result.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ChapterResultDetailsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        details = ChapterResultDetails.objects.all()
        serializer = ChapterResultDetailsSerializer(details, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ChapterResultDetailsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChapterResultDetailsDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            detail = ChapterResultDetails.objects.get(pk=pk)
        except ChapterResultDetails.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        serializer = ChapterResultDetailsSerializer(detail)
        return Response(serializer.data)

    def put(self, request, pk):
        try:
            detail = ChapterResultDetails.objects.get(pk=pk)
        except ChapterResultDetails.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        serializer = ChapterResultDetailsSerializer(detail, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            detail = ChapterResultDetails.objects.get(pk=pk)
        except ChapterResultDetails.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        detail.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ActivityAPIView(APIView):
    permission_classes = [IsAuthenticated]  # Ensures only authenticated users can access
    def get(self, request):
        activity_id = request.query_params.get('activity_id')
        activity = Activity.objects.all()
        if activity_id:
            try:
                activity = activity.filter(pk=activity_id)
            except Activity.DoesNotExist:
                return Response({"error": "Activity not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = ActivitySerializer(activity, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ActivitySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        try:
            activity = Activity.objects.get(pk=pk)
        except Activity.DoesNotExist:
            return Response({"error": "Activity not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = ActivitySerializer(activity, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            activity = Activity.objects.get(pk=pk)
            activity.delete()
            return Response({"message": "Activity deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Activity.DoesNotExist:
            return Response({"error": "Activity not found"}, status=status.HTTP_404_NOT_FOUND)

class ActivityUploadDetailsCSVAPIView(APIView):
    permission_classes = [IsAuthenticated]  # Ensures only authenticated users can access

    def post(self, request):
        # Check if file is provided
        if 'select_file' not in request.FILES:
            return Response({'error': 'Please select a CSV file for upload'}, status=status.HTTP_400_BAD_REQUEST)
        
        csv_file = request.FILES["select_file"]
        file_data = csv_file.read().decode("utf-8")
        csv_reader = csv.reader(file_data.splitlines())

        oldsub = ''
        oldchap = ''
        subid = 0
        chapid = 0
        no = 0

        for fields in csv_reader:
            no += 1
            if no == 1:  # Skip header row
                continue

            if len(fields) < 6:
                continue  # Skip invalid rows
            
            mat_type = fields[3].replace('///', ',').strip()
            mat_url = fields[4].replace('///', ',').strip()
            mat_desc = fields[5].replace('///', ',').strip()

            # Handling Subject
            subject_name = fields[0].replace('///', ',').strip()
            subject, created = Subject.objects.get_or_create(subject_name=subject_name)
            subid = subject.id

            # Handling Chapter
            chapter_name = fields[1].replace('///', ',').strip()
            chapter, created = Chapter.objects.get_or_create(chapter_name=chapter_name, subject_id=subid)
            chapid = chapter.id

            # Handling Topic
            topic_name = fields[2].replace('///', ',').strip()
            topic, created = Topic.objects.get_or_create(topic_name=topic_name, chapter_id=chapid)

            # Creating Activity Entry
            Activity.objects.create(
                subject_id=subid,
                chapter_id=chapid,
                topic=topic_name,
                mtype=mat_type,
                urlvalue=mat_url,
                description=mat_desc
            )

        return Response({'message': 'CSV data uploaded successfully'}, status=status.HTTP_201_CREATED)

class K8STerminalAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        K8STerminal_id = request.query_params.get('K8STerminal_id')
        terminals = K8STerminal.objects.all()
        if K8STerminal_id:
            terminals = terminals.filter(id = K8STerminal_id)
        serializer = K8STerminalSerializer(terminals, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = K8STerminalSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


