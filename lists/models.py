from django.db import models
from django.urls import reverse

class List(models.Model):
    def get_absolute_url(self):
        return reverse('view_list', args=[self.id])
    

class Item(models.Model):
    list = models.ForeignKey(List, related_name='items', on_delete=models.CASCADE)
    text = models.CharField(max_length=250)

    class Meta:
        unique_together = ('list', 'text')

    def __str__(self):
        return self.text