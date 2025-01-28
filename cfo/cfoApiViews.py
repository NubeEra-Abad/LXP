from lxpapiapp.models import *
from .cfoserializers import *
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.db.models import Sum, Case, When, Value, Max
from django.db.models.functions import Coalesce
from django.http import JsonResponse

class CourseTypeAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, pk=None):
        """
        Retrieve one or all course types.
        """
        if pk:
            try:
                coursetype = CourseType.objects.get(pk=pk)
                serializer = CourseTypeSerializer(coursetype)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except CourseType.DoesNotExist:
                return Response({"error": "Course Type not found"}, status=status.HTTP_404_NOT_FOUND)
        coursetypes = CourseType.objects.all()
        serializer = CourseTypeSerializer(coursetypes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """
        Create a new course type.
        """
        serializer = CourseTypeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        """
        Update an existing course type.
        """
        try:
            coursetype = CourseType.objects.get(pk=pk)
        except CourseType.DoesNotExist:
            return Response({"error": "Course Type not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = CourseTypeSerializer(coursetype, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """
        Delete a course type.
        """
        try:
            coursetype = CourseType.objects.get(pk=pk)
            coursetype.delete()
            return Response({"message": "Course Type deleted successfully"}, status=status.HTTP_200_OK)
        except CourseType.DoesNotExist:
            return Response({"error": "Course Type not found"}, status=status.HTTP_404_NOT_FOUND)

class BatchAPIView(APIView):
    permission_classes = [IsAuthenticated]
    """
    for CRUD operations on Batch model.

    Endpoints:
    - GET: Retrieve all batches or a single batch with its courses, trainers, learners, and videos.
    - POST: Create a new batch with associated courses, trainers, learners, and videos.
    - PUT: Update an existing batch along with its associated data.
    - DELETE: Delete a batch and its associated data.

    Example Request (POST):
    {
        "batch_name": "Batch 101",
        "coursetype": 1,
        "stdate": "2025-01-01",
        "enddate": "2025-06-01",
        "courses": [{"course_name": "Math 101"}],
        "trainers": [{"trainer_name": "John Doe"}],
        "learners": [{"learner_name": "Alice", "fee": 1000.50}, {"learner_name": "Bob", "fee": 1200.00}],
        "videos": [{"video_title": "Math Introduction"}]
    }

    Example Response (Success):
    {
        "id": 1,
        "batch_name": "Batch 101",
        "coursetype": 1,
        "stdate": "2025-01-01",
        "enddate": "2025-06-01",
        "courses": [{"id": 1, "batch": 1, "course_name": "Math 101"}],
        "trainers": [{"id": 1, "batch": 1, "trainer_name": "John Doe"}],
        "learners": [
            {"id": 1, "batch": 1, "learner_name": "Alice", "fee": 1000.50},
            {"id": 2, "batch": 1, "learner_name": "Bob", "fee": 1200.00}
        ],
        "videos": [{"id": 1, "batch": 1, "video_title": "Math Introduction"}]
    }
    """

    def get(self, request, pk=None):
        if pk:
            try:
                batch = Batch.objects.get(pk=pk)
                serializer = BatchSerializer(batch)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Batch.DoesNotExist:
                return Response({"error": "Batch not found"}, status=status.HTTP_404_NOT_FOUND)
        
        batches = Batch.objects.all()
        serializer = BatchSerializer(batches, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = BatchSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        try:
            batch = Batch.objects.get(pk=pk)
        except Batch.DoesNotExist:
            return Response({"error": "Batch not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = BatchSerializer(batch, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            batch = Batch.objects.get(pk=pk)
            batch.delete()
            return Response({"message": "Batch deleted successfully"}, status=status.HTTP_200_OK)
        except Batch.DoesNotExist:
            return Response({"error": "Batch not found"}, status=status.HTTP_404_NOT_FOUND)        

class SchedulerAPIView(APIView):
    """
    API for managing Scheduler events
    """

    def get(self, request, pk=None):
        """
        Retrieve a single scheduler event or a list of all events.
        Optional: Filter by `trainer`, `subject`, `chapter`, or `type`.
        """
        if pk:
            try:
                scheduler = Scheduler.objects.get(pk=pk)
                serializer = SchedulerSerializer(scheduler)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Scheduler.DoesNotExist:
                return Response({"error": "Scheduler not found"}, status=status.HTTP_404_NOT_FOUND)
        
        # Filtering based on query parameters
        filters = {k: v for k, v in request.query_params.items() if k in ['trainer', 'subject', 'chapter', 'type']}
        schedulers = Scheduler.objects.filter(**filters)
        serializer = SchedulerSerializer(schedulers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """
        Create a new scheduler event.
        """
        serializer = SchedulerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        """
        Update an existing scheduler event.
        """
        try:
            scheduler = Scheduler.objects.get(pk=pk)
        except Scheduler.DoesNotExist:
            return Response({"error": "Scheduler not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = SchedulerSerializer(scheduler, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """
        Delete a scheduler event.
        """
        try:
            scheduler = Scheduler.objects.get(pk=pk)
            scheduler.delete()
            return Response({"message": "Scheduler deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Scheduler.DoesNotExist:
            return Response({"error": "Scheduler not found"}, status=status.HTTP_404_NOT_FOUND)

class SchedulerCalendarAPIView(APIView):
    """
    API to fetch Scheduler data with annotated fields: `status_sum` and `completion_date`.
    """
    permission_classes = [IsAuthenticated]
    def get(self, request):
        try:
            # Annotate the Scheduler queryset with additional calculated fields
            schedulers = Scheduler.objects.annotate(
                status_sum=Coalesce(Sum('schedulerstatus__status'), Value(0)),
                completion_date=Case(
                    When(status_sum__gte=100, then=Max('schedulerstatus__date')),
                    default=Value(None),
                )
            )

            # Serialize the data with annotations
            serialized_data = []
            for scheduler in schedulers:
                serialized_data.append({
                    "id": scheduler.id,
                    "trainer": scheduler.trainer.id if scheduler.trainer else None,
                    "type": scheduler.type,
                    "subject": scheduler.subject.id if scheduler.subject else None,
                    "chapter": scheduler.chapter.id if scheduler.chapter else None,
                    "topic": scheduler.topic.id if scheduler.topic else None,
                    "start": scheduler.start,
                    "end": scheduler.end,
                    "eventdetails": scheduler.eventdetails,
                    "meeting_link": scheduler.meeting_link,
                    "status_sum": scheduler.status_sum,
                    "completion_date": scheduler.completion_date,
                })

            return Response(serialized_data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
def get_meetings(request):
    """
    API to fetch all Scheduler meetings and return them as a JSON response.
    """
    try:
        # Query all meetings from the Scheduler model
        meetings = Scheduler.objects.all()

        # Prepare events list
        events = [
            {
                "title": f"{meeting.subject.subject_name if meeting.subject else meeting.eventdetails}",
                "start": meeting.start.isoformat(),
                "end": meeting.end.isoformat(),
                "meeting_link": meeting.meeting_link,
            }
            for meeting in meetings
        ]
        return JsonResponse(events, safe=False, status=200)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)