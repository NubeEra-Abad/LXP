from lxpapiapp.models import *
from .ctoserializers import *
from rest_framework import status
from rest_framework.response import Response
import json
from rest_framework.views import APIView
from pathlib import Path
from rest_framework.permissions import IsAuthenticated
class SubjectAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    """
    API to handle CRUD operations for the Subject model.
    """

    def get(self, request, subject_id=None):
        """
        Retrieve all subjects or a specific subject by ID.

        GET:
        - If `subject_id` is provided, retrieve a single subject.
        - If no `subject_id` is provided, retrieve a list of all subjects.

        Path Parameter (Optional):
        - subject_id: ID of the subject to retrieve.

        Example Request (Single Subject):
        GET /api/cto/subject/1/

        Example Request (All Subjects):
        GET /api/cto/subject/

        Example Response (Single Subject):
        {
            "id": 1,
            "subject_name": "Mathematics"
        }

        Example Response (All Subjects):
        [
            {
                "id": 1,
                "subject_name": "Mathematics"
            },
            {
                "id": 2,
                "subject_name": "Science"
            }
        ]

        Returns:
        - 200 OK: On successful retrieval.
        - 404 Not Found: If the subject with the provided ID does not exist.
        
        Explanation of Paths:
        GET /api/cto/subject/

        Retrieves all subjects in the database.
        POST /api/cto/subject/

        Creates a new subject by accepting a JSON payload in the body.
        GET /api/cto/subject/<int:subject_id>/

        Retrieves a single subject by its ID.
        PUT /api/cto/subject/<int:subject_id>/

        Updates an existing subject with the provided subject_id using the JSON payload.
        DELETE /api/cto/subject/<int:subject_id>/

        Deletes the subject corresponding to the subject_id.
        """
        if subject_id:
            try:
                subject = Subject.objects.get(id=subject_id)
                serializer = SubjectSerializer(subject)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Subject.DoesNotExist:
                return Response({"error": "Subject not found"}, status=status.HTTP_404_NOT_FOUND)
        subjects = Subject.objects.all()
        serializer = SubjectSerializer(subjects, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """
        Create a new subject.

        POST:
        - Add a new subject by providing the required data.

        Request Body:
        {
            "subject_name": "Physics"
        }

        Example Response:
        {
            "id": 3,
            "subject_name": "Physics"
        }

        Returns:
        - 201 Created: On successful creation.
        - 400 Bad Request: If the request data is invalid.
        
        """
        serializer = SubjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, subject_id):
        """
        Update an existing subject by ID.

        PUT:
        - Update the `subject_name` of an existing subject.

        Path Parameter:
        - subject_id: ID of the subject to update.

        Request Body:
        {
            "subject_name": "Updated Subject Name"
        }

        Example Response:
        {
            "id": 1,
            "subject_name": "Updated Subject Name"
        }

        Returns:
        - 200 OK: On successful update.
        - 400 Bad Request: If the request data is invalid.
        - 404 Not Found: If the subject with the provided ID does not exist.
        """
        try:
            subject = Subject.objects.get(id=subject_id)
        except Subject.DoesNotExist:
            return Response({"error": "Subject not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = SubjectSerializer(subject, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, subject_id):
        """
        Delete a subject by ID.

        DELETE:
        - Removes the subject with the given ID.

        Path Parameter:
        - subject_id: ID of the subject to delete.

        Example Request:
        DELETE /api/cto/subject/1/

        Example Response:
        {
            "message": "Subject deleted successfully"
        }

        Returns:
        - 200 OK: On successful deletion.
        - 404 Not Found: If the subject with the provided ID does not exist.
        """
        try:
            subject = Subject.objects.get(id=subject_id)
            subject.delete()
            return Response({"message": "Subject deleted successfully"}, status=status.HTTP_200_OK)
        except Subject.DoesNotExist:
            return Response({"error": "Subject not found"}, status=status.HTTP_404_NOT_FOUND)

class ChapterAPIView(APIView):
    permission_classes = [IsAuthenticated]
    """
    API for CRUD operations on Chapter model.

    GET:
    - Retrieves all chapters.
    - Optional query parameter: `subject` (to filter by subject ID).

    POST:
    - Creates a new chapter.

    PUT:
    - Updates an existing chapter.

    DELETE:
    - Deletes an existing chapter.

    Example Request (POST):
    {
        "chapter_name": "Introduction to Physics",
        "subject": 1
    }

    Example Response (Success):
    {
        "id": 1,
        "chapter_name": "Introduction to Physics",
        "subject": 1
    }

    Example Response (Error):
    {
        "error": "Chapter not found."
    }
    
    Examples
        Filter Chapters by Subject
        Request: GET /api/chapter/?subject=1
        Response:
        [
            {
                "id": 1,
                "chapter_name": "Introduction to Physics",
                "subject": 1
            }
        ]
    """
    def get(self, request, chapter_id=None):
        if chapter_id:
            try:
                chapter = Chapter.objects.get(id=chapter_id)
                serializer = ChapterSerializer(chapter)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Chapter.DoesNotExist:
                return Response({"error": "Chapter not found."}, status=status.HTTP_404_NOT_FOUND)
        else:
            subject = request.query_params.get('subject')
            chapters = Chapter.objects.filter(subject=subject) if subject else Chapter.objects.all()
            serializer = ChapterSerializer(chapters, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ChapterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, chapter_id):
        try:
            chapter = Chapter.objects.get(id=chapter_id)
        except Chapter.DoesNotExist:
            return Response({"error": "Chapter not found."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = ChapterSerializer(chapter, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, chapter_id):
        try:
            chapter = Chapter.objects.get(id=chapter_id)
            chapter.delete()
            return Response({"message": "Chapter deleted successfully."}, status=status.HTTP_200_OK)
        except Chapter.DoesNotExist:
            return Response({"error": "Chapter not found."}, status=status.HTTP_404_NOT_FOUND)

class TopicAPIView(APIView):
    permission_classes = [IsAuthenticated]
    """
    API for CRUD operations on Topic model.

    GET:
    - Retrieves all topics.
    - Optional query parameters:
        - `subject` (filter by subject ID).
        - `chapter` (filter by chapter ID).
        - `subject` and `chapter` combined.

    POST:
    - Creates a new topic.

    PUT:
    - Updates an existing topic.

    DELETE:
    - Deletes an existing topic.

    Example Request (POST):
    {
        "topic_name": "Kinematics",
        "chapter": 1
    }

    Example Response (Success):
    {
        "id": 1,
        "topic_name": "Kinematics",
        "chapter": 1,
        "subject": 1
    }

    Example Response (Error):
    {
        "error": "Topic not found."
    }
    
    Filter Topics by Subject
    Request: GET /api/cto/topic/?subject=1
    Response:
    [
        {
            "id": 1,
            "topic_name": "Kinematics",
            "chapter": 1,
            "subject": 1
        }
    ]
    
    Filter Topics by Chapter
    Request: GET /api/cto/topic/?chapter=2
    Response:
    [
        {
            "id": 2,
            "topic_name": "Newton's Laws",
            "chapter": 2,
            "subject": 1
        }
    ]
    
    Filter Topics by Subject and Chapter
    Request: GET /api/cto/topic/?subject=1&chapter=2
    Response:
    [
        {
            "id": 2,
            "topic_name": "Newton's Laws",
            "chapter": 2,
            "subject": 1
        }
    ]


    """
    def get(self, request, topic_id=None):
        if topic_id:
            try:
                topic = Topic.objects.get(id=topic_id)
                serializer = TopicSerializer(topic)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Topic.DoesNotExist:
                return Response({"error": "Topic not found."}, status=status.HTTP_404_NOT_FOUND)
        else:
            subject = request.query_params.get('subject')
            chapter = request.query_params.get('chapter')
            if subject and chapter:
                topics = Topic.objects.filter(chapter__subject=subject, chapter=chapter)
            elif subject:
                topics = Topic.objects.filter(chapter__subject=subject)
            elif chapter:
                topics = Topic.objects.filter(chapter=chapter)
            else:
                topics = Topic.objects.all()
            serializer = TopicSerializer(topics, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = TopicSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, topic_id):
        try:
            topic = Topic.objects.get(id=topic_id)
        except Topic.DoesNotExist:
            return Response({"error": "Topic not found."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = TopicSerializer(topic, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, topic_id):
        try:
            topic = Topic.objects.get(id=topic_id)
            topic.delete()
            return Response({"message": "Topic deleted successfully."}, status=status.HTTP_200_OK)
        except Topic.DoesNotExist:
            return Response({"error": "Topic not found."}, status=status.HTTP_404_NOT_FOUND)                    
        
class MainHeadAPIView(APIView):
    permission_classes = [IsAuthenticated]
    """
    API for CRUD operations on MainHead model.

    GET:
    - Retrieves all mainheads.

    POST:
    - Creates a new mainhead.

    PUT:
    - Updates an existing mainhead.

    DELETE:
    - Deletes an existing mainhead.
    """
    def get(self, request, mainhead_id=None):
        if mainhead_id:
            try:
                mainhead = MainHead.objects.get(id=mainhead_id)
                serializer = MainHeadSerializer(mainhead)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except MainHead.DoesNotExist:
                return Response({"error": "MainHead not found."}, status=status.HTTP_404_NOT_FOUND)
        else:
            mainheads = MainHead.objects.all()
            serializer = MainHeadSerializer(mainheads, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = MainHeadSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, mainhead_id):
        try:
            mainhead = MainHead.objects.get(id=mainhead_id)
        except MainHead.DoesNotExist:
            return Response({"error": "MainHead not found."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = MainHeadSerializer(mainhead, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, mainhead_id):
        try:
            mainhead = MainHead.objects.get(id=mainhead_id)
            mainhead.delete()
            return Response({"message": "MainHead deleted successfully."}, status=status.HTTP_200_OK)
        except MainHead.DoesNotExist:
            return Response({"error": "MainHead not found."}, status=status.HTTP_404_NOT_FOUND)


class SubHeadAPIView(APIView):
    permission_classes = [IsAuthenticated]
    """
    API for CRUD operations on SubHead model.

    GET:
    - Retrieves all subheads.
    - Optional query parameter: `mainhead` (filter by mainhead ID).

    POST:
    - Creates a new subhead.

    PUT:
    - Updates an existing subhead.

    DELETE:
    - Deletes an existing subhead.
    """
    def get(self, request, subhead_id=None):
        if subhead_id:
            try:
                subhead = SubHead.objects.get(id=subhead_id)
                serializer = SubHeadSerializer(subhead)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except SubHead.DoesNotExist:
                return Response({"error": "SubHead not found."}, status=status.HTTP_404_NOT_FOUND)
        else:
            mainhead = request.query_params.get('mainhead')
            subheads = SubHead.objects.filter(mainhead=mainhead) if mainhead else SubHead.objects.all()
            serializer = SubHeadSerializer(subheads, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = SubHeadSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, subhead_id):
        try:
            subhead = SubHead.objects.get(id=subhead_id)
        except SubHead.DoesNotExist:
            return Response({"error": "SubHead not found."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = SubHeadSerializer(subhead, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, subhead_id):
        try:
            subhead = SubHead.objects.get(id=subhead_id)
            subhead.delete()
            return Response({"message": "SubHead deleted successfully."}, status=status.HTTP_200_OK)
        except SubHead.DoesNotExist:
            return Response({"error": "SubHead not found."}, status=status.HTTP_404_NOT_FOUND)

class CourseAPIView(APIView):
    permission_classes = [IsAuthenticated]
    """
    for CRUD operations on Course model.

    Endpoints:
    - GET: Retrieve all courses or a single course with its chapters.
    - POST: Create a new course with associated chapters.
    - PUT: Update an existing course along with its chapters.
    - DELETE: Delete a course and its associated chapters.

    Example Request (POST):
    {
        "course_name": "Advanced Mathematics",
        "description": "Learn advanced mathematics topics.",
        "whatlearn": "Calculus, Algebra, Geometry",
        "includes": "Video tutorials, Assignments",
        "themecolor": "1",
        "tags": "Math, Advanced",
        "image": "math.png",
        "banner": "math-banner.png",
        "price": 200,
        "mainhead": 1,
        "subhead": 1,
        "chapters": [
            {"subject": 1, "chapter": 1},
            {"subject": 2, "chapter": 3}
        ]
    }

    Example Response (Success):
    {
        "id": 1,
        "course_name": "Advanced Mathematics",
        "description": "Learn advanced mathematics topics.",
        "whatlearn": "Calculus, Algebra, Geometry",
        "includes": "Video tutorials, Assignments",
        "themecolor": "1",
        "tags": "Math, Advanced",
        "image": "math.png",
        "banner": "math-banner.png",
        "price": 200,
        "mainhead": 1,
        "subhead": 1,
        "chapters": [
            {
                "id": 1,
                "subject": 1,
                "subject_name": "Mathematics",
                "chapter": 1,
                "chapter_name": "Algebra"
            },
            {
                "id": 2,
                "subject": 2,
                "subject_name": "Science",
                "chapter": 3,
                "chapter_name": "Chemistry Basics"
            }
        ]
    }
"""
    def get(self, request, pk=None):
        if pk:
            try:
                course = Course.objects.get(pk=pk)
                serializer = CourseSerializer(course)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Course.DoesNotExist:
                return Response({"error": "Course not found"}, status=status.HTTP_404_NOT_FOUND)
        courses = Course.objects.all()
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = CourseCreateUpdateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        try:
            course = Course.objects.get(pk=pk)
        except Course.DoesNotExist:
            return Response({"error": "Course not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = CourseCreateUpdateSerializer(course, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            course = Course.objects.get(pk=pk)
            course.delete()
            return Response({"message": "Course deleted successfully"}, status=status.HTTP_200_OK)
        except Course.DoesNotExist:
            return Response({"error": "Course not found"}, status=status.HTTP_404_NOT_FOUND)
        
class SyncYouTubeAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:

            # Refresh the access token if expired
            def refresh_access_token():
                token_url = "https://oauth2.googleapis.com/token"
                response = requests.post(token_url, data={
                    'client_id': '522269335814-boqsbt800unpm7tcpt1jn3mlcfccgl5e.apps.googleusercontent.com',
                    'client_secret': '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',
                    'refresh_token': '1//046Ei7A7HevfJCgYIARAAGAQSNwF-L9IrKjrZ0MlK_0H2WAKAvqi0ONN2qBt4hamSwb-66HC45ZyHO6vcBCL_wsU2PduuODeQVhs',
                    'grant_type': 'refresh_token'
                })
                if response.status_code == 200:
                    new_access_token = response.json().get('access_token')
                    return new_access_token
                else:
                    raise Exception("Failed to refresh access token: " + response.text)
            access_token = 'ya29.a0AXeO80RsDxEKpN1GLeH_J_-HCRtVlIO4Z964aYIAq2zfMDtxto3u9cSj_KoLaPoAv7TSISqAPwor5PJR5Ygng4OjnEuobyaWWX6ufspAi2lQpVmdTOsPM5F2SOdD1vA24ogBGibpCi9BaUTrbOTG9AZdn7Q7nxh2MYkazlMsaCgYKAe4SARISFQHGX2MifS1VxHeK6T02eMbDrUzlOQ0175'
            # Use the access token
            if not access_token:
                access_token = refresh_access_token()

            headers = {
                'Authorization': f'Bearer {access_token}'
            }

            # Fetch playlists
            playlist_url = "https://www.googleapis.com/youtube/v3/playlists"
            playlist_response = requests.get(playlist_url, headers=headers, params={
                'part': 'id,snippet',
                'mine': 'true',
                'maxResults': 50
            })

            if playlist_response.status_code == 401:  # Unauthorized, refresh token
                access_token = refresh_access_token()
                headers['Authorization'] = f'Bearer {access_token}'
                playlist_response = requests.get(playlist_url, headers=headers, params={
                    'part': 'id,snippet',
                    'mine': 'true',
                    'maxResults': 50
                })

            if playlist_response.status_code != 200:
                return Response({"error": playlist_response.json()}, status=playlist_response.status_code)

            playlists = playlist_response.json().get('items', [])
            if not playlists:
                return Response({"message": "No playlists found."})

            synced_playlists = []
            for playlist in playlists:
                playlist_id = playlist['id']
                playlist_name = playlist['snippet']['title']

                # Check if the playlist already exists in the Subject model
                subject, created = Subject.objects.update_or_create(
                    subject_name=playlist_name,
                    defaults={'is_youtube': True}
                )

                # Fetch videos in the playlist
                videos_url = "https://www.googleapis.com/youtube/v3/playlistItems"
                videos_response = requests.get(videos_url, headers=headers, params={
                    'part': 'id,snippet',
                    'maxResults': 50,
                    'playlistId': playlist_id
                })

                videos = videos_response.json().get('items', [])
                for video in videos:
                    video_title = video['snippet']['title']

                    # Check if the video already exists in the Chapter model
                    Chapter.objects.update_or_create(
                        chapter_name=video_title,
                        subject=subject,
                        defaults={'is_youtube': True}
                    )

                synced_playlists.append({
                    "playlist_id": playlist_id,
                    "playlist_name": playlist_name,
                    "video_count": len(videos)
                })

            return Response({
                "message": "Playlists and videos synced successfully.",
                "data": synced_playlists
            })

        except Exception as e:
            return Response({"error": str(e)}, status=500)
        