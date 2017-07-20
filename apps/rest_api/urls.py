from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.index),
	url(r'^login$', views.login),
	url(r'^createUser$', views.createUser),
	url(r'^createPost$', views.createPost),
	url(r'^addPostToFeed$', views.addPostToFeed),
	url(r'^swipePost$', views.swipePost),
]