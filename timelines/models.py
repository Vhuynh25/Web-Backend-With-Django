from django.db import models

# Create your models here.


class Post(models.Model):
	text = models.CharField(max_length=500)
	url = models.CharField(max_length=100)
	user_id = models.IntegerField()
	username = models.CharField(max_length=50)
	timestamp = models.CharField(max_length=100)
