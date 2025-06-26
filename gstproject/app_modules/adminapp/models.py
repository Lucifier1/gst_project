from django.db import models
from app_modules.base.models import BaseModel
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.db.models import Avg
from simple_history.models import HistoricalRecords
# Create your models here.


class User(AbstractUser):
    role = models.CharField(max_length=255,null=True,blank=True,default="Customer")
    phone = models.IntegerField(null=True,blank=True,
                                validators=[RegexValidator(r'^\+?1?\d{9,15}$', 'Enter a valid phone number.')])
    address = models.TextField(null=True,blank=True)
    position = models.CharField(max_length=255,null=True,blank=True)
    gender = models.CharField(max_length=255,null=True,blank=True)
    gst_number = models.CharField(max_length=255,null=True,blank=True,
                                  validators=[RegexValidator(r'^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[1-9A-Z]{1}[A-Z]{1}[0-9A-Z]{1}$', 'Enter a valid GST number.')])
    profile = models.ImageField(upload_to='user_profile',null=True,blank=True)
    is_forgotpassword = models.BooleanField(default=False)
    
class UserVisit(BaseModel):
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField()
    referrer = models.TextField()
    visit_count = models.PositiveIntegerField(default=1)  
    timestamp = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('ip_address', 'user_agent') 
        
    def __str__(self):
        return f'{self.ip_address} - {self.user_agent} (Visits: {self.visit_count})'


class BasicDetails(BaseModel):
    name = models.CharField(max_length=255)
    about = models.TextField()
    address = models.TextField()
    phone = models.PositiveIntegerField()
    email = models.EmailField()
    twitter_link = models.CharField(max_length=255)
    facebook_link = models.CharField(max_length=255)
    instagram_link = models.CharField(max_length=255)
    linkedin_link = models.CharField(max_length=255)
    
    
class FAQ(BaseModel):
    question = models.TextField()
    answer = models.TextField()
    history = HistoricalRecords()
    
    def get_update_url(self):
        return reverse('adminapp:faq_update', kwargs={'pk': self.pk})
    
    def get_delete_url(self):
        return reverse('adminapp:faq_delete', kwargs={'pk': self.pk})
    
class Category(BaseModel):
    name = models.CharField(max_length=255)
    
    def get_update_url(self):
        return reverse('adminapp:category_update', kwargs={'pk': self.pk})
    
    def get_delete_url(self):
        return reverse('adminapp:category_delete', kwargs={'pk': self.pk})
    
class Blog(BaseModel):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='user_blog')
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.ForeignKey(Category,on_delete=models.CASCADE,related_name='blog_category')
    image = models.ImageField(upload_to='blog_image')
    
    def get_update_url(self):
        return reverse('adminapp:blog_update', kwargs={'pk': self.pk})
    
    def get_delete_url(self):
        return reverse('adminapp:blog_delete', kwargs={'pk': self.pk})
    
class Testimonial(BaseModel):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='user_testimonial')
    title = models.CharField(max_length=255)
    description = models.TextField()
    rate = models.PositiveIntegerField(null=True,blank=True)
    
    @classmethod
    def average_rating(cls):
        return cls.objects.aggregate(Avg('rate'))['rate__avg']
    
    def get_update_url(self):
        return reverse('adminapp:testimonial_update', kwargs={'pk': self.pk})
    
    def get_delete_url(self):
        return reverse('adminapp:testimonial_delete', kwargs={'pk': self.pk})
    
class Services(BaseModel):
    logo = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    description = models.TextField()
    
    def get_update_url(self):
        return reverse('adminapp:services_update', kwargs={'pk': self.pk})
    
    def get_delete_url(self):
        return reverse('adminapp:services_delete', kwargs={'pk': self.pk})
    
class AboutParameter(BaseModel):
    icon = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    description = models.TextField()
    
    def get_update_url(self):
        return reverse('adminapp:aboutparameter_update', kwargs={'pk': self.pk})
    
    def get_delete_url(self):
        return reverse('adminapp:aboutparameter_delete', kwargs={'pk': self.pk})
    
     