from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('profile/<str:username>/', views.user_profile, name='user_profile'),
    path('follow/<str:username>/', views.follow_user, name='follow_user'),
    path('unfollow/<str:username>/', views.unfollow_user, name='unfollow_user'),
    path('logout/', views.logout_view, name='logout'),
    
    # Blog posts
    path('post/new/', views.create_post, name='create_post'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/<int:pk>/edit/', views.edit_post, name='edit_post'),
    path('post/<int:pk>/delete/', views.delete_post, name='delete_post'),
    path('post/<int:pk>/like/', views.like_post, name='like_post'),
    path('post/<int:pk>/dislike/', views.dislike_post, name='dislike_post'),
    path('drafts/', views.DraftListView.as_view(), name='draft_list'),
    
    # Comments
    path('post/<int:post_pk>/comment/', views.add_comment, name='add_comment'),
    path('comment/<int:comment_pk>/reply/', views.reply_to_comment, name='reply_to_comment'),
    path('comment/<int:pk>/like/', views.like_comment, name='like_comment'),
    path('comment/<int:pk>/dislike/', views.dislike_comment, name='dislike_comment'),
    
    # Categories and Tags
    path('category/<str:name>/', views.category_posts, name='category_posts'),
    path('tag/<str:name>/', views.tag_posts, name='tag_posts'),
    
    # Search
    path('search/', views.search_posts, name='search_posts'),
    
    # Admin panel for moderation
    path('admin-panel/', views.admin_panel, name='admin_panel'),
    path('admin-panel/posts/', views.admin_posts, name='admin_posts'),
    path('admin-panel/comments/', views.admin_comments, name='admin_comments'),
    path('admin-panel/users/', views.admin_users, name='admin_users'),
    
    # Tags
    path('tag/create/', views.create_tag, name='create_tag'),
    path('tag/search/', views.get_tags, name='get_tags'),
] 