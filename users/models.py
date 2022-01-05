from django.db import models

# Create your models here.

class User(models.Model):
	bio = models.CharField(max_length=1000)
	email = models.CharField(max_length=100, unique=True)
	username = models.CharField(max_length=50)
	password = models.CharField(max_length=100)

class Follow(models.Model):
	class Meta:
		unique_together = (('followed_name','follower_id'),)

	followed_name = models.CharField(max_length=50)
	follower_id = models.IntegerField()