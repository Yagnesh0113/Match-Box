from django.contrib import admin
from .models import *

admin.site.register(State)
admin.site.register(City)
admin.site.register(Admin_Profession)
admin.site.register(ProfessionReview)
admin.site.register(ProfessionReview_Reply)

# Register your models here.
