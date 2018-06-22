from django.conf.urls import url

from . import views

app_name = 'posts'
urlpatterns = [
    url('', views.post_list, name='post_list'),
    url('<int:pk>/', views.post_detail, name='post_detail'),
]
