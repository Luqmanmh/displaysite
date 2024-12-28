from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

class Patient(models.Model):
    full_name = models.CharField(max_length=255)
    personal_doc = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    phone_num = models.CharField(max_length=14, default=0)
    critical_con = models.BooleanField(default=False)
    newest_update = models.DateTimeField(null=True, blank=True)
    
class patientdata(models.Model):
    jsondata = models.FileField()
    pat_owner = models.ForeignKey(Patient, on_delete=models.CASCADE, null=False)
    up_date = models.DateTimeField(default=datetime.now, blank=True)
    
class Alert(models.Model):
    content = models.TextField()
    time = models.TimeField()
    is_read = models.BooleanField(default=False)
    doctor = models.ForeignKey(User, on_delete=models.CASCADE)