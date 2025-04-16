from django.db import models
from users.models import Worker
from core.models import Department,Position
# Create your models here.
class HRReport (models.Model):
    worker  = models.ForeignKey(Worker, on_delete=models.CASCADE)
    date  = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=100, choices=[('icazəli', 'İcazəli'), ('icazəsiz', 'İcazəsiz')])
    comment = models.TextField(blank=True, null=True)


    def __str__(self):
        return f"{self.worker.worker_name} {self.worker.worker_surname} - {self.status} - {self.date}"
