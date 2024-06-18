__version__ = '0.9.53'
__author__ = 'Matt Andrzejczuk'
import random
from django.db import models
from krogoth_gantry.models.models_chat import JawnUser
from polymorphic.models import PolymorphicModel


# Create your models here.
class AKThreadCategory(models.Model):
    uid = models.CharField(max_length=249, primary_key=True)
    title = models.CharField(max_length=248, default='new category')
    description = models.CharField(max_length=248, default='No description.')
    is_deleted = models.BooleanField(default=False)


    @classmethod
    def make_thread_category(cls, named: str):
        make_sample = cls(title="Sample Threads")
        make_sample.save()
        return make_sample

    def save(self, *args, **kwargs):
        count = len(AKThread.objects.all())
        p1 = self.title.replace(" ", "_").replace("?", "").replace("$", "").replace("!", "").replace("$", "")
        self.uid = p1.replace("%", "_").replace("&", "").replace("@", "").replace("^", "").replace("/", "") + str(count)
        super(AKThreadCategory, self).save(*args, **kwargs)

    def __str__(self):
        return self.uid

class AKThread(PolymorphicModel):
    uid = models.CharField(max_length=249, primary_key=True)
    title = models.CharField(max_length=257, default='new post')
    author = models.ForeignKey(JawnUser, on_delete=models.CASCADE, null=True, blank=True)
    pub_date = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(null=True, blank=True)
    is_deleted = models.BooleanField(default=False)
    category = models.ForeignKey(AKThreadCategory, on_delete=models.CASCADE, related_name="ak_threads", null=True, blank=True)
    parent = models.ForeignKey('AKThread', on_delete=models.CASCADE, null=True, blank=True, related_name="broodling")
    content = models.TextField(default="")

    @property
    def is_reply(self):
	    return self.parent is not None
	    
    @property
    def author_name(self):
        return self.author.base_user.username
	    	 
    @property
    def totalThreads(self):
        return len(AKThread.objects.all())
    

    def __str__(self):
        return self.uid


SOCIAL_MEDIA_THREAD_KINDS = (
    ('text', 'text'),
    ('article', 'article'),
    ('video', 'video'),
    ('image', 'image'),
)
class AKThreadSocialMedia(AKThread):
    type = models.CharField(max_length=40, default="text", choices=SOCIAL_MEDIA_THREAD_KINDS)
    text_body = models.TextField()
    likes = models.IntegerField(default=0)

class ForumThreadCategory(models.Model):
    uid = models.CharField(max_length=249, primary_key=True, default='NO_UID_GIVEN')
    title = models.CharField(max_length=248, default='new category')
    description = models.CharField(max_length=248, default='No description.')
    total_threads = models.IntegerField(default=0)
    weight = models.IntegerField(default=0)
    img_url = models.CharField(max_length=249, null=True, blank=True)


class ForumThreadOP(models.Model):
    uid = models.CharField(max_length=249, primary_key=True, default="" + str(random.randint(1, 9000000000000)))
    title = models.CharField(max_length=257, default='new post')
    author = models.ForeignKey(JawnUser, on_delete=models.CASCADE, null=True, blank=True)
    pub_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    date_modified = models.DateTimeField(null=True, blank=True)
    not_deleted = models.BooleanField(default=True)
    category = models.ForeignKey(ForumThreadCategory, on_delete=models.CASCADE, null=True, blank=True)
    content = models.TextField(default="")
    total_likes = models.IntegerField(default=0)
    total_replies = models.IntegerField(default=0)
    total_views = models.IntegerField(default=0)

    @property
    def header(self):
        self.total_views += 1
        return "Views " + str(total_views)

    @property
    def author_name(self):
        return self.author.base_user.username

class ForumThreadReply(models.Model):
    uid = models.CharField(max_length=249, primary_key=True)
    author = models.ForeignKey(JawnUser, on_delete=models.CASCADE, null=True, blank=True)
    pub_date = models.DateTimeField(null=True, blank=True)
    date_modified = models.DateTimeField(null=True, blank=True)
    not_deleted = models.BooleanField(default=True)
    content = models.TextField(default="")
    total_likes = models.IntegerField(default=0)
    parent = models.ForeignKey(ForumThreadOP, on_delete=models.CASCADE, null=True, blank=True)

    @property
    def author_name(self):
        return self.author.base_user.username


# DEFAULTS:
try:
    sampleCat = AKThreadCategory.objects.filter(title="Sample Threads")
    if len(sampleCat) < 1:
        make_sample = AKThreadCategory.make_thread_category(named="Sample Threads")
        t1 = AKThread(title="First One", author=JawnUser.objects.all().first(), category=make_sample).save()
        t2 = AKThread(title="Second One", author=JawnUser.objects.all().first(), category=make_sample).save()
        t3 = AKThread(title="Reply to First One", author=JawnUser.objects.all().first(), category=make_sample,
                      parent=t1).save()
        t4 = AKThread(title="Third One", author=JawnUser.objects.all().first(), category=make_sample).save()
except:
    pass