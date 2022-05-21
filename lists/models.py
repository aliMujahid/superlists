from django.db import models

class List(models.Model):
    pass

class Item(models.Model):
    list = models.ForeignKey(List, related_name='items', on_delete=models.CASCADE)
    text = models.CharField(max_length=250)