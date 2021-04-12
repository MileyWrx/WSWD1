from django.contrib import admin

# Register your models here.
from newsapp.models import NewsStories
from newsapp.models import Authors
admin.site.register(NewsStories)
admin.site.register(Authors)