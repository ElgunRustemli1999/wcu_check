from django.db import models


class Department(models.Model):
    department_name = models.CharField(max_length=1000)

    def __str__(self):
        return self.department_name
    
class Position(models.Model):
    position_name = models.CharField(max_length=1000)

    def __str__(self):
        return self.position_name

class Holiday(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateField(unique=True)

    def __str__(self):
        return f"{self.name} - {self.date}"

















"""
# Create your models here.
class Building(models.Model):
    name = models.CharField(max_length=255)
    active = models.BooleanField(default=True)

class Department(models.Model):
    position_name = models.CharField(max_length=255)
    position_where = models.CharField(max_length=255)
    active = models.BooleanField()
   """ 