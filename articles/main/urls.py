from django.urls import path
from .views import *

urlpatterns = [
    path('', PostsListView.as_view(), name='posts_list'),
    path('post/create/', create_post, name='create_post'),
    path('post/<slug:slug>/update/', update_post, name='post_update'),
    path('post/<slug:slug>/delete/', PostDeleteView.as_view(), name='post_delete'),

    path('post/<slug:slug>/', post_detail, name='post'),
]
