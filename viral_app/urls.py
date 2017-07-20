"""viral_app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Exampl-s:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.db.models import Count

from rest_framework import routers, serializers, viewsets
from apps.rest_api.models import User, Post

class FeedUserSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = User
		fields = ('id', 'username')

class FeedSerializer(serializers.HyperlinkedModelSerializer):
	posted_by = FeedUserSerializer(read_only=True)
	class Meta:
		model = Post
		fields = ('id', 'content', 'posted_by', 'likes', 'views')



class PostSerializer(serializers.HyperlinkedModelSerializer):

	class Meta:
		model = Post
		fields = ('id', 'content', 'posted_by', 'feeds', 'likes','views', 'created_at', 'updated_at')

	def get_like_count(self, obj):
		return obj.like_set.all().count()

class UserSerializer(serializers.HyperlinkedModelSerializer):
	feed = FeedSerializer(read_only=True,many=True)
	likes = PostSerializer(read_only=True,many=True)
	class Meta:
		model = User
		fields = ('id','username','first_name', 'last_name', 'email', 'feed', 'created_at', 'updated_at', 'likes')

class UserViewSet(viewsets.ModelViewSet):
	queryset = User.objects.all()
	serializer_class = UserSerializer

class PostViewSet(viewsets.ModelViewSet):
	queryset = Post.objects.all()
	serializer_class = PostSerializer

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'posts', PostViewSet)

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('apps.rest_api.urls')),
    url(r'^rest-api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls')),
]
