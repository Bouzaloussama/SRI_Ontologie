from django.conf.urls import url
from django.urls import path

#from . views import All_posts, Post
from . import views

app_name = 'Ontology'


urlpatterns = [
	url(r'^$', views.Ontology, name='Ontology'),
	url(r'^All_class$', views.All_class, name='All_class'),
	#url(r'^(?P<id>\d+)$', views.Post, name='Post'),
]
