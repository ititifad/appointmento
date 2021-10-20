from django.db import models
from django.db.models.enums import Choices
from django.contrib.auth.models import User

class Hospital(models.Model):
    name = models.CharField(max_length=200)
    user = models.OneToOneField(User,null=True, blank=True, on_delete=models.CASCADE)
    phone = models.CharField(max_length=200, null=True)
    email = models.EmailField(null=True)
    location    = models.CharField(max_length=40,null=True, blank=True)
    profile_pic = models.ImageField(default='default.png',upload_to='profile_pics')
    is_verified = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    
    def __str__(self):
        return self.name
    
class Specialist(models.Model):
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    specialist = models.CharField(max_length=200, null=True, blank=True)
    phone = models.CharField(max_length=200, null=True)
    
    def __str__(self):
        return self.name

class Appointment(models.Model):
    GENDER = (
        ('Male','male'),
        ('Female','female')
    )
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    gender = models.CharField(max_length=200, choices=GENDER)
    hospital = models.ForeignKey(Hospital, on_delete=models.SET_NULL, null=True)
    specialist = models.ForeignKey(Specialist, on_delete=models.SET_NULL, null=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    message = models.TextField()
    app_date = models.DateField()
        
    def __str__(self):
        return self.first_name
