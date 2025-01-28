import jwt
import datetime
import uuid
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.permissions import IsAuthenticated

JITSI_SECRET = "a5f9c73e4d85e0c9f25b2d4394b6d24d5c00f27aaebef34f97f13a9f6f1c9ec7"
JITSI_SERVER = "https://34.235.128.110"  # Replace with your Jitsi Meet server IP

# Function to generate Jitsi token
def generate_jitsi_token(username, meeting_id, is_host):
    payload = {
        "context": {
            "user": {
                "name": username,  # Display name in the meeting
                "id": username     # Unique identifier
            }
        },
        "aud": "my_django_app",
        "iss": "my_django_app",
        "sub": JITSI_SERVER,
        "room": meeting_id,
        "exp": datetime.datetime.now() + datetime.timedelta(hours=1),
        "moderator": is_host
    }
    token = jwt.encode(payload, JITSI_SECRET, algorithm='HS256')
    return token


# API View for Generating Jitsi Token
@method_decorator(csrf_exempt, name='dispatch')  # Disable CSRF for simplicity
class JitsiTokenAPI(View):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        try:
            # Extract request data
            username = request.user.username  # Automatically uses the logged-in user
            meeting_id = request.POST.get("meeting_id", "")
            is_host = request.POST.get("is_host", "false").lower() == "true"

            # Validate inputs
            if not meeting_id:
                return JsonResponse({"error": "Meeting ID is required"}, status=400)

            # Generate the Jitsi token
            token = generate_jitsi_token(username, meeting_id, is_host)

            # Return the token
            return JsonResponse({"token": token, "meeting_link": f"https://{JITSI_SERVER}/{meeting_id}"}, status=200)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)