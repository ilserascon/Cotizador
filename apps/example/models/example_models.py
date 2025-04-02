from django.db import models
from utils.soft_delete import SoftDeleteModel


class Person(SoftDeleteModel):
  public_atts = ['first_name', 'last_name', 'age']

  first_name = models.CharField(max_length=50)
  last_name = models.CharField(max_length=60)
  age = models.IntegerField()
  created_at = models.DateTimeField(auto_now_add=True)



class Note(SoftDeleteModel):
  title = models.CharField(max_length=64)
  content = models.CharField(max_length=256, null=True)
  person = models.ForeignKey(to=Person, on_delete=models.CASCADE, related_name="notes")
