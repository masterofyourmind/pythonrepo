from django.contrib import admin
from programmer.models import Contact
from programmer.models import Post, BlogComment
# Register your models here.

admin.site.register(Contact)
admin.site.register((Post, BlogComment))