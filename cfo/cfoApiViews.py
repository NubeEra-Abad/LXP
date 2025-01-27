from lxpapiapp.models import *
from .cfoserializers import *
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

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