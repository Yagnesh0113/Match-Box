from datetime import date, datetime
from django.db import models
from django.contrib.auth.models import User
from .validator import *
from django.core.validators import MaxLengthValidator, MinLengthValidator

class State(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name

class City(models.Model):
    state = models.ForeignKey(State,on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name

class Admin_Profession(models.Model):
    Profession_Name=models.CharField(max_length=100)
    Profession_Outside_Image=models.FileField(upload_to="Profession_Outside_Image",validators=[Image_file_size])  #imagefield to transfer in filefiled
    Profession_Inside_Image=models.FileField(upload_to="Profession_Inside_Image",validators=[Image_file_size])  #imagefield to transfer in filefiled


    def __str__(self):
        return self.Profession_Name

# Create your models here.
class UserType(models.Model):
    user_id=models.OneToOneField(to=User,on_delete=models.CASCADE)
    user_type=models.CharField(max_length=50,null=True,blank=True)

class UserProfile(models.Model):
    usertype=models.OneToOneField(to=UserType,on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=10,null=True, blank=True)
    profile_image=models.FileField(upload_to='Profile_Pic',null=True, blank=True,validators=[Image_file_size],default='default.webp')  #imagefield to transfer in filefiled
    # profile_image=models.ImageField(upload_to='Profile_Pic',null=True, blank=True)
    terms_conditions=models.BooleanField(null=True, blank=True)
    state=models.CharField(max_length=50,null=True, blank=True)
    city=models.CharField(max_length=50,null=True, blank=True)
    country_code = models.CharField(max_length=2, null=True, blank=True,)
    whatsapp_number = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
      return self.usertype.user_id.username

class Profession(models.Model):
    UserProfile=models.ForeignKey(to=UserProfile,on_delete=models.CASCADE)
    profession = models.ForeignKey(to=Admin_Profession, on_delete=models.CASCADE)
    profession_image=models.FileField(upload_to='Profession',validators=[Image_file_size] )  #imagefield to transfer in filefiled
    # profession_image=models.ImageField(upload_to='Profession')
    year_of_experience = models.IntegerField(null=True, blank=True)
    shop_name = models.CharField(max_length=50,null=True, blank=True)
    shop_start_time= models.TimeField(null=True, blank=True)
    shop_close_time= models.TimeField(null=True, blank=True)
    shop_address= models.TextField(null=True, blank=True)
    shop_city= models.CharField(max_length=50)
    shop_state= models.CharField(max_length=50)
    shop_status_sunday=models.BooleanField(null=True, blank=True)
    shop_status_monday=models.BooleanField(null=True, blank=True)
    shop_status_Tuesday=models.BooleanField(null=True, blank=True)
    shop_status_Wednesday=models.BooleanField(null=True, blank=True)
    shop_status_Thrusday=models.BooleanField(null=True, blank=True)
    shop_status_Friday=models.BooleanField(null=True, blank=True)
    shop_status_saturday=models.BooleanField(null=True, blank=True)
    shop_description= models.TextField(null=True, blank=True)
    shop_Longititude= models.TextField(null=True, blank=True)
    shop_Latitude= models.TextField(null=True, blank=True)
    Profession_Rating = models.FloatField(default=0)
    profession_longitude=models.FloatField(null=True, blank=True)
    profession_latitude=models.FloatField(null=True, blank=True)


    def __str__(self):
        return self.UserProfile.usertype.user_id.first_name

class ProfessionServices(models.Model):
    Profession= models.ForeignKey(to=Profession,on_delete=models.CASCADE)
    service_name=models.CharField(max_length=50)
    service_price= models.CharField(max_length=10)

class Professionimage(models.Model):
    profession= models.ForeignKey(to=Profession,on_delete=models.CASCADE)
    # image=models.ImageField(upload_to='Profession')
    image=models.FileField(upload_to='Profession',validators=[Image_file_size]) #imagefield to transfer in filefiled


class Professionvideo(models.Model):
    profession= models.ForeignKey(to=Profession,on_delete=models.CASCADE)
    # video=models.FileField(upload_to='Video/%y',validators=[file_size])
    video=models.FileField(upload_to='Video/%y',validators=[video_file_size])



class Recent_serach(models.Model):
    Profession_obj=models.ForeignKey(to=Profession, on_delete=models.CASCADE)
    User_obj=models.ForeignKey(to=UserProfile, on_delete=models.CASCADE)


class nearest_profession(models.Model):
    user=models.OneToOneField(to=User, on_delete=models.CASCADE)
    near=models.JSONField()