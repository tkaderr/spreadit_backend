# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from .models import User, Post
from django.http import HttpResponse
import bcrypt, urllib2

# Create your views here.
def index(request):
	request.session['user_id']=1
	return render(request, 'rest_api/index.html')

def login(request):
	postData = {
		'email': request.POST['email'],
		'password': request.POST['password'],
	}

	if not User.objects.login(postData):
		user_id = User.objects.get(email=postData['email']).id
		return HttpResponse(urllib2.urlopen("http://localhost:8000/rest-api/users/"+str(user_id)).read())

	return HttpResponse(status=400)

def swipePost(request):
	postData = {
		'user_id': request.POST['user_id'],
		'post_id': request.POST['post_id'],
		'like': request.POST['like'], # This should be a boolean value sent with http resquest
	}

	print(postData['like'])
	post = Post.objects.get(id=postData['post_id'])
	user = User.objects.get(id=postData['user_id'])

	if postData['like']=="1":
		post.likes.add(user)


	user.feed.remove(post)

	post.views.add(user)

	return HttpResponse(status=200)

def createUser(request):
	print(request)
	postData = {
		'username': request.POST['username'],
		'first_name': request.POST['first_name'],
		'last_name': request.POST['last_name'],
		'email': request.POST['email'],
		'password': request.POST['password'],
		'confirm_pw': request.POST['confirm_pw'],
	}

	if not User.objects.register(postData):
		hashed_pw = bcrypt.hashpw(postData['password'].encode('utf-8'), bcrypt.gensalt())
		new_user = User.objects.create(username=postData['username'], first_name=postData['first_name'], last_name=postData['last_name'], email=postData['email'], hashed_pw=hashed_pw)
		print(new_user)

		return HttpResponse(status=201)

	return HttpResponse(status=400)

def createPost(request):
	postData = {
		'content': request.POST['content'],
		'posted_by': request.POST['posted_by'],
	}

	posted_by = User.objects.get(id=postData['posted_by'])
	new_post = Post.objects.create(content=postData['content'], posted_by=posted_by)
	
	new_post.likes.add(posted_by)
	new_post.views.add(posted_by)

	return HttpResponse(status=201)


def addPostToFeed(request):
	postData = {
		'post_id': request.POST['post_id'],
		'user_id': request.POST['user_id'],
	}

	user = User.objects.get(id=postData['user_id'])
	post = Post.objects.get(id=postData['post_id'])

	user.feed.add(post)

	return HttpResponse(status=200)

















