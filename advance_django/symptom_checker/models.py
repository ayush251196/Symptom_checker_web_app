from django.db import models
# Create your models here.

class Symptoms(models.Model):
    name_id=models.PositiveIntegerField()
    name=models.CharField(max_length=256)
    issues_id=models.CharField(max_length=256)

    def __str__(self):
        return self.name
#--------------------------------------------------------------------------------------------------------------------------------------------
class Issues(models.Model):
    issue_id=models.PositiveIntegerField()
    name=models.CharField(max_length=256)
    specializations=models.CharField(max_length=256)
    short_description=models.TextField()
    medical_condition=models.TextField()
    treatement_description=models.TextField()
    related_symptoms=models.TextField()
    def __str__(self):
        return str(self.issue_id)
#---------------------------------------------------------------------------------------------------------------------------------------------------
class Specialization(models.Model):
    s_id=models.PositiveIntegerField()
    name=models.TextField()

    def __str__(self):
        return str(self.s_id)
#--------------------------------------------------------------------------------------------------------------------------------------------------------
class Details(models.Model):
    name=models.TextField()
    yearofbirth=models.PositiveIntegerField()
    gender=models.TextField()

    def __str__(self):
        return str(self.yearofbirth)
