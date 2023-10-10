from django.urls import path

from .views import PostList, PostDetail, PostCreate

app_name = 'bboardapp'
urlpatterns = [
    path('', PostList.as_view(), name='post_list'),
    path('<int:pk>', PostDetail.as_view(), name='post_detail'),
    path('post_create/', PostCreate.as_view(), name='post_create'),
]

