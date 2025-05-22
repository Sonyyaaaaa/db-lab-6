from django.db import models

class Task(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    deadline = models.DateTimeField()
    Client_id = models.IntegerField()

    class Meta:
        db_table = 'task'
        managed = False