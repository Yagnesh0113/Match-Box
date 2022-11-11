from django.db import models
from Account.models import *
# from Account.validator import file_siz
from Account.validator import *

from datetime import date,datetime
# Create your models here.

from PIL import Image


class UserPost(models.Model):
    User_Profile=models.ForeignKey(to=UserProfile, on_delete=models.CASCADE, related_name='User_Profile')
    # Image=models.FileField(upload_to="Post", validators=[file_size], null=True,blank=True)
    Image=models.FileField(upload_to="Post", null=True,blank=True)
    Description=models.TextField(null=True, blank=True)
    Like=models.ManyToManyField(to=UserProfile, null=True, blank=True, related_name='liked')
    Post_Date=models.DateField(null=True, blank=True)
    Post_Time=models.TimeField(null=True, blank=True)
    is_active=models.BooleanField(default=True)
    Post_comment=models.IntegerField(null=True, blank=True)
    post_type1 = models.BooleanField(null=True, blank=True)
    Post_bookmark=models.BooleanField(default=False)

    def __str__(self):
        return self.Description


    def save(self, *args, **kwargs):
        super().save()  # saving image first
        try:
            img = Image.open(self.Image.path) # Open image using self

            if img.height > 600 or img.width > 700:
                new_img = (600,700)
                img.thumbnail(new_img)
                img.save(self.Image.path)  # saving image at the same path
        except:
            pass

class Post_Commment(models.Model):
    User_Post=models.ForeignKey(to=UserPost, on_delete=models.CASCADE)
    User_Profile=models.ForeignKey(to=UserProfile, on_delete=models.CASCADE)
    Comment=models.TextField(null=True, blank=True)
    Comment_Date=models.DateField(null=True, blank=True)
    Commenet_Time=models.TimeField(null=True, blank=True)
    Post_comment_reply=models.IntegerField(null=True, blank=True)
    Comment_like=models.ManyToManyField(to=UserProfile,null=True, blank=True,related_name='Comment_like')


class Comment_reply(models.Model):
    Comment=models.ForeignKey(to=Post_Commment, on_delete=models.CASCADE)
    User_Profile=models.ForeignKey(to=UserProfile, on_delete=models.CASCADE)
    Reply=models.TextField()
    Reply_Date=models.DateField(null=True, blank=True)
    Reply_Time=models.TimeField(null=True, blank=True)

class User_Question(models.Model):
    User_Profile=models.ForeignKey(to=UserProfile, on_delete=models.CASCADE)
    Question=models.TextField()
    User_id=models.TextField(null=True,blank=True)
    Date=models.DateField(null=True,blank=True)
    Time=models.TimeField(null=True,blank=True)
    answer=models.IntegerField(null=True, blank=True)
    Question_Like=models.ManyToManyField(to=UserProfile, null=True, blank=True, related_name='Question_Like' )
    Answer_later=models.BooleanField(default=False)
    Question_Edit=models.BooleanField(default=False,null=True,blank=True)
    Question_bookmark=models.BooleanField(default=False)

    def __str__(self):
        return self.Question

class User_Answer(models.Model):
    Question=models.ForeignKey(to=User_Question, on_delete=models.CASCADE)
    User_Profile=models.ForeignKey(to=UserProfile, on_delete=models.CASCADE)
    Answer=models.TextField()
    reply=models.IntegerField(null=True, blank=True)
    Date=models.DateField(null=True,blank=True)
    Time=models.TimeField(null=True,blank=True)
    Answer_Like=models.ManyToManyField(to=UserProfile, null=True, blank=True, related_name='Answer_Like' )

class Answer_Reply(models.Model):
    Answer=models.ForeignKey(to=User_Answer, on_delete=models.CASCADE)
    User_Profile=models.ForeignKey(to=UserProfile, on_delete=models.CASCADE)
    Reply=models.TextField()
    Reply_date=models.DateField(null=True, blank=True)
    Reply_Time=models.TimeField(null=True, blank=True)

class Community(models.Model):
    User_Profile=models.ForeignKey(to=UserProfile, on_delete=models.CASCADE,null=True,blank=True)
    Community_Name=models.CharField(max_length=70)
    Community_Cover_Image=models.ImageField(upload_to="Community_Cover_image",null=True,blank=True)
    Community_Profile_Image=models.ImageField(upload_to="Community_Profile_Image")
    Public=models.BooleanField(default=False)
    Private=models.BooleanField(default=False)
    Restricted=models.BooleanField(default=False)
    Adult_Content=models.BooleanField(default=False)
    Community_Type=models.BooleanField(default=True)
    community_member=models.IntegerField(blank=True,null=True,default=0)
    community_Description=models.TextField(blank=True,null=True)
    
    def __str__(self):
        return self.Community_Name

    
    def save(self, *args, **kwargs):
        super().save()  # saving image first
        try:
            img = Image.open(self.Community_Cover_Image.path) # Open image using self
            if img.height > 400 or img.width > 1519:
                new_img = (400,1519)
                img.thumbnail(new_img)
                img.save(self.Community_Cover_Image.path)  # saving image at the same path
        except:
            pass
        
        try:
            img1 = Image.open(self.Community_Profile_Image.path) # Open image using self
            if img1.height > 40 or img1.width > 40:
                new_img = (40,40)
                img1.thumbnail(new_img)
                img1.save(self.Community_Profile_Image.path)  # saving image at the same path
        except:
            pass

class Community_Post(models.Model):
    Community_obj=models.ForeignKey(to=Community, on_delete=models.CASCADE)
    Community_type=models.CharField(max_length=50, null=True, blank=True)
    user_post=models.ForeignKey(to=UserPost, on_delete=models.CASCADE)

class Community_Post_Comment(models.Model):
    Community_Post_obj=models.ForeignKey(to=Community_Post, on_delete=models.CASCADE)
    Community_Comment=models.ForeignKey(to=Post_Commment, on_delete=models.CASCADE)

class Community_Comment_reply(models.Model):
    Community_Comment=models.ForeignKey(to=Community_Post_Comment, on_delete=models.CASCADE)
    User_Profile=models.ForeignKey(to=UserProfile, on_delete=models.CASCADE)
    Reply=models.TextField()
    Reply_Date=models.DateField(null=True, blank=True)
    Reply_Time=models.TimeField(null=True, blank=True)

class Join_Community(models.Model):
    User_profile=models.ForeignKey(to=UserProfile,on_delete=models.CASCADE)
    # Commnunity_id=models.JSONField(null=True,blank=True)
    Commnunity_id=models.ForeignKey(to=Community,on_delete=models.CASCADE, null=True, blank=True)
    
class News(models.Model):
    # Image=models.FileField(upload_to='Image',null=True,blank=True,validators=[file_size])
    # Video=models.FileField(upload_to='Video',null=True,blank=True,validators=[file_size])
    Image=models.FileField(upload_to='Image',null=True,blank=True)
    Video=models.FileField(upload_to='Video',null=True,blank=True,validators=[video_file_size])
    Description=models.TextField()
    Date=models.DateField(default=date.today())
    Time=models.TimeField(default=datetime.now())
    comment=models.IntegerField(null=True, blank=True)
    News_like=models.ManyToManyField(to=UserProfile, null=True, blank=True, related_name='News_like' )
    News_bookmark=models.BooleanField(default=False)

    def __str__(self):
        return self.Description
    

    
    def save(self, *args, **kwargs):
        super().save()  # saving image first
        try:
            img = Image.open(self.Image.path) # Open image using self
            if img.height > 600 or img.width > 700:
                new_img = (600,700)
                img.thumbnail(new_img)
                img.save(self.Image.path)  # saving image at the same path
        except:
            pass
        

class News_Comment(models.Model):
    User_Profile=models.ForeignKey(to=UserProfile, on_delete=models.CASCADE)
    News_id=models.ForeignKey(to=News, on_delete=models.CASCADE)
    Comment=models.TextField()
    Date=models.DateField(null=True, blank=True)
    Time=models.TimeField(null=True, blank=True)
    reply=models.IntegerField(default=0, null=True, blank=True)
    News_comment_like=models.ManyToManyField(to=UserProfile, null=True, blank=True, related_name='News_comment_like' )

    def __str__(self):
        return self.User_Profile.usertype.user_id.first_name

class News_Comment_reply(models.Model):
    Comment=models.ForeignKey(to=News_Comment, on_delete=models.CASCADE)
    User_Profile=models.ForeignKey(to=UserProfile, on_delete=models.CASCADE,null=True,blank=True)
    Reply=models.TextField()
    Reply_Date=models.DateField(default=date.today)
    Reply_Time=models.TimeField(default=datetime.now())

    def __str__(self):
        return self.Reply

class POST_and_Question(models.Model):
    Post=models.ForeignKey(to=Community_Post, on_delete=models.CASCADE,null=True,blank=True)
    Question=models.ForeignKey(to=User_Question, on_delete=models.CASCADE,null=True,blank=True)


    def __str__(self):
        return str(self.Post)

class Answer_later(models.Model):
    Question=models.ForeignKey(to=User_Question, on_delete=models.CASCADE)
    User_Profile=models.ForeignKey(to=UserProfile, on_delete=models.CASCADE)
    Date=models.DateField(null=True, blank=True)
    Time=models.TimeField(null=True, blank=True)

class Bookmark(models.Model):
    user_profile=models.ForeignKey(to=UserProfile, on_delete=models.CASCADE)
    post=models.ForeignKey(to=Community_Post, on_delete=models.CASCADE,null=True, blank=True)
    question=models.ForeignKey(to=User_Question, on_delete=models.CASCADE, null=True, blank=True)
    news=models.ForeignKey(to=News, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return str(self.user_profile)

class distance_calculation(models.Model):
    user_profile = models.OneToOneField(UserProfile,on_delete=models.CASCADE)
    distance=models.JSONField()

class Report(models.Model):
    user_profile=models.ForeignKey(to=UserProfile, on_delete=models.CASCADE)
    post=models.ForeignKey(to=UserPost, on_delete=models.CASCADE, null=True, blank=True)
    question=models.ForeignKey(to=User_Question, on_delete=models.CASCADE, null=True, blank=True)
    community_id=models.ForeignKey(to=Community, on_delete=models.CASCADE, null=True, blank=True)
    news_id=models.ForeignKey(to=News, on_delete=models.CASCADE, null=True, blank=True)
    user_id=models.IntegerField(null=True, blank=True)
    report_date=models.DateField(null=True, blank=True)
    report_time=models.TimeField(null=True, blank=True)
    adult_content=models.BooleanField(default=False)
    abusing_content=models.BooleanField(default=False)
    report_description=models.TextField()