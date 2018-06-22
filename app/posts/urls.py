from django.conf.urls import url

from posts.views import post_list, post_detail


urlpatterns = [
    url('', post_list),
    url('<int:pk>/', post_detail),
]
