from django.db import models
from django.contrib.auth import get_user_model
import uuid


class Category(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField()

    def __str__(self):
        return self.title


class Note(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    context = models.TextField()    
    category = models.ForeignKey(Category, on_delete=models.PROTECT, null=True, blank=True)
    creator = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True)
    bookmark = models.BooleanField(default=False)
    published = models.BooleanField(default=False)
    dtcreate = models.DateTimeField(auto_now_add=True)
    dtupdate = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['dtcreate']