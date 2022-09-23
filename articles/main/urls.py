from django.urls import path
from .views import *

urlpatterns = [
    path('', PostsListView.as_view(), name='posts_list'),
    path('post/create/', PostCreateView.as_view(), name='post_create'),
    path('post/<int:pk>/', post_detail, name='post_detail'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post_update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),
]
