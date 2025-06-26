from django.db import models
from app_modules.base.models import BaseModel
from app_modules.adminapp.models import User
from simple_history.models import HistoricalRecords
# Create your models here.


class Feedback(BaseModel):
    from_user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='from_feedback')
    to_user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='to_feedback')
    description = models.TextField()
    rate = models.PositiveIntegerField()
    document = models.FileField(upload_to='feedback_document',null=True,blank=True)
    is_active = models.BooleanField(default=True)
    history = HistoricalRecords()
    
class FeedbackResponse(BaseModel):
    feedback = models.ForeignKey(Feedback,on_delete=models.CASCADE,related_name='feedback_responses')
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='response_user')
    description = models.TextField()
    document = models.FileField(upload_to='feedback_response_document',null=True,blank=True)
    is_active = models.BooleanField(default=True)
    history = HistoricalRecords()
    
    
class ReportFeedback(BaseModel):
    feedback = models.ForeignKey(Feedback,on_delete=models.CASCADE,related_name='report_feedbacks')
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='reported_user')
    is_active = models.BooleanField(default=True)
    