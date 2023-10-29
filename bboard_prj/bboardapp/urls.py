from django.urls import path

from .views import PostList, PostDetail, PostCreate, СheckComment, PostUpdate, FilterPostsView, FilterMyPostsView, \
    Search, NewsListView, NewsAddView, NewsDetail

app_name = 'bboardapp'
urlpatterns = [
    path('', PostList.as_view(), name='posts'),
    path('filter/', FilterPostsView.as_view(), name='filter'),
    path('my_posts/', FilterMyPostsView.as_view(), name='my_posts'),
    path('search/', Search.as_view(), name='search'),
    path('<int:pk>', PostDetail.as_view(), name='post_detail'),
    path('news/', NewsListView.as_view(), name='news'),
    path('news/<int:pk>', NewsDetail.as_view(), name='news_detail'),
    path('news_add/', NewsAddView.as_view(), name='news_add'),
    path('post_create/', PostCreate.as_view(), name='post_create'),
    path('post_update/<int:pk>', PostUpdate.as_view(), name='post_update'),
    path('comment_update/<int:pk>', СheckComment.as_view(), name='cmnt_updt'),
    # path('run_function/', views.run_function),
    # path('image-request/', image_request, name='image-request'),
]

