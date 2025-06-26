import re
from django.utils.deprecation import MiddlewareMixin
from app_modules.adminapp.models import UserVisit
from django.conf import settings
from django.shortcuts import redirect
# from user_agents import parse
from django.http import Http404
from django.db import IntegrityError

class CaptureUserInformationMiddleWare(MiddlewareMixin):

    def process_request(self, request):
        ip = self.get_client_ip(request)
        user_agent = request.META.get('HTTP_USER_AGENT', '')
        referrer = request.META.get('HTTP_REFERER', '')
        
        request.user_ip = ip
        request.user_agent = user_agent

    def process_response(self, request, response):
        ip = request.user_ip
        user_agent = request.user_agent
        referrer = request.META.get('HTTP_REFERER', '')
        try:
            ip_details = UserVisit.objects.filter(ip_address=ip, user_agent=user_agent).first()

            if ip_details:
                ip_details.visit_count += 1
                ip_details.save()
            else:
                ip_details = UserVisit.objects.create(ip_address=ip, user_agent=user_agent, referrer=referrer)

        except IntegrityError as e:
            print(f"Error occurred during saving or updating entry: {e}")
        except Exception as e:
            print(f"Unexpected error occurred: {e}")
        return response

    def get_client_ip(self, request):
        """Get the client IP address."""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

class HandleErrorsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            response = self.get_response(request)
        except Exception as e:
            # If an exception is raised, handle it by redirecting to the 404 page
            response = self.handle_error(request, e)
        return response

    def handle_error(self, request, exception):
        # Log the exception (optional, but good for debugging)
        # You can log this error to your logger to track issues
        if settings.DEBUG:
            print(f"Error occurred: {exception}")

        # Redirect to the default 404 page
        # return redirect('/404/')
        raise Http404("Page not found")
    