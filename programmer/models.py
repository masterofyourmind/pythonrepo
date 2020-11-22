from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.utils.timezone import now


# Create your models here.
class Post(models.Model):
    sno = models.AutoField(primary_key=True)
    blogtitle = models.CharField(max_length=255)
    image = models.ImageField(_('image'), blank=True, null=True, upload_to='programmer/media/images')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    descri = models.CharField(max_length=300)
    slug = models.CharField(max_length=130)
    body = models.TextField()
    timestamp = models.DateTimeField(blank=False)

    def __str__(self):
        return self.blogtitle


class Contact(models.Model):
    name= models.CharField(max_length=122)
    email= models.CharField(max_length=122)
    phone= models.CharField(max_length=16)
    desc=models.TextField()
    date = models.DateField()

    def __str__(self):
        return self.name


class BlogComment(models.Model):
    sno = models.AutoField(primary_key=True)
    comment = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
    timestamp = models.DateTimeField(default=now)

    def __str__(self):
        return self.comment[0:13] + "..." + "by" + self.user.username
