from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Community)
admin.site.register(Join_Community)
admin.site.register(News)
admin.site.register(News_Comment)
admin.site.register(News_Comment_reply)
admin.site.register(User_Question)
admin.site.register(UserPost)
admin.site.register(Post_Commment)


