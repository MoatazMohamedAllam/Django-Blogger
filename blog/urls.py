from django.urls import path
from . import views
from .views import PostListView,PostCreateView,PostUpdateView,PostDeleteView

app_name='blog'

urlpatterns = [
    path('', PostListView.as_view(), name='blog-home'),
    path('about/', views.about, name='blog-about'),
    path('post/new/', PostCreateView.as_view(), name='create-post'),
    path('post/detail/<int:post_id>', views.post_detail, name='detail'),
    path('post/update/<int:pk>', PostUpdateView.as_view(), name='update'),
    path('post/delete/<int:pk>', PostDeleteView.as_view(), name='delete'),
    path('posts/<str:username>', views.user_posts, name='user-posts'),
]
