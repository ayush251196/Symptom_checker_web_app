from django.contrib import admin
from symptom_checker.models import Symptoms,Issues,Specialization,Details
# Register your models here.

admin.site.register(Symptoms)
admin.site.register(Issues)
admin.site.register(Specialization)
admin.site.register(Details)
