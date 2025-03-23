from lxpapiapp.models import *
from .serializers import *
from django.http import JsonResponse
from rest_framework import permissions, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
import json
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework.permissions import AllowAny
from django.core.exceptions import ValidationError
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
from django.utils import timezone
from django.contrib.auth import update_session_auth_hash
from rest_framework.authtoken.models import Token
from django.contrib.auth import logout
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import ForeignKey
from django.apps import apps
from django.db import transaction
from django.core.files.storage import default_storage
import os
from django.conf import settings
from django.contrib.auth import login
from django.views import View
from django.shortcuts import render
from urllib.parse import urljoin
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView
from django.urls import reverse
from django.shortcuts import redirect

class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    callback_url = settings.GOOGLE_OAUTH_CALLBACK_URL
    client_class = OAuth2Client


class GoogleLoginCallback(APIView):
    def get(self, request, *args, **kwargs):
        """Accept callback request from Google OAuth screen.
        Extract code and send a POST request to Google authentication endpoint.

        If you are building a fullstack application (eg. with React app next to Django)
        you can place this endpoint in your frontend application to receive
        the JWT tokens there - and store them in the state
        """

        code = request.GET.get("code")

        if code is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        token_endpoint_url = urljoin("http://127.0.0.1:5566", reverse("google_login"))
        response = requests.post(url=token_endpoint_url, data={"code": code})

        return Response(response.json(), status=status.HTTP_200_OK)

def google_complete(request):
    # Get the authorization code from the query string
    code = request.GET.get('code')
    
    if not code:
        return JsonResponse({'error': 'Authorization code missing'}, status=400)

    # Step 1: Exchange the authorization code for an access token and refresh token
    token_url = 'https://oauth2.googleapis.com/token'

    data = {
        'code': code,
        'client_id': settings.SOCIAL_AUTH_GOOGLE_OAUTH2_KEY,
        'client_secret': settings.SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET,
        'redirect_uri': settings.GOOGLE_OAUTH_CALLBACK_URL,
        'grant_type': 'authorization_code',
    }

    response = requests.post(token_url, data=data)
    tokens = response.json()

    if response.status_code != 200:
        return JsonResponse({'error': 'Failed to get tokens'}, status=400)

    access_token = tokens.get('access_token')
    refresh_token = tokens.get('refresh_token')

    if not access_token or not refresh_token:
        return JsonResponse({'error': 'Tokens not found'}, status=400)

    # Step 2: Use the access token to fetch user information from Google
    user_info_url = 'https://www.googleapis.com/oauth2/v2/userinfo'
    headers = {
        'Authorization': f'Bearer {access_token}',
    }

    user_info_response = requests.get(user_info_url, headers=headers)
    user_info = user_info_response.json()

    # Get or create the user (based on the email returned from Google)
    user, created = User.objects.get_or_create(email=user_info.get('email'))

    # You can save the tokens in the user model or another table
    # user.profile.google_access_token = access_token
    # user.profile.google_refresh_token = refresh_token
    # user.profile.save()

    # Log the user in
    login(request, user)

    # Return a success response or redirect to the appropriate page
    return JsonResponse({'message': 'Google login successful', 'user_info': user_info})
  
def custom_logout(request):
    logout(request)  # Log the user out
    return redirect('login')  # Redirect to login page or homepage after logout
  
class LoginPage(View):
    def get(self, request, *args, **kwargs):
        return render(
            request,
            "pages/login.html",
            {
                "google_callback_uri": settings.GOOGLE_OAUTH_CALLBACK_URL,
                "google_client_id": settings.GOOGLE_OAUTH_CLIENT_ID,
            },
        )
@receiver(user_logged_in)
def post_login(sender, user, request, **kwargs):
    """
    Signal handler for when a user logs in.

    Triggered when the user successfully logs in via Django's built-in authentication system.

    Purpose:
    - Tracks the login time for the user.
    - Optionally fetches the user's profile picture if the user is not a staff member 
    - Stores the login time for use in subsequent events (e.g., when the user logs out).

    Args:
    - sender: The sender of the signal (typically the User model).
    - user: The user instance that has logged in.
    - request: The incoming request object.

    Returns:
    - Updates internal state, such as storing the `login_time` in memory or a temporary cache.

    Example Use Case:
    - This signal can be used to track when users log in, which is useful for auditing, user activity logs, or tracking session durations.
    

    Example Flow:
    1. User logs in.
    2. `post_login` signal is triggered.
    3. The login time is recorded and optionally, the user's profile picture is retrieved.
    4. This information can be used for session tracking or analytics.

    Example Response:
    - This handler doesn't return a response, but it processes the login time and potentially stores other data like profile pictures.
"""
    login_time = timezone.now()  # Use timezone-aware datetime

login_time = timezone.now()
logout_time  = timezone.now()
@receiver(user_logged_out)
def post_logout(sender, user, request, **kwargs):
    """
    Signal handler for when a user logs out.

    Triggered when the user successfully logs out via Django's built-in authentication system.

    Purpose:
    - Tracks the logout time for the user.
    - Calculates the session duration by subtracting the login time from the logout time.
    - Logs the session details (login time, logout time, and duration) into the `UserLog` model for auditing or analytics purposes.
    - Optionally clears old session data from the `LastUserLogin` model to maintain only the most recent session.

    Args:
    - sender: The sender of the signal (typically the User model).
    - user: The user instance that has logged out.
    - request: The incoming request object.

    Returns:
    - A `UserLog` entry is created that logs the user's session details, including the login time, logout time, and session duration.
    - Optionally, old session data can be cleared from the `LastUserLogin` model.

    Example Use Case:
    - This signal is useful for auditing purposes to track when users log out and how long their sessions last.
    - It can be used in applications where session duration is important, such as for user behavior analysis or monitoring.

    Example Flow:
    1. User logs out.
    2. `post_logout` signal is triggered.
    3. The logout time is recorded, and the duration of the session is calculated.
    4. A new `UserLog` entry is created to record the session details.
    5. Optionally, the system may clean up old user session data in the `LastUserLogin` model.

    Example Response:
    - This handler doesn't return a response but creates a log entry in the database that contains the session details.
"""
    logout_time = timezone.now()  # Use timezone-aware datetime
    duration = str(logout_time - login_time).split(".")[0]  # Ensure the duration is in proper format

    userlog = UserLog.objects.create(
        user=user,
        login=login_time,
        logout=logout_time,
        dur=duration
    )
    userlog.save()

    # Optionally clean up old LastUserLogin records if needed
    LastUserLogin.objects.all().delete()
class SignupAPIView(APIView):
    """
    API View for user registration (signup).

    POST:
    - Registers a new user with first name, last name, password, and email.
    - Automatically generates a unique username using the first name, last name, and the latest user ID.
    - Validates the provided data and creates a user if all fields are valid.

    Request Body:
    {
        "first_name": "John",
        "last_name": "Doe",
        "password": "examplepassword",
        "email": "john.doe@example.com"
    }

    Responses:
    - 201 Created: When the user is successfully registered.
    - 400 Bad Request: If any required fields are missing or there are validation errors.
    - 500 Internal Server Error: If there is an unexpected error during user creation.

    Example Response (Success):
    {
        "message": "User created successfully!",
        "username": "John_Doe_1"
    }

    Example Response (Failure):
    {
        "error": "All fields are required."
    }

    How to Use:
    1. Send a `POST` request to `/api/signup/` with the `first_name`, `last_name`, `password`, and `email` in the request body.
    2. The response will contain a success message along with the generated `username` if the registration is successful.
    3. If there is an error (e.g., missing fields or validation failure), the response will contain an error message.
    
    Example HTML Usage (Signup):
    <script>
      const signup = async () => {
        const response = await fetch('https://api.nubeera.com/api/signup/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            first_name: 'John',
            last_name: 'Doe',
            password: 'examplepassword',
            email: 'john.doe@example.com'
          })
        });

        if (response.ok) {
          const data = await response.json();
          console.log('Signup successful:', data);
        } else {
          console.log('Signup failed:', await response.json());
        }
      };
      signup();
    </script>
"""
    permission_classes = [AllowAny]
    
    def post(self, request):
        first_name = str(request.data.get('first_name', '')).strip()
        last_name = str(request.data.get('last_name', '')).strip()
        password = request.data.get('password', '').strip()
        email = request.data.get('email', '').strip()
        username = str(request.data.get('username', '')).strip()

        # Check for required fields
        if not first_name or not last_name or not password or not email or not username:
            return Response({"error": "All fields are required."}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the username already exists
        if User.objects.filter(username=username).exists():
            return Response({"error": "Username already exists."}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the email already exists
        if User.objects.filter(email=email).exists():
            return Response({"error": "Email already exists."}, status=status.HTTP_400_BAD_REQUEST)

        # Create the user
        try:
            new_user = User.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                username=username,
                password=password,
                email=email
            )
            new_user.full_clean()  # Validate the model instance
            new_user.save()
            return Response({"message": "User created successfully!", "username": username}, status=status.HTTP_201_CREATED)
        except ValidationError as ve:
            return Response({"error": ve.message_dict}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": f"Something went wrong: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class LoginAPI(APIView):
    """
    API View for user login and token generation.

    POST:
    - Authenticates the user with provided username and password.
    - If authentication is successful, generates a refresh token and an access token for the user.
    - Returns both tokens in the response.

    Request Body:
    {
        "username": "john_doe",
        "password": "examplepassword"
    }

    Responses:
    - 200 OK: If the credentials are valid, returns both refresh and access tokens.
    - 401 Unauthorized: If the credentials are invalid or authentication fails.

    Example Response:
    {
        "refresh": "refresh_token_value",
        "access": "access_token_value"
    }

    How to Use:
    1. Send a `POST` request to `/api/userlogin/` with the `username` and `password` of the user you want to authenticate.
    2. The response will include an `access` token and a `refresh` token if the credentials are correct.
    3. Store the `access` token securely, as it will be required for making authenticated requests to other protected endpoints.
    4. For expired tokens, use the `refresh` token to request a new `access` token via a refresh token API (if implemented).

    Example HTML Usage (Login):
    <script>
      const login = async () => {
        const response = await fetch('https://api.nubeera.com/api/login/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            username: 'john_doe',
            password: 'examplepassword'
          })
        });

        if (response.ok) {
          const data = await response.json();
          console.log('Login successful:', data);
          // Store access token for future requests
          localStorage.setItem('access_token', data.access);
        } else {
          console.log('Login failed:', await response.json());
        }
      };
      login();
    </script>
"""
    permission_classes = [AllowAny]
    
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        
        # Authenticate the user
        user = authenticate(username=username, password=password)
        
        if user is not None:
            # Create a refresh token for the user
            refresh = RefreshToken.for_user(user)
            
            # Return both access and refresh tokens
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_200_OK)
        
        return Response({
            'detail': 'Invalid credentials'
        }, status=status.HTTP_401_UNAUTHORIZED)

class LogoutAPIView(APIView):
    """
    API View to handle user logout.

    POST:
    - Logs out the authenticated user by invalidating their session and token.

    Responses:
    - 200 OK: If the user is successfully logged out.
    - 401 Unauthorized: If the user is not authenticated.

    Example Response (Success):
    {
        "message": "User logged out successfully."
    }

    Example Response (Failure):
    {
        "error": "Authentication credentials were not provided."
    }

    HTML Usage Example (Logout):
    <script>
      const logoutUser = async () => {
        const response = await fetch('/api/logout/', {
          method: 'POST',
          headers: {
            'Authorization': 'Token <your_auth_token>' // Replace with the user's token
          }
        });

        if (response.ok) {
          const data = await response.json();
          console.log('Logout successful:', data);
        } else {
          console.log('Logout failed:', await response.json());
        }
      };

      // Example call to logout
      logoutUser();
    </script>
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            # Invalidate the session
            logout(request)

            # If using token authentication, also delete the token
            token = Token.objects.get(user=request.user)
            token.delete()

            return Response({"message": "User logged out successfully."}, status=200)
        except Exception as e:
            return Response({"error": str(e)}, status=500)        
          
class ChangePasswordAPIView(APIView):
    """
    API view to handle password changes for authenticated users using JWT.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        current_password = request.data.get('current_password')
        new_password = request.data.get('new_password')

        if not current_password or not new_password:
            return Response({"error": "Both current and new passwords are required."}, status=status.HTTP_400_BAD_REQUEST)

        if not user.check_password(current_password):
            return Response({"error": "Invalid -- Authentication credentials were not provided."}, status=status.HTTP_400_BAD_REQUEST)

        # Set the new password
        user.set_password(new_password)

        try:
            user.save()  # Save the updated password

            # Create a new JWT token after the password change
            refresh = RefreshToken.for_user(user)
            access_token = refresh.access_token

            return Response({
                "message": "Password updated successfully.",
                "access_token": str(access_token),  # Send the new access token
                "refresh_token": str(refresh),      # Optionally, send the refresh token as well
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
          
class AdminViewUserList(APIView):
    """
    API View for retrieving the list of regular users (non-admins).

    GET:
    - Retrieves the list of users who are not superusers (non-admins).
    - Only accessible by superusers (admins).

    Responses:
    - 200 OK: Returns the list of users (excluding admins).
    - 403 Forbidden: If the authenticated user is not an admin.
    - 500 Internal Server Error: If an exception occurs during the process.
    
    USER_TYPE_CHOICES = (
        ("1", "TRAINER"),
        ("2", "LEARNER"),
        ("3", "CTO"),
        ("4", "CFO"),
        ("5","MENTOR"),
        ("6","STAFF"),
    )
    
    Example Response:
    {
        "users": [
            {
                "user_full_name": "Jane Doe",
                "email": "jane.doe@example.com",
                "utype": "Regular",
                "mobile": "1234567890",
                "whatsappno": "0987654321",
                "profile_pic": "url_to_image",
                "profile_updated": true,
                "status": true,
                "created": "2025-01-01T12:00:00Z",
                "is_superuser": false,
                "username": "jane_doe",
                "first_name": "Jane",
                "last_name": "Doe",
                "last_login": "2025-01-01T12:00:00Z"
            },
            {
                "user_full_name": "Bob Smith",
                "email": "bob.smith@example.com",
                "utype": "Regular",
                "mobile": "9876543210",
                "whatsappno": "0123456789",
                "profile_pic": "url_to_image",
                "profile_updated": false,
                "status": true,
                "created": "2024-12-25T10:30:00Z",
                "is_superuser": false,
                "username": "bob_smith",
                "first_name": "Bob",
                "last_name": "Smith",
                "last_login": "2025-01-10T08:45:00Z"
            }
        ]
    }

    How to Use:
    1. First, authenticate the user via the `/api/login/` endpoint to get the `access_token`.
    2. Send a `GET` request to `/api/admin/view-users/` with the `Authorization` header containing the `access_token`:
       ```
       Authorization: Bearer <access_token>
       ```
    3. If the authenticated user is a superuser (admin), the response will contain a list of non-admin users.
    4. If the user is not an admin, the response will return a `403 Forbidden` error.

    Example HTML Usage (Admin View User List):
    <script>
      const getUsers = async () => {
        const accessToken = localStorage.getItem('access_token');
        const response = await fetch('https://api.nubeera.com/api/admin/view-users/', {
          method: 'GET',
          headers: {
            'Authorization': `Bearer ${accessToken}`
          }
        });

        if (response.ok) {
          const data = await response.json();
          console.log('List of Users:', data.users);
        } else if (response.status === 403) {
          console.log('Unauthorized: User is not an admin');
        } else {
          console.log('Error:', await response.json());
        }
      };
      getUsers();
    </script>
"""
    permission_classes = [IsAuthenticated]  # Ensure only logged-in users can access
    
    def get(self, request, *args, **kwargs):
        try:
            
            # Check if the user is an admin
            if request.user.is_superuser:
                # Raw SQL query to get user information
                users = User.objects.all().filter(is_superuser=False)

                # Serialize the user data
                serializer = UserSerializer(users, many=True)

                # Return the serialized data as JSON response
                return Response({'users': serializer.data}, status=200)
            else:
                return Response({'detail': 'Unauthorized'}, status=403)

        except Exception as e:
            return Response({'detail': str(e)}, status=500)


class AdminViewUserLogDetailsAPIView(APIView):
    """
    API View to Retrieve User Log Details for Admins

    GET:
    - Retrieves all log details for a specific user identified by `user_id`.
    - Only accessible to authenticated users with admin privileges.

    URL Parameters:
    - `user_id` (int): The ID of the user whose log details are to be retrieved.

    Responses:
    - 200 OK: Returns a list of log details for the specified user.
    - 403 Forbidden: If the session user is not an admin.
    - 404 Not Found: If the specified user ID does not exist or has no logs.
    - 500 Internal Server Error: If there is an unexpected error.

    Example Response (Success):
    {
        "logs": [
            {
                "id": 1,
                "user_id": 42,
                "login": "2025-01-01T10:00:00Z",
                "logout": "2025-01-01T12:00:00Z",
                "dur": "2 hours",
                "session_id": "session_abc123"
            },
            {
                "id": 2,
                "user_id": 42,
                "login": "2025-01-02T09:00:00Z",
                "logout": "2025-01-02T11:30:00Z",
                "dur": "2.5 hours",
                "session_id": "session_xyz456"
            }
        ]
    }

    Example Response (Failure - Not Admin):
    {
        "error": "Access denied. Admin privileges required."
    }

    HTML Usage Example:
    <script>
      const getUserLogs = async (userId) => {
        const response = await fetch(`/api/admin/user-log-details/${userId}/`, {
          method: 'GET',
          headers: {
            'Authorization': 'Token <your_auth_token>' // Replace with the admin's token
          }
        });

        if (response.ok) {
          const data = await response.json();
          console.log('User Logs:', data.logs);
        } else {
          console.error('Failed to fetch user logs:', await response.json());
        }
      };

      // Example call
      getUserLogs(42);
    </script>
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id, *args, **kwargs):
        # Check if the user is an admin
        if not request.user.is_superuser:
            return Response({"error": "Access denied. Admin privileges required."}, status=403)

        try:
            # Retrieve the user log details
            logs = UserLog.objects.filter(user_id=user_id).values('id', 'user_id', 'login', 'logout', 'dur', 'session_id')
            if not logs:
                return Response({"error": "No logs found for this user."}, status=404)

            # Return the logs
            return Response({"logs": list(logs)}, status=200)
        except Exception as e:
            return Response({"error": str(e)}, status=500)

class AdminViewUserActivityDetailsAPIView(APIView):
    """
    API View to Retrieve User Activity Details for Admins

    GET:
    - Retrieves all activity details for a specific user identified by `user_id`.
    - Only accessible to authenticated users with admin privileges.

    URL Parameters:
    - `user_id` (int): The ID of the user whose activity details are to be retrieved.

    Responses:
    - 200 OK: Returns a list of activity details for the specified user.
    - 403 Forbidden: If the session user is not an admin.
    - 404 Not Found: If the specified user ID does not exist or has no activity.
    - 500 Internal Server Error: If there is an unexpected error.

    Example Response (Success):
    {
        "activities": [
            {
                "id": 1,
                "user_id": 42,
                "url": "/dashboard",
                "method": "GET",
                "status_code": 200,
                "timestamp": "2025-01-01T10:30:00Z"
            },
            {
                "id": 2,
                "user_id": 42,
                "url": "/quiz",
                "method": "POST",
                "status_code": 201,
                "timestamp": "2025-01-01T11:00:00Z"
            }
        ]
    }

    Example Response (Failure - Not Admin):
    {
        "error": "Access denied. Admin privileges required."
    }

    HTML Usage Example:
    <script>
      const getUserActivities = async (userId) => {
        const response = await fetch(`/api/admin/user-activity-details/${userId}/`, {
          method: 'GET',
          headers: {
            'Authorization': 'Token <your_auth_token>' // Replace with the admin's token
          }
        });

        if (response.ok) {
          const data = await response.json();
          console.log('User Activities:', data.activities);
        } else {
          console.error('Failed to fetch user activities:', await response.json());
        }
      };

      // Example call
      getUserActivities(42);
    </script>
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id, *args, **kwargs):
        # Check if the user is an admin
        if not request.user.is_superuser:
            return Response({"error": "Access denied. Admin privileges required."}, status=403)

        try:
            # Retrieve the user activity details
            activities = UserActivity.objects.filter(user_id=user_id).values('id', 'user_id', 'url', 'method', 'status_code', 'timestamp')
            if not activities:
                return Response({"error": "No activities found for this user."}, status=404)

            # Return the activities
            return Response({"activities": list(activities)}, status=200)
        except Exception as e:
            return Response({"error": str(e)}, status=500)

class AdminToggleUserStatusAPIView(APIView):
    """
    API View to Toggle User Status for Admins

    PUT:
    - Toggles the `status` (is_active) field of a user between `True` and `False`.
    - If `status` is currently `True`, it will be set to `False` (User Disabled).
    - If `status` is currently `False`, it will be set to `True` (User Enabled).
    - Only accessible to authenticated users with admin privileges.

    URL Parameters:
    - `user_id` (int): The ID of the user to toggle the status for.

    Responses:
    - 200 OK: If the user status is successfully toggled.
    - 403 Forbidden: If the session user is not an admin.
    - 404 Not Found: If the specified user ID does not exist.
    - 500 Internal Server Error: If there is an unexpected error.

    Example Response (Success - User Enabled):
    {
        "message": "User status changed successfully.",
        "user_id": 42,
        "status": "Enabled"
    }

    Example Response (Success - User Disabled):
    {
        "message": "User status changed successfully.",
        "user_id": 42,
        "status": "Disabled"
    }

    Example Response (Failure - Not Admin):
    {
        "error": "Access denied. Admin privileges required."
    }

    HTML Usage Example:
    <script>
      const toggleUserStatus = async (userId) => {
        const response = await fetch(`/api/admin/toggle-user-status/${userId}/`, {
          method: 'PUT',
          headers: {
            'Authorization': 'Token <your_auth_token>', // Replace with the admin's token
            'Content-Type': 'application/json'
          }
        });

        if (response.ok) {
          const data = await response.json();
          console.log('User Status Toggled:', data);
        } else {
          console.error('Failed to Toggle User Status:', await response.json());
        }
      };

      // Example call
      toggleUserStatus(42);
    </script>
    """
    permission_classes = [IsAuthenticated]

    def put(self, request, user_id, *args, **kwargs):
        if not request.user.is_superuser:
            return Response({"error": "Access denied. Admin privileges required."}, status=403)

        try:
            user = User.objects.filter(id=user_id).first()
            if not user:
                return Response({"error": "User not found."}, status=404)

            # Toggle the current status of the user (reverse it)
            current_status = user.is_active
            new_status = not current_status  # Reverse the status (True -> False, False -> True)
            user.is_active = new_status
            user.save()

            status_message = "Enabled" if new_status else "Disabled"

            return Response({
                "message": "User status changed successfully.",
                "user_id": user_id,
                "status": status_message
            }, status=200)

        except Exception as e:
            return Response({"error": str(e)}, status=500)

class DeleteUserAPIView(APIView):
    """
    API View to delete a non-admin user and their related data.

    DELETE:
    - Deletes the user and all associated data from related tables.
    - Only accessible by superusers.

    Responses:
    - 200 OK: If the user and their data were successfully deleted.
    - 400 Bad Request: If the provided user ID is invalid or the user is an admin.
    - 404 Not Found: If the user does not exist.
    - 401 Unauthorized: If the requester is not authenticated or is not a superuser.

    Example Response (Success):
    {
        "message": "User and associated data deleted successfully."
    }

    Example Response (Failure):
    {
        "error": "User is an admin and cannot be deleted."
    }

    Example Response (Failure):
    {
        "error": "User does not exist."
    }

    Example Response (Failure):
    {
        "error": "You do not have permission to delete users."
    }

    How to Use:
    1. Send a `DELETE` request to `/api/delete-user/<user_id>/` with the `user_id` in the URL.
    2. Include an Authorization header with the request:
        Authorization: Token <your_auth_token>
    3. If the user exists, is not an admin, and the requester is a superuser, the user and their associated data will be deleted.
    4. If there is an error (e.g., trying to delete an admin user, invalid user ID, or insufficient permissions), an error message will be returned.

    Example HTML Usage (Delete User):
    <script>
      const deleteUser = async (userId) => {
        const response = await fetch(`/api/delete-user/${userId}/`, {
          method: 'DELETE',
          headers: {
            'Authorization': 'Token <your_auth_token>' // Replace with the user's token
          }
        });

        if (response.ok) {
          const data = await response.json();
          console.log('User deleted:', data);
        } else {
          console.log('Deletion failed:', await response.json());
        }
      };

      // Example call to delete user with userId = 2
      deleteUser(2);
    </script>
"""
    permission_classes = [IsAuthenticated]

    def delete(self, request, user_id, *args, **kwargs):
        if not request.user.is_superuser:
            return Response({"error": "You do not have permission to delete users."}, status=401)

        try:
            user = User.objects.get(id=user_id)

            # Check if user is not an admin (superuser)
            if user.is_superuser:
                return Response({"error": "Admin users cannot be deleted."}, status=400)

            # Start a database transaction
            with transaction.atomic():
                # Get all models from the Django apps
                for model in apps.get_models():
                    # Find all related models that have a foreign key to User
                    for field in model._meta.fields:
                        if isinstance(field, ForeignKey) and field.related_model == User:
                            # Delete related objects for this model
                            model.objects.filter(**{field.name: user}).delete()

                # Now delete the user itself
                user.delete()

            return Response({"message": "User and associated data deleted successfully."}, status=200)

        except ObjectDoesNotExist:
            return Response({"error": "User does not exist."}, status=404)
        except Exception as e:
            return Response({"error": str(e)}, status=500)


class UserProfileView(APIView):
  """
    API View for updating user profile information.

    POST:
    - Updates the user profile including fields like first name, last name, full name, email, mobile, whatsappno, and profile picture.
    - Validates the provided data and updates the user if valid.
    - Optionally handles password update if old and new password are provided.
    - Returns an error if the old password does not match the current one or if the data is invalid.

    Request Body:
    {
        "first_name": "John",
        "last_name": "Doe",
        "user_full_name": "John Doe",
        "email": "john.doe@example.com",
        "mobile": "1234567890",
        "whatsappno": "9876543210",
        "old_password": "old_password123",  # Optional, used for password change
        "new_password": "new_password123",  # Optional, used for password change
        "profile_pic": "image_file.jpg"  # Optional, used for updating profile picture
    }

    Responses:
    - 200 OK: When the profile is successfully updated.
    - 400 Bad Request: If the provided data is invalid or the old password is incorrect.
    - 401 Unauthorized: If the user is not authenticated.

    Example Response (Success):
    {
        "message": "Profile updated successfully."
    }

    Example Response (Failure):
    {
        "error": "Invalid old password."
    }

    Example Response (Failure):
    {
        "error": "Invalid data provided."
    }

    How to Use:
    1. Send a `POST` request to `/api/user-profile/` with the data you want to update.
    2. Include an Authorization header with the request:
        Authorization: Token <your_auth_token>
    3. If the request is valid, the user profile will be updated and a success message will be returned.
    4. If there is an error, such as an invalid password or invalid data, an error message will be returned.

    Example HTML Usage (Update User Profile):
    <script>
      const updateUserProfile = async () => {
        const formData = new FormData();
        formData.append('first_name', 'John');
        formData.append('last_name', 'Doe');
        formData.append('user_full_name', 'John Doe');
        formData.append('email', 'john.doe@example.com');
        formData.append('mobile', '1234567890');
        formData.append('whatsappno', '9876543210');
        formData.append('profile_pic', document.getElementById('profile_pic_input').files[0]);
        formData.append('old_password', 'old_password123');
        formData.append('new_password', 'new_password123');
        
        const response = await fetch('/api/user-profile/', {
          method: 'POST',
          headers: {
            'Authorization': 'Token <your_auth_token>'  // Replace with your token
          },
          body: formData
        });

        if (response.ok) {
          const data = await response.json();
          console.log('Profile updated:', data);
        } else {
          console.log('Update failed:', await response.json());
        }
      };

      // Example usage to update profile
      updateUserProfile();
    </script>
"""
  permission_classes = [permissions.IsAuthenticated]
  def post(self, request, *args, **kwargs):
      user = request.user

      # Validate the data
      serializer = UserProfileSerializer(data=request.data)
      if serializer.is_valid():
          # Update user fields
          user.first_name = serializer.validated_data['first_name']
          user.last_name = serializer.validated_data['last_name']
          user.user_full_name = serializer.validated_data['user_full_name']
          user.email = serializer.validated_data['email']
          user.mobile = serializer.validated_data['mobile']
          user.whatsappno = serializer.validated_data['whatsappno']
          user.profile_updated = True
          # Handle profile picture upload
          profile_pic = request.FILES.get('profile_pic')
          if profile_pic:
              file_extension = os.path.splitext(profile_pic.name)[1]
              new_file_name = f"{user.username}_{user.id}{file_extension}"

              # Define file path and delete the old one if it exists
              file_path = user.profile_pic.storage.path(new_file_name)
              if default_storage.exists(new_file_name):
                  default_storage.delete(new_file_name)

              # Save the new profile picture
              user.profile_pic.save(new_file_name, profile_pic)

          # Check and update password if needed
          if 'old_password' in request.data:
              old_password = request.data['old_password']
              new_password = request.data['new_password']
              
              if user.check_password(old_password):
                  user.set_password(new_password)
                  user.profile_updated = True  # Assuming you have this field
                  user.save()
                  update_session_auth_hash(request, user)  # Keep the user logged in after password change
                  return Response({"message": "Profile updated successfully."}, status=status.HTTP_200_OK)
              else:
                  return Response({"error": "Invalid old password."}, status=status.HTTP_400_BAD_REQUEST)
          
          # Save user object after updates
          user.save()
          return Response({"message": "Profile updated successfully."}, status=status.HTTP_200_OK)

      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class UserInfoView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            # Fetch the user info based on the logged-in user
            user = request.user  # `request.user` will give the currently authenticated user
            
            # Serialize the data you want to return (e.g., user details)
            user_data = {
                'user_full_name': user.user_full_name,
                'email': user.email,
                'utype': user.utype,
                'mobile': user.mobile,
                'whatsappno': user.whatsappno,
                'profile_pic': user.profile_pic.url if user.profile_pic else None,
                'profile_updated': user.profile_updated,
                'status': user.status,
                'created': user.created,
                'skills': user.skills,
                'bio': user.bio,
                'regdate':user.regdate,
                'is_superuser':user.is_superuser
            }
            return Response(user_data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)