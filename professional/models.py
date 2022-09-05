from django.db import models
from Account.models import *

class ProfessionReview(models.Model):
    Profession= models.ForeignKey(to=Profession,on_delete=models.CASCADE)
    user_profile=models.ForeignKey(to=UserProfile,on_delete=models.CASCADE, related_name="user_profile")
    Review=models.TextField()
    Rate=models.IntegerField(default=0,
        validators=[MaxLengthValidator(5),MinLengthValidator(0)]
    )
    Review_Date=models.DateField(default=date.today())
    Review_Time=models.TimeField(default=datetime.now())
    like=models.ManyToManyField(to=UserProfile, null=True, blank=True)
    Reply=models.IntegerField(null=True, blank=True)

    def __str__(self):
      return self.Review

    @property
    def num_likes(self):
        return self.like.all().count()

LIKE_CHOISE = (
    ('Like', 'Like'),
    ('Unlike', 'Unlike'),
)

class Review_Like(models.Model):
    user_profile = models.ForeignKey(to=UserProfile, on_delete=models.CASCADE)
    Profession_Review = models.ForeignKey(to=ProfessionReview, on_delete=models.CASCADE)
    value = models.CharField(choices=LIKE_CHOISE, default='Like', max_length=10)

    def __str__(self):
        return str(self.profession)

class ProfessionReview_Reply(models.Model):
    Review= models.ForeignKey(to=ProfessionReview,on_delete=models.CASCADE)
    User_Profile=models.ForeignKey(to=UserProfile,on_delete=models.CASCADE)
    Review_Reply=models.TextField()
    Review_Reply_Date=models.DateField(default=date.today())
    Review_Reply_Time=models.TimeField(default=datetime.now())

    def __str__(self):
      return self.Review_Reply