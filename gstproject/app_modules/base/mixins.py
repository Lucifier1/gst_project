from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.views.generic import ListView,CreateView,UpdateView,DeleteView,DetailView,View,TemplateView
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect

class SuperUserRequiredMixin:
    """
    Mixin to restrict access to superusers only.
    Redirect to respective homepages if the user does not meet the condition.
    """
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser and request.user.is_authenticated:
            if request.user.is_staff:
                return redirect("parentapp:parentlogin") 
            return redirect("userapp:userindex")  
        return super().dispatch(request, *args, **kwargs)
    
class StaffUserRequiredMixin:
    """
    Mixin to restrict access to staff users (not superusers).
    Redirect to respective homepages if the user does not meet the condition.
    """
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff and request.user.is_authenticated:
            if request.user.is_superuser:
                return redirect("adminapp:adminindex") 
            return redirect("userapp:userindex")  
        return super().dispatch(request, *args, **kwargs)
    