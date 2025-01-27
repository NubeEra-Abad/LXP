import logging
import threading
import traceback

from lxpapiapp.models import UserActivity, ErrorLog
class RequestMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        thread_locals = threading.local()
        thread_locals.request = request
        response = self.get_response(request)
        return response

    @staticmethod
    def get_current_request():
        return getattr(threading.local(), 'request', None)


class ErrorMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = None
        try:
            response = self.get_response(request)
        except Exception as e:
            logger = logging.getLogger(__name__)
            logger.exception('An error occurred during view processing')
            ErrorLog.objects.create(
                user=request.user,
                url=request.path,
                exception=str(e),
                traceback=traceback.format_exc()
            )
            raise e
        return response


class UserActivityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = None
        try:
            response = self.get_response(request)
        except Exception as e:
            logger = logging.getLogger(__name__)
            logger.exception('An error occurred during view processing')
            ErrorLog.objects.create(
                user=request.user,
                url=request.path,
                exception=str(e),
                traceback=traceback.format_exc()
            )
            raise e
        if request.user.is_authenticated and request.path != '/':
            UserActivity.objects.create(
                user=request.user,
                url=request.path,
                method=request.method,
                status_code=response.status_code if response else None
            )
        return response
