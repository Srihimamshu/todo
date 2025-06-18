from django.db import models
from django.contrib.auth.models import User

class Todo(models.Model):
    category_choices=[
        ('personal','Personal'),
        ('work','Work'),
        ('health','Health'),
        ('social','Social'),
        ('academic','Academic'),
        ('errands','Errands'),
        ('misc','Miscelleneous'),       
        ]
    sno=models.AutoField(primary_key=True,auto_created=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task_name=models.CharField(max_length=100)
    description=models.TextField(blank=True)
    category=models.CharField(max_length=25,choices=category_choices,default='personal')
    created_at=models.DateTimeField(auto_now_add=True)
    due_date=models.DateField(null=True,blank=True)
    completed=models.BooleanField(default=False)
