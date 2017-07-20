# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import bcrypt, re

# Create your models here.
class UserManager(models.Manager):
	def register(self, postData):
		errors = []

		if len(postData['first_name']) < 1 or len(postData['last_name']) < 1 or len(postData['email']) < 1 or len(postData['first_name']) < 1:
			errors.append('Missing field.')

		if len(postData['first_name']) < 2 or len(postData['last_name']) < 2:
			errors.append('First name and/or last name cannot be fewer than 2 characters.')

		# if not NAME_REGEX.match(postData['first_name']) or not NAME_REGEX.match(postData['last_name']):
		# 	errors.append('First name and/or last name can only contain letters.')

		# if not EMAIL_REGEX.match(postData['email']):
		# 	errors.append('Email is invalid.')

		# if not PW_REGEX.match(postData['password']):
		# 	errors.append('Password is invalid. Cannot be fewer than 8 characters.')

		if postData['password'] != postData['confirm_pw']:
			errors.append('Passwords do not match.')

		# search for email in database
		if User.objects.filter(email=postData['email']):
			errors.append('Email already exists.')

		return errors

	def login(self, postData):
		errors = []

		if not User.objects.filter(email=postData['email']):
			errors.append('Username and/or password are invalid.')
		else:
			if bcrypt.hashpw(postData['password'].encode('utf-8'), User.objects.get(email=postData['email']).hashed_pw.encode('utf-8')) != User.objects.get(email=postData['email']).hashed_pw:
				errors.append('Username and/or password are invalid.')

		return errors

class User(models.Model):
	username = models.CharField(max_length=255)
	first_name = models.CharField(max_length=255)
	last_name = models.CharField(max_length=255)
	email = models.CharField(max_length=255)
	hashed_pw = models.CharField(max_length=255)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	objects = UserManager()

class Post(models.Model):
	content = models.URLField(max_length=255)
	posted_by = models.ForeignKey(User)
	feeds = models.ManyToManyField(User, related_name="feed")
	likes = models.ManyToManyField(User, related_name="likes")
	views = models.ManyToManyField(User, related_name="views")
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
