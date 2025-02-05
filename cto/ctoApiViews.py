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

    def get(self, request):
        subject_id = request.query_params.get('subject_id', None)
        subject_name = request.query_params.get('subject_name', None)

        # Filter the queryset based on the presence of subject_id and subject_name
        if subject_id and subject_name:
            subjects = Subject.objects.filter(id=subject_id, subject_name=subject_name)
        elif subject_id:
            subjects = Subject.objects.filter(id=subject_id)
        elif subject_name:
            subjects = Subject.objects.filter(subject_name=subject_name)
        else:
            subjects = Subject.objects.all()

        # Check if any subjects are found
        if not subjects.exists():
            return Response({"error": "No subjects found matching the criteria"}, status=status.HTTP_404_NOT_FOUND)

        # Serialize the result
        serializer = SubjectSerializer(subjects, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
       
        serializer = SubjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, subject_id):
        
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
        
        try:
            subject = Subject.objects.get(id=subject_id)
            subject.delete()
            return Response({"message": "Subject deleted successfully"}, status=status.HTTP_200_OK)
        except Subject.DoesNotExist:
            return Response({"error": "Subject not found"}, status=status.HTTP_404_NOT_FOUND)

class ChapterAPIView(APIView):
    permission_classes = [IsAuthenticated]
   
    def get(self, request):
        subject_id = request.query_params.get('subject_id')
        chapter_id = request.query_params.get('chapter_id')
        chapter_name = request.query_params.get('chapter_name')

        if chapter_id:
            try:
                chapter = Chapter.objects.get(pk=chapter_id)
                serializer = ChapterSerializer(chapter)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Chapter.DoesNotExist:
                return Response({"error": "Chapter not found."}, status=status.HTTP_404_NOT_FOUND)

        chapters = Chapter.objects.all()

        if subject_id:
            chapters = chapters.filter(subject_id=subject_id)

        if chapter_name:
            chapters = chapters.filter(chapter_name__icontains=chapter_name)

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
    def get(self, request):
        subject_id = request.query_params.get('subject_id')
        chapter_id = request.query_params.get('chapter_id')
        topic_id = request.query_params.get('topic_id')
        topic_name = request.query_params.get('topic_name')

        # Fetch a specific topic if topic_id is provided
        if topic_id:
            try:
                topic = Topic.objects.get(pk=topic_id)
                serializer = TopicSerializer(topic)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Topic.DoesNotExist:
                return Response({"error": "Topic not found."}, status=status.HTTP_404_NOT_FOUND)

        # Fetch topics based on filters
        topics = Topic.objects.all()

        if subject_id:
            topics = topics.filter(chapter__subject=subject_id)  # Assuming Topic has a ForeignKey to Subject

        if chapter_id:
            topics = topics.filter(chapter_id=chapter_id)  # Assuming Topic has a ForeignKey to Chapter

        if topic_name:
            topics = topics.filter(topic_name=topic_name)

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
        
class CategoryAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        category_id = request.query_params.get('category_id', None)
        category_name = request.query_params.get('category_name', None)

        # Filter the queryset based on the presence of category_id and category_name
        if category_id and category_name:
            categorys = Category.objects.filter(id=category_id, category_name=category_name)
        elif category_id:
            categorys = Category.objects.filter(id=category_id)
        elif category_name:
            categorys = Category.objects.filter(category_name=category_name)
        else:
            categorys = Category.objects.all()

        # Check if any categorys are found
        if not categorys.exists():
            return Response({"error": "No categorys found matching the criteria"}, status=status.HTTP_404_NOT_FOUND)

        # Serialize the result
        serializer = CategorySerializer(categorys, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
       
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, category_id):
        
        try:
            category = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            return Response({"error": "Category not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = CategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, category_id):
        
        try:
            category = Category.objects.get(id=category_id)
            category.delete()
            return Response({"message": "Category deleted successfully"}, status=status.HTTP_200_OK)
        except Category.DoesNotExist:
            return Response({"error": "Category not found"}, status=status.HTTP_404_NOT_FOUND)

class SubCategoryAPIView(APIView):
    permission_classes = [IsAuthenticated]
   
    def get(self, request):
        category_id = request.query_params.get('category_id')
        subcategory_id = request.query_params.get('subcategory_id')
        subcategory_name = request.query_params.get('subcategory_name')

        if subcategory_id:
            try:
                subcategory = SubCategory.objects.get(pk=subcategory_id)
                serializer = SubCategorySerializer(subcategory)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except SubCategory.DoesNotExist:
                return Response({"error": "Sub Category not found."}, status=status.HTTP_404_NOT_FOUND)

        subcategorys = SubCategory.objects.all()

        if category_id:
            subcategorys = subcategorys.filter(category_id=category_id)

        if subcategory_name:
            subcategorys = subcategorys.filter(subcategory_name__icontains=subcategory_name)

        serializer = SubCategorySerializer(subcategorys, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = SubCategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, subcategory_id):
        try:
            subcategory = SubCategory.objects.get(id=subcategory_id)
        except SubCategory.DoesNotExist:
            return Response({"error": "Sub Category not found."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = SubCategorySerializer(subcategory, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, subcategory_id):
        try:
            subcategory = SubCategory.objects.get(id=subcategory_id)
            subcategory.delete()
            return Response({"message": "Sub Category deleted successfully."}, status=status.HTTP_200_OK)
        except SubCategory.DoesNotExist:
            return Response({"error": "Sub Category not found."}, status=status.HTTP_404_NOT_FOUND)

class CourseAPIView(APIView):
    permission_classes = [IsAuthenticated]
   
    def get(self, request):
        category_id = request.query_params.get('category_id')
        subcategory_id = request.query_params.get('subcategory_id')
        course_name = request.query_params.get('course_name')

        # Fetch courses based on filters
        courses = Course.objects.all()

        if category_id:
            courses = courses.filter(category_id=category_id)  # Assuming Course has a ForeignKey to Category

        if subcategory_id:
            courses = courses.filter(subcategory_id=subcategory_id)  # Assuming Course has a ForeignKey to SubCategory

        if course_name:
            courses = courses.filter(course_name=course_name)  

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

class CourseChapterDetailView(APIView):
    def get(self, request, pk=None):
        if pk:
            try:
                # Get CourseChapter with the provided pk and course_id
                course_chapter = CourseChapter.objects.filter(course_id=pk)
                if course_chapter.exists():
                    serializer = CourseChapterSerializer(course_chapter, many=True)
                    return Response(serializer.data, status=status.HTTP_200_OK)
                else:
                    return Response({"error": "No chapters found for this course"}, status=status.HTTP_404_NOT_FOUND)
            except Course.DoesNotExist:
                return Response({"error": "Course not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            # If no pk is provided, return all course chapters
            course_chapters = CourseChapter.objects.all()
            serializer = CourseChapterSerializer(course_chapters, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
            
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
        