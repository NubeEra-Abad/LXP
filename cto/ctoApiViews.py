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
    def get(self, request, subject_id=None):
        
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
        
class CategoryAPIView(APIView):
    permission_classes = [IsAuthenticated]
   
  
    def get(self, request, category_id=None):
        if category_id:
            try:
                category = Category.objects.get(id=category_id)
                serializer = CategorySerializer(category)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Category.DoesNotExist:
                return Response({"error": "Category not found."}, status=status.HTTP_404_NOT_FOUND)
        else:
            categorys = Category.objects.all()
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
            return Response({"error": "Category not found."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = CategorySerializer(category, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, category_id):
        try:
            category = Category.objects.get(id=category_id)
            category.delete()
            return Response({"message": "Category deleted successfully."}, status=status.HTTP_200_OK)
        except Category.DoesNotExist:
            return Response({"error": "Category not found."}, status=status.HTTP_404_NOT_FOUND)


class SubCategoryAPIView(APIView):
    permission_classes = [IsAuthenticated]
  
    def get(self, request, subcategory_id=None):
        if subcategory_id:
            try:
                subcategory = SubCategory.objects.get(id=subcategory_id)
                serializer = SubCategorySerializer(subcategory)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except SubCategory.DoesNotExist:
                return Response({"error": "Sub Categorynot found."}, status=status.HTTP_404_NOT_FOUND)
        else:
            category = request.query_params.get('category')
            subcategorys = SubCategory.objects.filter(category=category) if category else SubCategory.objects.all()
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
            return Response({"error": "Sub Categorynot found."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = SubCategorySerializer(subcategory, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, subcategory_id):
        try:
            subcategory = SubCategory.objects.get(id=subcategory_id)
            subcategory.delete()
            return Response({"message": "Sub Categorydeleted successfully."}, status=status.HTTP_200_OK)
        except SubCategory.DoesNotExist:
            return Response({"error": "Sub Categorynot found."}, status=status.HTTP_404_NOT_FOUND)

class CourseAPIView(APIView):
    permission_classes = [IsAuthenticated]
   
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
        