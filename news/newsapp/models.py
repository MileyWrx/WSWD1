from django.db import models

class Authors(models.Model):
    username = models.CharField(max_length=16,primary_key=True)
    name = models.CharField(max_length=16)
    password = models.CharField(max_length=32)
    def __str__(self):
        return self.username


class NewsStories(models.Model):
    key = models.AutoField(primary_key=True)
    headline = models.CharField(max_length=64)
    CATEGORIES = (
        ('pol', 'politics'),
        ('art', 'art news'),
        ('tech', 'technology news'),
        ('trivia', 'trivial news'),
    )
    category = models.CharField(max_length=16, choices=CATEGORIES)
    REGIONS = (
        ('uk','uk news'),
        ('eu','european news'),
        ('w','word news'),
    )
    region = models.CharField(max_length=16, choices=REGIONS)
    author = models.ForeignKey (Authors,on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    details = models.CharField(max_length=512)
    def __str__(self):
        return self.headline
# Create your models here.
