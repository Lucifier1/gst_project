from django.shortcuts import render,redirect
from django.views.generic import TemplateView,DeleteView,DetailView,CreateView,UpdateView,View
from django.contrib.auth.views import LoginView,LogoutView
from django.contrib import messages
from django.urls import reverse_lazy
from app_modules.userapp import forms
from django.contrib.auth import login,logout,authenticate
from app_modules.adminapp import models
from app_modules.adminapp.tasks import send_password_reset_email
import random
from django.contrib.auth.hashers import make_password
# Create your views here.


class UserIndexView(TemplateView):
    template_name = "userapp/index.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["basic_details"] = models.BasicDetails.objects.first()
        context["about_parameter"] = models.AboutParameter.objects.all()
        context["services"] = models.Services.objects.all()
        context["faq"] = models.FAQ.objects.all()
        context["testimonial"] = models.Testimonial.objects.all()
        context["blogs"] = models.Blog.objects.all()
        print(f' ==> [Line 24]: \033[38;2;213;62;59m[context]\033[0m({type(context).__name__}) = \033[38;2;105;158;28m{context}\033[0m')
        return context
   
class UserForgotPasswordView(TemplateView):
    template_name = "userapp/auth/forgot_password.html"
    
    def post(self,request):
        email = request.POST.get('email')
        try:
            user = models.User.objects.get(username=email)
            password = str(random.randrange(111111,999999))
            print(password)
            # user.set_password(f"GST{password}")
            user.password = make_password(password)
            user.is_forgotpassword = True
            user.save()
            print("finalll password",user.password)
            send_password_reset_email(password,email)
            print("mail send..........")
        except:
            print("Given email is not registered yet.")
            messages.error(request,"Given email is not registered yet.")
            return redirect("userapp:userforgotpassword")
        
        return redirect("userapp:userlogin")
    
class UserResetPassword(TemplateView):
    template_name = "userapp/auth/reset_password.html"
    
    def post(self,request):
        password = request.POST.get('password')
        password1 = request.POST.get('password1')
        if password != password1:
            messages.error(request, "Passwords do not match.")
            return render(request, self.template_name)
        try:
            user = models.User.objects.get(username=request.user.username)
            user.set_password(password)
            user.is_forgotpassword = False
            user.save()
            login(self.request,user)
            messages.success(request, "Your password has been reset successfully.")
            return redirect('userapp:userindex')
        except models.User.DoesNotExist:
            messages.error(request, "Error, User not found.")
            return render(request, self.template_name)
        except Exception as e:
            messages.error(request, "Error, ",e)
            return render(request, self.template_name)
        
class UserLoginView(LoginView):
    template_name = "userapp/auth/login.html"
    authentication_form = forms.CustomAuthenticationForm
    success_url = reverse_lazy("userapp:userindex")
    
    def form_valid(self, form):
        print("hiiiiiiiiiii")
        user = form.get_user()
        login(self.request,user)
        print(self.request.user)
        messages.success(self.request,f'Login Successfull')
        if self.request.user.role == "Admin":
            if self.request.user.is_forgotpassword:
                return redirect("userapp:userresetpassword")
            return redirect("adminapp:adminindex")
        elif self.request.user.role == "Customer":
            if self.request.user.is_forgotpassword:
                return redirect("userapp:userresetpassword")
            return redirect("userapp:userindex")
        else:
            return redirect("userapp:userindex")
        
    def form_invalid(self, form):
        response = super().form_invalid(form)
        print(form.errors)
        messages.error(self.request,f'Error, {form.errors}')
        return response
    
    
class UserRegisterView(TemplateView):
    template_name = "userapp/auth/register.html"
    
    

class UserLogoutView(LogoutView):
    template_name = "userapp/auth/login.html"
    
    def dispatch(self, request, *args, **kwargs):
        messages.success(request, "Logged Out Successfully")
        return super().dispatch(request, *args, **kwargs)

class UserChatView(TemplateView):
    template_name = "userapp/chat.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["users"] = models.User.objects.all().exclude(username=self.request.user.username)
        print(f' ==> [Line 111]: \033[38;2;175;143;159m[context]\033[0m({type(context).__name__}) = \033[38;2;21;207;98m{context}\033[0m')
        return context
    