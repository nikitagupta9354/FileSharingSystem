from django.db import models
from accounts.models import User

# Create your models here.
class File(models.Model):
    user= models.ForeignKey(User, on_delete=models.CASCADE)
    doc= models.FileField(upload_to='')
    uploaded_at= models.DateTimeField(auto_now_add=True)
