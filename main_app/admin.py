from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *
# Register your models here.


class UserModel(UserAdmin):
    ordering = ('email',)


admin.site.register(CustomUser, UserModel)
admin.site.register(Manager)    # Staff 
admin.site.register(ProjectEngineer)    # Student  
admin.site.register(Track)  # Course
admin.site.register(Task)   # Subject
