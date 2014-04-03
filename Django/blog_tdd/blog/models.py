from django.core.urlresolvers import reverse
from django.db import models
from django.contrib.auth.models import UserManager

class Entry(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey('auth.user')
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    modified_at = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta:
        verbose_name_plural = "entries"

    def __unicode__(self):
        return self.title
    
    def get_absolute_url(self):
        abs_url = reverse('blog.views.entry_detail', kwargs={'pk': self.pk})
        return abs_url

class Comment(models.Model):
    entry = models.ForeignKey(Entry)
    name = models.CharField(max_length=20)
    email = models.EmailField()
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    modified_at = models.DateTimeField(auto_now_add=True, editable=False)

    def __unicode__(self):
        return self.name

