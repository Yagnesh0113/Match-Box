from django.db import models
from Account.models import *
from Account.validator import file_size
from datetime import date,datetime
# Create your models here.

class UserPost(models.Model):
    User_Profile=models.ForeignKey(to=UserProfile, on_delete=models.CASCADE, related_name='User_Profile')
    Image=models.FileField(upload_to="Post", validators=[file_size], null=True,blank=True)
    Description=models.TextField(null=True, blank=True)
    Like=models.ManyToManyField(to=UserProfile,null=True, blank=True, related_name='liked')
    Post_Date=models.DateField(null=True, blank=True)
    Post_Time=models.TimeField(null=True, blank=True)
    is_active=models.BooleanField(default=True)
    Post_comment=models.IntegerField(null=True, blank=True)
    post_type1 = models.BooleanField(null=True, blank=True)

    def __str__(self):
        return self.Description

    @property
    def num_likes(self):
        return self.Like.all().count()


LIKE_CHOISE = (
    ('Like', 'Like'),
    ('Unlike', 'Unlike'),
)


class Like(models.Model):
    user_profile = models.ForeignKey(to=UserProfile, on_delete=models.CASCADE)
    Post = models.ForeignKey(to=UserPost, on_delete=models.CASCADE)
    value = models.CharField(choices=LIKE_CHOISE, default='Like', max_length=10)

    def __str__(self):
        return str(self.Post)


class Post_Commment(models.Model):
    User_Post=models.ForeignKey(to=UserPost, on_delete=models.CASCADE)
    User_Profile=models.ForeignKey(to=UserProfile, on_delete=models.CASCADE)
    Comment=models.TextField(null=True, blank=True)
    Comment_Date=models.DateField(null=True, blank=True)
    Commenet_Time=models.TimeField(null=True, blank=True)
    Comment_like=models.ImageField(null=True, blank=True)

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
    Date=models.DateField(default=date.today())
    Time=models.TimeField(default=datetime.now())
    answer=models.IntegerField(null=True, blank=True)
    def __str__(self):
        return self.Question

class User_Answer(models.Model):
    Question=models.ForeignKey(to=User_Question, on_delete=models.CASCADE)
    User_Profile=models.ForeignKey(to=UserProfile, on_delete=models.CASCADE)
    Answer=models.TextField()

class Answer_Reply(models.Model):
    Answer=models.ForeignKey(to=User_Answer, on_delete=models.CASCADE)
    User_Profile=models.ForeignKey(to=UserProfile, on_delete=models.CASCADE)
    Reply=models.TextField()

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
    def __str__(self):
        return self.Community_Name

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
    Image=models.FileField(upload_to='Image',null=True,blank=True,validators=[file_size])
    Video=models.FileField(upload_to='Video',null=True,blank=True,validators=[file_size])
    Description=models.TextField()
    Date=models.DateField(default=date.today())
    Time=models.TimeField(default=datetime.now())

    def __str__(self):
        return self.Description

class News_Comment(models.Model):
    User_Profile=models.ForeignKey(to=UserProfile, on_delete=models.CASCADE)
    News_id=models.ForeignKey(to=News, on_delete=models.CASCADE)
    Comment=models.TextField()
    Date=models.DateField(default=date.today())
    Time=models.TimeField(default=datetime.now())

    def __str__(self):
        return self.User_Profile.usertype.user_id.first_name

class News_Comment_reply(models.Model):
    Comment=models.ForeignKey(to=News_Comment, on_delete=models.CASCADE)
    User_Profile=models.ForeignKey(to=UserProfile, on_delete=models.CASCADE,null=True,blank=True)
    Reply=models.TextField()
    Reply_Date=models.DateField(default=date.today)
    Reply_Time=models.TimeField(default=datetime.now())

    def __str__(self):
        return self.Comment.Comment

class POST_and_Question(models.Model):
    Post=models.ForeignKey(to=UserPost, on_delete=models.CASCADE,null=True,blank=True)
    Question=models.ForeignKey(to=User_Question, on_delete=models.CASCADE,null=True,blank=True)

class Answer_later(models.Model):
    Question=models.ForeignKey(to=User_Question, on_delete=models.CASCADE)
    User_Profile=models.ForeignKey(to=UserProfile, on_delete=models.CASCADE)
    Date=models.DateField(default=date.today())
    Time=models.TimeField(default=datetime.now())
