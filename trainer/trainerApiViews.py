from lxpapiapp.models import *
from .trainerserializers import *
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
from django.db import connection
from django.shortcuts import get_object_or_404
class SchedulerStatus(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        statuses = SchedulerStatus.objects.all()
        serializer = SchedulerStatusSerializer(statuses, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = SchedulerStatusSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, pk):
        try:
            status_entry = SchedulerStatus.objects.get(pk=pk)
        except SchedulerStatus.DoesNotExist:
            return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = SchedulerStatusSerializer(status_entry, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            status_entry = SchedulerStatus.objects.get(pk=pk)
        except SchedulerStatus.DoesNotExist:
            return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)

        status_entry.delete()
        return Response({"message": "Deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    
class SchedulerStatusMarkDone(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            data = request.data
            status_id = int(data.get('id'))  # Convert ID to integer

            # Get sum of all status values for this scheduler
            total_status = SchedulerStatus.objects.filter(scheduler_id=status_id).aggregate(
                total=Sum('status')
            )['total'] or 0

            if total_status < 100:
                remaining_status = 100 - total_status
                sch = SchedulerStatus.objects.create(
                    scheduler_id=status_id,
                    trainer=request.user,
                    status=remaining_status,
                    date=datetime.now().date()
                )
                sch.save()
                return Response({'success': True, 'message': 'Status marked as done.'}, status=status.HTTP_201_CREATED)
            else:
                return Response({'success': False, 'message': 'Status is already completed.'}, status=status.HTTP_400_BAD_REQUEST)

        except ValueError:
            return Response({'success': False, 'message': 'Invalid ID format.'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'success': False, 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class SchedulerStatusSum(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        scheduler_id = request.query_params.get("scheduler_id")

        if not scheduler_id:
            return Response({"error": "Missing scheduler_id"}, status=status.HTTP_400_BAD_REQUEST)

        # Get the sum of 'status' values for the given scheduler
        status_sum = SchedulerStatus.objects.filter(scheduler_id=scheduler_id).aggregate(Sum('status'))['status__sum'] or 0

        return Response({"status_sum": status_sum}, status=status.HTTP_200_OK)

class TrainerSchedulerCalendar(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        trainer_id = request.user.id  # Get the logged-in trainer's ID
        
        schedulers = Scheduler.objects.annotate(
            status_sum=Coalesce(Sum('schedulerstatus__status'), Value(0)),
            completion_date=Case(
                When(status_sum__gte=100, then=Max('schedulerstatus__date')),
                default=Value(None),
            )
        ).filter(trainer_id=trainer_id)

        # Serialize the data (assuming you have a SchedulerSerializer)
        serializer = TrainerSchedulerCalendarSerializer(schedulers, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

class ActivityLearnerList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Get learners associated with the trainer’s batches
        learners = User.objects.filter(
            batchlearner__batch__batchtrainer__trainer_id=request.user.id
        ).distinct().values('id', 'first_name', 'last_name')

        return Response(learners, status=status.HTTP_200_OK)
    
class ActivityLearnerBatchList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, learner_id):
        # SQL Query Execution
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT DISTINCT 
                    lxpapp_batch.batch_name,
                    lxpapp_course.course_name,
                    lxpapp_subject.subject_name,
                    lxpapp_chapter.chapter_name,
                    lxpapp_activity.description,
                    lxpapp_activity.id,
                    (SELECT COUNT(lxpapp_activityanswers.id) 
                     FROM lxpapp_activityanswers  
                     WHERE lxpapp_activityanswers.course_ID = lxpapp_course.id
                     AND lxpapp_activityanswers.learner_id = lxpapp_batchlearner.learner_id 
                     AND lxpapp_activityanswers.course_id = lxpapp_batchcourse.course_id) as anscount
                FROM lxpapp_batchtrainer
                LEFT OUTER JOIN lxpapp_batch ON (lxpapp_batchtrainer.batch_id = lxpapp_batch.id)
                LEFT OUTER JOIN lxpapp_batchlearner ON (lxpapp_batch.id = lxpapp_batchlearner.batch_id)
                LEFT OUTER JOIN lxpapp_batchcourse ON (lxpapp_batch.id = lxpapp_batchcourse.batch_id)
                LEFT OUTER JOIN lxpapp_course ON (lxpapp_batchcourse.course_id = lxpapp_course.id)
                LEFT OUTER JOIN lxpapp_coursechapter ON (lxpapp_course.id = lxpapp_coursechapter.course_id)
                LEFT OUTER JOIN lxpapp_chapter ON (lxpapp_coursechapter.chapter_id = lxpapp_chapter.id)
                LEFT OUTER JOIN lxpapp_subject ON (lxpapp_chapter.subject_id = lxpapp_subject.id)
                LEFT OUTER JOIN lxpapp_activity ON (lxpapp_activity.chapter_id = lxpapp_chapter.id)
                LEFT OUTER JOIN lxpapp_activityanswers ans ON (ans.activity_id = lxpapp_activity.id)
                WHERE lxpapp_activity.id IS NOT NULL 
                AND lxpapp_batchlearner.learner_id = %s 
                AND lxpapp_batchtrainer.trainer_id = %s
            """, [learner_id, request.user.id])

            results = [
                {
                    "batch_name": row[0],
                    "course_name": row[1],
                    "subject_name": row[2],
                    "chapter_name": row[3],
                    "description": row[4],
                    "activity_id": row[5],
                    "anscount": row[6] if row[6] is not None else 0
                }
                for row in cursor.fetchall()
            ]

        return Response(results, status=status.HTTP_200_OK)

class ActivityLearnerBatchActivity(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, activity_id):
        # Query activity answers with related activity details
        activities = ActivityAnswers.objects.filter(activity_id=activity_id).select_related('activity').values(
            'activity__description',
            'id',
            'file_url',
            'marks',
            'remarks',
            'status',
            'submitted_on'
        )

        results = list(activities)  # Convert QuerySet to list of dictionaries

        return Response(results, status=status.HTTP_200_OK)

class ActivityLearnerBatchActivityUpdate(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            data = request.data  # DRF automatically parses JSON

            activityanswer_id = data.get('id')
            marks = data.get('marks')
            status_value = data.get('status')
            remarks = data.get('remarks')

            # Validate required fields
            if activityanswer_id is None or marks is None or remarks is None:
                return Response({'status': 'error', 'message': 'Missing required fields'}, status=status.HTTP_400_BAD_REQUEST)

            # Get the ActivityAnswers object or return 404 if not found
            answer = get_object_or_404(ActivityAnswers, id=activityanswer_id)

            # Update fields
            answer.marks = marks
            answer.status = status_value
            answer.remarks = remarks
            answer.save()

            return Response({'status': 'success', 'message': 'Answer updated successfully'}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'status': 'error', 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)