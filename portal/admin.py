from django.contrib import admin
from .models import Student, Company, Job, Application

# Register your models here.

admin.site.register(Student)
admin.site.register(Company)
admin.site.register(Job)
admin.site.register(Application)