from django import forms 
from app_modules.adminapp import models

class UserForm(forms.ModelForm):
    class Meta:
        model = models.User
        fields = ['first_name','last_name','email','phone','address','role','position','gst_number',]

class BasicDetailsForm(forms.ModelForm):
    class Meta:
        model = models.BasicDetails
        fields = "__all__"
        

class FAQForm(forms.ModelForm):
    class Meta:
        model = models.FAQ
        fields = "__all__"
        
class CategoryForm(forms.ModelForm):
    class Meta:
        model = models.Category
        fields = "__all__"

class BlogForm(forms.ModelForm):
    class Meta:
        model = models.Blog
        fields = "__all__"
        exclude = ['user']

class TestimonialForm(forms.ModelForm):
    class Meta:
        model = models.Testimonial
        fields = "__all__"
        exclude = ['user']
        
class ServicesForm(forms.ModelForm):
    class Meta:
        model = models.Services
        fields = "__all__"
        
class AboutParameterForm(forms.ModelForm):
    class Meta:
        model = models.AboutParameter
        fields = "__all__"
        