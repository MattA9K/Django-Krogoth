from django.db import models

from django.contrib.auth.models import User



class AKNote(models.Model):
    author = models.OneToOneField(User, related_name='published_by', on_delete=models.CASCADE)
    title = models.CharField(max_length=150, blank=False, null=False)
    body = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(blank=True, null=True)


