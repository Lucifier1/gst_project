from django.shortcuts import render,redirect,HttpResponse
from django.views.generic import TemplateView,UpdateView,ListView,DetailView,DeleteView,View,CreateView
from django.urls import reverse_lazy
from django.core.mail import send_mail
from django.conf import settings
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from django.contrib import messages
from app_modules.adminapp import models
from app_modules.adminapp import forms
from django_datatables_too.mixins import DataTableMixin
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.utils.dateparse import parse_date
from django.db.models import Q
# Create your views here.


class AdminIndexView(TemplateView):
    template_name = "adminapp/index.html"
    
class AdminProfileView(TemplateView):
    template_name = "adminapp/profile.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    
    def post(self,request):
        data = models.User.objects.get(username=request.user)
        form = forms.UserForm(request.POST,instance=data)
        email = request.POST.get('email')
        try:
            models.User.objects.filter(username=email).exclude(data).exists()
            messages.error(request,'Error, Another Same Email Already Exists')
        except:
            if form.is_valid():
                form.save()
                messages.success(request,'Profile Updated Successfully')
            else:
                print(form.errors)
                messages.error(request,'Error, Please try again')
        return redirect("adminapp:adminprofile")
    
    
# class EmailSendView(TemplateView):
#     template_name = "adminapp/email_add.html"

#     def post(self,request,*args):
#         from_user = self.request.POST.get('from_user')
#         print(f' ==> [Line 13]: \033[38;2;188;96;123m[from_user]\033[0m({type(from_user).__name__}) = \033[38;2;237;38;119m{from_user}\033[0m')
#         to_user = self.request.POST.get('to_user')
#         print(f' ==> [Line 15]: \033[38;2;116;136;85m[to_user]\033[0m({type(to_user).__name__}) = \033[38;2;204;252;166m{to_user}\033[0m')
#         message = self.request.POST.get('message')
#         print(f' ==> [Line 17]: \033[38;2;25;199;155m[message]\033[0m({type(message).__name__}) = \033[38;2;139;23;222m{message}\033[0m')
#         title = self.request.POST.get('title')
#         print(f' ==> [Line 19]: \033[38;2;198;232;212m[title]\033[0m({type(title).__name__}) = \033[38;2;76;186;91m{title}\033[0m')
#         to_email = [to_user]
#         settings.EMAIL_HOST_USER = from_user
#         mailing = Mail(from_email=from_user,recipient_list=to_email,message=message,subject=title)
#         print(from_user) 
#         try:
#             sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
#             response = sg.send(message)
            
#             print(f"Email sent from {from_user} to {to_user}")
#             print(f"Response Status Code: {response.status_code}")
#             print(f"Response Body: {response.body}")
#             print(f"Response Headers: {response.headers}")
            
#             return HttpResponse("Email sent successfully.")
#         except Exception as e:
#             print(f"Error sending email: {e}")
#             return HttpResponse("Failed to send email.")
        
# --------------------------------------------------- BASIC_DETAILS --------------------------------------------------------

class BasicDetailsCreateView(CreateView):
    model = models.BasicDetails
    form_class = forms.BasicDetailsForm
    template_name = "adminapp/basicdetails_add.html"
    success_url = reverse_lazy("adminapp:basicdetails_list")
    
    def form_valid(self, form):
        form
        messages.success(self.request,'Basic Details Added Successfully')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        response = super().form_invalid(form)
        print(form.errors)
        messages.error(self.request,'Error, Please try again')
        return response
    
    
class BasicDetailsListView(ListView):
    model = models.BasicDetails
    template_name = "adminapp/basicdetails_list.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["basicdetails_data"] = models.BasicDetails.objects.first() 
        return context
    
    
class BasicDetailsUpdateView(UpdateView):
    model = models.BasicDetails
    form_class = forms.BasicDetailsForm
    template_name = "adminapp/basicdetails_update.html"
    success_url = reverse_lazy("adminapp:basicdetails_list")
    
    def form_valid(self, form):
        form
        messages.success(self.request,'Basic Details Updated Successfully')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        response = super().form_invalid(form)
        print(form.errors)
        messages.error(self.request,'Error, Please try again')
        return response
   
    
class BasicDetailsDeleteView(DeleteView):
    model = models.BasicDetails
    template_name = "adminapp/basicdetails_list.html"
    success_url = reverse_lazy("adminapp:basicdetails_list")

# --------------------------------------------------- FAQ_CRUD --------------------------------------------------------

class FAQCreateView(CreateView):
    model = models.FAQ
    form_class = forms.FAQForm
    template_name = "adminapp/faq_add.html"
    success_url = reverse_lazy("adminapp:faq_list")
    
    def form_valid(self, form):
        form
        messages.success(self.request,'FAQ Added Successfully')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        response = super().form_invalid(form)
        print(form.errors)
        messages.error(self.request,'Error, Please try again')
        return response
    
class FAQListView(ListView):
    model = models.FAQ
    template_name = "adminapp/faq_list.html"
    context_object_name = "faq_data"
    
class FAQUpdateView(UpdateView):
    model = models.FAQ
    form_class = forms.FAQForm
    template_name = "adminapp/faq_update.html"
    success_url = reverse_lazy("adminapp:faq_list")
    
    def form_valid(self, form):
        form
        messages.success(self.request,'FAQ Updated Successfully')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        response = super().form_invalid(form)
        print(form.errors)
        messages.error(self.request,'Error, Please try again')
        return response
    
class FAQDeleteView(DeleteView):
    model = models.FAQ
    template_name = "adminapp/faq_list.html"
    success_url = reverse_lazy("adminapp:faq_list")
    
    def form_valid(self, form):
        form
        messages.success(self.request,'FAQ Deleted Successfully')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        response = super().form_invalid(form)
        print(form.errors)
        messages.error(self.request,'Error, Please try again')
        return response
    
class FAQDatatableView(DataTableMixin,View):
    model = models.FAQ
    queryset = models.FAQ.objects.all().order_by('-id')
    
    def _get_actions(self, obj):
        """Get action buttons w/links."""
        return f'<a href="{obj.get_update_url()}" title="Edit" class="btn btn-primary btn-xs"><i class="fa fa-edit"></i></a> <a data-title="{obj}" title="Delete" onclick="showDeletemodal({obj.id})" data-bs-toggle="modal" class="btn btn-danger btn-xs btn-delete"><i class="fa fa-trash" style="color:white";></i></a>'
    def filter_queryset(self, qs):
        """Return the list of items for this view."""
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')
        if self.search:
            return qs.filter(
                #  Q(state__icontains=self.search) |
                Q(question__icontains=self.search) |
                Q(answer__icontains=self.search) 
            )
        if start_date and end_date:
            start_date = parse_date(start_date)
            end_date = parse_date(end_date)
            qs = qs.filter(created_at__gte=start_date, created_at__lte=end_date)
            return qs
        return qs
    def prepare_results(self, qs,start_index):
        data = []
        for index,o in enumerate(qs):
            global_index = start_index + index + 1
            data.append({
                'id': global_index,
                'question': o.question,
                'answer': o.answer,
                'actions': self._get_actions(o)
            })
        return data
    def get(self, request, *args, **kwargs):
        start = int(request.GET.get('start', 0))  
        length = int(request.GET.get('length', 10))
        queryset = self.filter_queryset(self.queryset)
        paginator = Paginator(queryset, length)
        page_number = (start // length) + 1  
        paginated_queryset = paginator.get_page(page_number)
        data = self.prepare_results(paginated_queryset,start)
        response_data = {
            'draw': int(request.GET.get('draw', 0)),  
            'recordsTotal': queryset.count(),  
            'recordsFiltered': paginator.count,
            'data': data  
        }
        return JsonResponse(response_data)
    

# --------------------------------------------------- CATEGORY-CRUD --------------------------------------------------------

class CategoryCreateView(CreateView):
    model = models.Category
    form_class = forms.CategoryForm
    template_name = "adminapp/category_add.html"
    success_url = reverse_lazy("adminapp:category_list")
    
    def form_valid(self, form):
        form
        messages.success(self.request,'Category Added Successfully')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        response = super().form_invalid(form)
        print(form.errors)
        messages.error(self.request,'Error, Please try again')
        return response
    
class CategoryListView(ListView):
    model = models.Category
    template_name = "adminapp/category_list.html"
    context_object_name = "category_data"
    
class CategoryUpdateView(UpdateView):
    model = models.Category
    form_class = forms.CategoryForm
    template_name = "adminapp/category_update.html"
    success_url = reverse_lazy("adminapp:category_list")
    
    def form_valid(self, form):
        form
        messages.success(self.request,'Category Updated Successfully')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        response = super().form_invalid(form)
        print(form.errors)
        messages.error(self.request,'Error, Please try again')
        return response
    
class CategoryDeleteView(DeleteView):
    model = models.Category
    template_name = "adminapp/category_list.html"
    success_url = reverse_lazy("adminapp:category_list")
    
    def form_valid(self, form):
        form
        messages.success(self.request,'Category Deleted Successfully')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        response = super().form_invalid(form)
        print(form.errors)
        messages.error(self.request,'Error, Please try again')
        return response
    
class CategoryDatatableView(DataTableMixin,View):
    model = models.Category
    queryset = models.Category.objects.all().order_by('-id')
    
    def _get_actions(self, obj):
        """Get action buttons w/links."""
        return f'<a href="{obj.get_update_url()}" title="Edit" class="btn btn-primary btn-xs"><i class="fa fa-edit"></i></a> <a data-title="{obj}" title="Delete" onclick="showDeletemodal({obj.id})" data-bs-toggle="modal" class="btn btn-danger btn-xs btn-delete"><i class="fa fa-trash" style="color:white";></i></a>'
    def filter_queryset(self, qs):
        """Return the list of items for this view."""
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')
        if self.search:
            return qs.filter(
                #  Q(state__icontains=self.search) |
                Q(name__icontains=self.search) 
            )
        if start_date and end_date:
            start_date = parse_date(start_date)
            end_date = parse_date(end_date)
            qs = qs.filter(created_at__gte=start_date, created_at__lte=end_date)
            return qs
        return qs
    def prepare_results(self, qs,start_index):
        data = []
        for index,o in enumerate(qs):
            global_index = start_index + index + 1
            data.append({
                'id': global_index,
                'name': o.name,
                'actions': self._get_actions(o)
            })
        return data
    def get(self, request, *args, **kwargs):
        start = int(request.GET.get('start', 0))  
        length = int(request.GET.get('length', 10))
        queryset = self.filter_queryset(self.queryset)
        paginator = Paginator(queryset, length)
        page_number = (start // length) + 1  
        paginated_queryset = paginator.get_page(page_number)
        data = self.prepare_results(paginated_queryset,start)
        response_data = {
            'draw': int(request.GET.get('draw', 0)),  
            'recordsTotal': queryset.count(),  
            'recordsFiltered': paginator.count,
            'data': data  
        }
        return JsonResponse(response_data)
    

# --------------------------------------------------- BLOG-CRUD --------------------------------------------------------

class BlogCreateView(CreateView):
    model = models.Blog
    form_class = forms.BlogForm
    template_name = "adminapp/blog_add.html"
    success_url = reverse_lazy("adminapp:blog_list")
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category"] = models.Category.objects.all() 
        return context
        
    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        obj.save()
        messages.success(self.request,'Blog Added Successfully')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        response = super().form_invalid(form)
        print(form.errors)
        messages.error(self.request,'Error, Please try again')
        return response
    
class BlogListView(ListView):
    model = models.Blog
    template_name = "adminapp/blog_list.html"
    context_object_name = "blog_data"
    
class BlogUpdateView(UpdateView):
    model = models.Blog
    form_class = forms.BlogForm
    template_name = "adminapp/blog_update.html"
    success_url = reverse_lazy("adminapp:blog_list")
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category"] = models.Category.objects.all() 
        return context
    
    def form_valid(self, form):
        form
        messages.success(self.request,'Blog Updated Successfully')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        response = super().form_invalid(form)
        print(form.errors)
        messages.error(self.request,'Error, Please try again')
        return response
    
class BlogDeleteView(DeleteView):
    model = models.Blog
    template_name = "adminapp/blog_list.html"
    success_url = reverse_lazy("adminapp:blog_list")
    
    def form_valid(self, form):
        form
        messages.success(self.request,'Blog Deleted Successfully')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        response = super().form_invalid(form)
        print(form.errors)
        messages.error(self.request,'Error, Please try again')
        return response
    
class BlogDatatableView(DataTableMixin,View):
    model = models.Blog
    queryset = models.Blog.objects.all().order_by('-id')
    
    def _get_actions(self, obj):
        """Get action buttons w/links."""
        return f'<a href="{obj.get_update_url()}" title="Edit" class="btn btn-primary btn-xs"><i class="fa fa-edit"></i></a> <a data-title="{obj}" title="Delete" onclick="showDeletemodal({obj.id})" data-bs-toggle="modal" class="btn btn-danger btn-xs btn-delete"><i class="fa fa-trash" style="color:white";></i></a>'
    def filter_queryset(self, qs):
        """Return the list of items for this view."""
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')
        if self.search:
            return qs.filter(
                #  Q(state__icontains=self.search) |
                Q(title__icontains=self.search) |
                Q(description__icontains=self.search) |
                Q(category__name__icontains=self.search) 
            )
        if start_date and end_date:
            start_date = parse_date(start_date)
            end_date = parse_date(end_date)
            qs = qs.filter(created_at__gte=start_date, created_at__lte=end_date)
            return qs
        return qs
    def prepare_results(self, qs,start_index):
        data = []
        for index,o in enumerate(qs):
            global_index = start_index + index + 1
            data.append({
                'id': global_index,
                'title': o.title,
                'category': o.category.name,
                'description': o.description,
                'image': o.image.url,
                'actions': self._get_actions(o)
            })
        return data
    def get(self, request, *args, **kwargs):
        start = int(request.GET.get('start', 0))  
        length = int(request.GET.get('length', 10))
        queryset = self.filter_queryset(self.queryset)
        paginator = Paginator(queryset, length)
        page_number = (start // length) + 1  
        paginated_queryset = paginator.get_page(page_number)
        data = self.prepare_results(paginated_queryset,start)
        response_data = {
            'draw': int(request.GET.get('draw', 0)),  
            'recordsTotal': queryset.count(),  
            'recordsFiltered': paginator.count,
            'data': data  
        }
        return JsonResponse(response_data)
   

# --------------------------------------------------- TESTIMONIAL-CRUD --------------------------------------------------------

class TestimonialCreateView(CreateView):
    model = models.Testimonial
    form_class = forms.TestimonialForm
    template_name = "adminapp/testimonial_add.html"
    success_url = reverse_lazy("adminapp:testimonial_list")
    
    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        obj.save()
        messages.success(self.request,'Testimonial Added Successfully')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        response = super().form_invalid(form)
        print(form.errors)
        messages.error(self.request,'Error, Please try again')
        return response
    
class TestimonialListView(ListView):
    model = models.Testimonial
    template_name = "adminapp/testimonial_list.html"
    context_object_name = "testimonial_data"
    
class TestimonialUpdateView(UpdateView):
    model = models.Testimonial
    form_class = forms.TestimonialForm
    template_name = "adminapp/testimonial_update.html"
    success_url = reverse_lazy("adminapp:testimonial_list")
    
    def form_valid(self, form):
        form
        messages.success(self.request,'Testimonial Updated Successfully')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        response = super().form_invalid(form)
        print(form.errors)
        messages.error(self.request,'Error, Please try again')
        return response
    
class TestimonialDeleteView(DeleteView):
    model = models.Testimonial
    template_name = "adminapp/testimonial_list.html"
    success_url = reverse_lazy("adminapp:testimonial_list")
    
    def form_valid(self, form):
        form
        messages.success(self.request,'Testimonial Deleted Successfully')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        response = super().form_invalid(form)
        print(form.errors)
        messages.error(self.request,'Error, Please try again')
        return response
    
class TestimonialDatatableView(DataTableMixin,View):
    model = models.Testimonial
    queryset = models.Testimonial.objects.all().order_by('-id')
    
    def _get_actions(self, obj):
        """Get action buttons w/links."""
        return f'<a href="{obj.get_update_url()}" title="Edit" class="btn btn-primary btn-xs"><i class="fa fa-edit"></i></a> <a data-title="{obj}" title="Delete" onclick="showDeletemodal({obj.id})" data-bs-toggle="modal" class="btn btn-danger btn-xs btn-delete"><i class="fa fa-trash" style="color:white";></i></a>'
    def filter_queryset(self, qs):
        """Return the list of items for this view."""
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')
        if self.search:
            return qs.filter(
                #  Q(state__icontains=self.search) |
                Q(title__icontains=self.search) |
                Q(description__icontains=self.search) |
                Q(user__first_name__icontains=self.search) |
                Q(user__last_name__icontains=self.search) 
            )
        if start_date and end_date:
            start_date = parse_date(start_date)
            end_date = parse_date(end_date)
            qs = qs.filter(created_at__gte=start_date, created_at__lte=end_date)
            return qs
        return qs
    def prepare_results(self, qs,start_index):
        data = []
        for index,o in enumerate(qs):
            global_index = start_index + index + 1
            user_data = o.user.first_name + " " + o.user.last_name
            data.append({
                'id': global_index,
                'title': o.title,
                'description': o.description,
                'user': user_data,
                'actions': self._get_actions(o)
            })
        return data
    def get(self, request, *args, **kwargs):
        start = int(request.GET.get('start', 0))  
        length = int(request.GET.get('length', 10))
        queryset = self.filter_queryset(self.queryset)
        paginator = Paginator(queryset, length)
        page_number = (start // length) + 1  
        paginated_queryset = paginator.get_page(page_number)
        data = self.prepare_results(paginated_queryset,start)
        response_data = {
            'draw': int(request.GET.get('draw', 0)),  
            'recordsTotal': queryset.count(),  
            'recordsFiltered': paginator.count,
            'data': data  
        }
        return JsonResponse(response_data)
   

# --------------------------------------------------- SERVICES-CRUD --------------------------------------------------------

class ServicesCreateView(CreateView):
    model = models.Services
    form_class = forms.ServicesForm
    template_name = "adminapp/services_add.html"
    success_url = reverse_lazy("adminapp:services_list")
    
    def form_valid(self, form):
        form
        messages.success(self.request,'Services Added Successfully')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        response = super().form_invalid(form)
        print(form.errors)
        messages.error(self.request,'Error, Please try again')
        return response
    
class ServicesListView(ListView):
    model = models.Services
    template_name = "adminapp/services_list.html"
    context_object_name = "services_data"
    
class ServicesUpdateView(UpdateView):
    model = models.Services
    form_class = forms.ServicesForm
    template_name = "adminapp/services_update.html"
    success_url = reverse_lazy("adminapp:services_list")
    
    def form_valid(self, form):
        form
        messages.success(self.request,'Services Updated Successfully')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        response = super().form_invalid(form)
        print(form.errors)
        messages.error(self.request,'Error, Please try again')
        return response
    
class ServicesDeleteView(DeleteView):
    model = models.Services
    template_name = "adminapp/services_list.html"
    success_url = reverse_lazy("adminapp:services_list")
    
    def form_valid(self, form):
        form
        messages.success(self.request,'Services Deleted Successfully')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        response = super().form_invalid(form)
        print(form.errors)
        messages.error(self.request,'Error, Please try again')
        return response
    
class ServicesDatatableView(DataTableMixin,View):
    model = models.Services
    queryset = models.Services.objects.all().order_by('-id')
    
    def _get_actions(self, obj):
        """Get action buttons w/links."""
        return f'<a href="{obj.get_update_url()}" title="Edit" class="btn btn-primary btn-xs"><i class="fa fa-edit"></i></a> <a data-title="{obj}" title="Delete" onclick="showDeletemodal({obj.id})" data-bs-toggle="modal" class="btn btn-danger btn-xs btn-delete"><i class="fa fa-trash" style="color:white";></i></a>'
    def filter_queryset(self, qs):
        """Return the list of items for this view."""
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')
        if self.search:
            return qs.filter(
                #  Q(state__icontains=self.search) |
                Q(logo__icontains=self.search) |
                Q(name__icontains=self.search) |
                Q(description__icontains=self.search) 
            )
        if start_date and end_date:
            start_date = parse_date(start_date)
            end_date = parse_date(end_date)
            qs = qs.filter(created_at__gte=start_date, created_at__lte=end_date)
            return qs
        return qs
    def prepare_results(self, qs,start_index):
        data = []
        for index,o in enumerate(qs):
            global_index = start_index + index + 1
            data.append({
                'id': global_index,
                'logo': o.logo,
                'name': o.name,
                'description': o.description,
                'actions': self._get_actions(o)
            })
        return data
    def get(self, request, *args, **kwargs):
        start = int(request.GET.get('start', 0))  
        length = int(request.GET.get('length', 10))
        queryset = self.filter_queryset(self.queryset)
        paginator = Paginator(queryset, length)
        page_number = (start // length) + 1  
        paginated_queryset = paginator.get_page(page_number)
        data = self.prepare_results(paginated_queryset,start)
        response_data = {
            'draw': int(request.GET.get('draw', 0)),  
            'recordsTotal': queryset.count(),  
            'recordsFiltered': paginator.count,
            'data': data  
        }
        return JsonResponse(response_data)
   

# --------------------------------------------------- ABOUTPARAMETER-CRUD --------------------------------------------------------

class AboutParameterCreateView(CreateView):
    model = models.AboutParameter
    form_class = forms.AboutParameterForm
    template_name = "adminapp/aboutparameter_add.html"
    success_url = reverse_lazy("adminapp:aboutparameter_list")
    
    def form_valid(self, form):
        form
        messages.success(self.request,'About Parameter Added Successfully')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        response = super().form_invalid(form)
        print(form.errors)
        messages.error(self.request,'Error, Please try again')
        return response
    
class AboutParameterListView(ListView):
    model = models.AboutParameter
    template_name = "adminapp/aboutparameter_list.html"
    context_object_name = "aboutparameter_data"
    
class AboutParameterUpdateView(UpdateView):
    model = models.AboutParameter
    form_class = forms.AboutParameterForm
    template_name = "adminapp/aboutparameter_update.html"
    success_url = reverse_lazy("adminapp:aboutparameter_list")
    
    def form_valid(self, form):
        form
        messages.success(self.request,'About Parameter Updated Successfully')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        response = super().form_invalid(form)
        print(form.errors)
        messages.error(self.request,'Error, Please try again')
        return response
    
class AboutParameterDeleteView(DeleteView):
    model = models.AboutParameter
    template_name = "adminapp/aboutparameter_list.html"
    success_url = reverse_lazy("adminapp:aboutparameter_list")
    
    def form_valid(self, form):
        form
        messages.success(self.request,'About Parameter Deleted Successfully')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        response = super().form_invalid(form)
        print(form.errors)
        messages.error(self.request,'Error, Please try again')
        return response
    
class AboutParameterDatatableView(DataTableMixin,View):
    model = models.AboutParameter
    queryset = models.AboutParameter.objects.all().order_by('-id')
    
    def _get_actions(self, obj):
        """Get action buttons w/links."""
        return f'<a href="{obj.get_update_url()}" title="Edit" class="btn btn-primary btn-xs"><i class="fa fa-edit"></i></a> <a data-title="{obj}" title="Delete" onclick="showDeletemodal({obj.id})" data-bs-toggle="modal" class="btn btn-danger btn-xs btn-delete"><i class="fa fa-trash" style="color:white";></i></a>'
    def filter_queryset(self, qs):
        """Return the list of items for this view."""
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')
        if self.search:
            return qs.filter(
                #  Q(state__icontains=self.search) |
                Q(icon__icontains=self.search) |
                Q(title__icontains=self.search) |
                Q(description__icontains=self.search) 
            )
        if start_date and end_date:
            start_date = parse_date(start_date)
            end_date = parse_date(end_date)
            qs = qs.filter(created_at__gte=start_date, created_at__lte=end_date)
            return qs
        return qs
    def prepare_results(self, qs,start_index):
        data = []
        for index,o in enumerate(qs):
            global_index = start_index + index + 1
            data.append({
                'id': global_index,
                'icon': o.icon,
                'title': o.title,
                'description': o.description,
                'actions': self._get_actions(o)
            })
        return data
    def get(self, request, *args, **kwargs):
        start = int(request.GET.get('start', 0))  
        length = int(request.GET.get('length', 10))
        queryset = self.filter_queryset(self.queryset)
        paginator = Paginator(queryset, length)
        page_number = (start // length) + 1  
        paginated_queryset = paginator.get_page(page_number)
        data = self.prepare_results(paginated_queryset,start)
        response_data = {
            'draw': int(request.GET.get('draw', 0)),  
            'recordsTotal': queryset.count(),  
            'recordsFiltered': paginator.count,
            'data': data,
        }
        return JsonResponse(response_data)
    