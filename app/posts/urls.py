from django.conf.urls import url
from django.urls import path

# 상대경로 방식
# 풀네임을 다 써주면 절대경로
from . import views

app_name = 'posts'
urlpatterns = [
    # 포스트 리스트 페이지를 불러온다
    path('', views.post_list, name='post_list'),
    # 포스트 디테일 페이지를 불러온다
    path('<int:pk>/', views.post_detail, name='post_detail'),
    # 글작성 페이지를 불러온다
    path('create', views.post_create, name='post_create'),
    # 글삭제 기능을 호출한다.
    path('<int:pk>/delete/', views.delete, name='delete'),
    path('<int:pk>/comment/', views.comment_create, name='comment_create'),
]
