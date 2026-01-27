from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse
from django.db.models import Q, Count
from django.core.paginator import Paginator
from .models import Profile, BlogPost, Comment, Category, Follow, Notification, Tag
from .forms import (UserRegisterForm, UserUpdateForm, ProfileUpdateForm, 
                   BlogPostForm, CommentForm, ReplyForm, SearchForm, TagForm)
from django.contrib.auth import logout

class DraftListView(LoginRequiredMixin, ListView):
    model = BlogPost
    template_name = 'blog/draft_list.html'
    context_object_name = 'drafts'
    paginate_by = 10

    def get_queryset(self):
        return BlogPost.objects.filter(
            author=self.request.user,
            status='draft'
        ).order_by('-created_at')

def home(request):
    posts = BlogPost.objects.filter(status='published').order_by('-created_at')
    popular_posts = BlogPost.objects.filter(status='published').order_by('-view_count')[:5]
    categories = Category.objects.all()
    
    paginator = Paginator(posts, 10)  # Show 10 posts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'popular_posts': popular_posts,
        'categories': categories,
    }
    
    return render(request, 'blog/home.html', context)

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now log in.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    
    return render(request, 'blog/register.html', {'form': form})

@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    
    # Get user's blog posts
    posts = BlogPost.objects.filter(author=request.user).order_by('-created_at')
    
    # Get followers and following
    followers = Follow.objects.filter(followed=request.user).select_related('follower')
    following = Follow.objects.filter(follower=request.user).select_related('followed')
    
    context = {
        'u_form': u_form,
        'p_form': p_form,
        'posts': posts,
        'followers': followers,
        'following': following,
    }
    
    return render(request, 'blog/profile.html', context)

@login_required
def edit_profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    
    context = {
        'u_form': u_form,
        'p_form': p_form,
    }
    
    return render(request, 'blog/edit_profile.html', context)

def user_profile(request, username):
    user = get_object_or_404(User, username=username)
    posts = BlogPost.objects.filter(author=user, status='published').order_by('-created_at')
    
    # Check if the current user is following this user
    is_following = False
    if request.user.is_authenticated:
        is_following = Follow.objects.filter(follower=request.user, followed=user).exists()
    
    # Get followers and following
    followers = Follow.objects.filter(followed=user).select_related('follower')
    following = Follow.objects.filter(follower=user).select_related('followed')
    
    context = {
        'profile_user': user,
        'posts': posts,
        'is_following': is_following,
        'followers': followers,
        'following': following,
    }
    
    return render(request, 'blog/user_profile.html', context)

@login_required
def follow_user(request, username):
    user_to_follow = get_object_or_404(User, username=username)
    
    # Check if already following
    if request.user != user_to_follow:
        Follow.objects.get_or_create(follower=request.user, followed=user_to_follow)
        messages.success(request, f'You are now following {username}.')
    
    return redirect('user_profile', username=username)

@login_required
def unfollow_user(request, username):
    user_to_unfollow = get_object_or_404(User, username=username)
    
    # Delete the follow relationship
    Follow.objects.filter(follower=request.user, followed=user_to_unfollow).delete()
    messages.success(request, f'You have unfollowed {username}.')
    
    return redirect('user_profile', username=username)

@login_required
def create_post(request):
    if request.method == 'POST':
        form = BlogPostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            
            # Handle existing tags
            tags = form.cleaned_data.get('tags')
            if tags:
                form.save_m2m()  # This saves the existing tags relation
            
            # Handle custom tags
            custom_tags = form.cleaned_data.get('custom_tags', '')
            if custom_tags:
                tag_names = [name.strip() for name in custom_tags.split(',') if name.strip()]
                for tag_name in tag_names:
                    tag, created = Tag.objects.get_or_create(name=tag_name.lower())
                    post.tags.add(tag)
            
            if post.status == 'draft':
                messages.success(request, 'Your draft has been saved!')
            else:
                messages.success(request, 'Your blog post has been published!')
            return redirect('post_detail', pk=post.pk)
    else:
        form = BlogPostForm()
    
    context = {
        'form': form,
        'title': 'New Post',
    }
    
    return render(request, 'blog/post_form.html', context)

def post_detail(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    
    # Increment view count
    post.view_count += 1
    post.save()
    
    # Get comments (top-level only)
    comments = post.comments.filter(parent=None).order_by('created_at')
    
    # Check if user has liked or disliked
    is_liked = False
    is_disliked = False
    if request.user.is_authenticated:
        is_liked = post.likes.filter(id=request.user.id).exists()
        is_disliked = post.dislikes.filter(id=request.user.id).exists()
    
    # Comment form
    comment_form = CommentForm()
    reply_form = ReplyForm()
    
    # Related posts based on category and tags
    similar_posts = BlogPost.objects.filter(status='published').exclude(id=post.id)
    
    if post.category:
        similar_posts = similar_posts.filter(category=post.category)
    
    if post.tags.exists():
        post_tags_ids = post.tags.values_list('id', flat=True)
        similar_posts = similar_posts.filter(tags__in=post_tags_ids).distinct()
    
    similar_posts = similar_posts.order_by('-created_at')[:3]
    
    context = {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
        'reply_form': reply_form,
        'is_liked': is_liked,
        'is_disliked': is_disliked,
        'similar_posts': similar_posts,
        'categories': Category.objects.all(),
    }
    
    return render(request, 'blog/post_detail.html', context)

@login_required
def edit_post(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    
    # Check if user is the author
    if post.author != request.user:
        messages.error(request, 'You are not authorized to edit this post.')
        return redirect('post_detail', pk=post.pk)
    
    if request.method == 'POST':
        form = BlogPostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            
            # Handle tags - now using the ModelMultipleChoiceField 
            # The form.save_m2m() will handle the tags
            form.save_m2m()
            
            messages.success(request, 'Your blog post has been updated!')
            return redirect('post_detail', pk=post.pk)
    else:
        form = BlogPostForm(instance=post)
    
    context = {
        'form': form,
        'title': 'Edit Post',
        'post': post,
    }
    
    return render(request, 'blog/post_form.html', context)

@login_required
def delete_post(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    
    # Check if user is the author
    if post.author != request.user:
        messages.error(request, 'You are not authorized to delete this post.')
        return redirect('post_detail', pk=post.pk)
    
    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Your post has been deleted!')
        return redirect('home')
    
    context = {
        'post': post,
    }
    
    return render(request, 'blog/post_confirm_delete.html', context)

@login_required
def add_comment(request, post_pk):
    post = get_object_or_404(BlogPost, pk=post_pk)
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            messages.success(request, 'Your comment has been added!')
    
    return redirect('post_detail', pk=post_pk)

@login_required
def reply_to_comment(request, comment_pk):
    parent_comment = get_object_or_404(Comment, pk=comment_pk)
    
    if request.method == 'POST':
        form = ReplyForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.post = parent_comment.post
            reply.author = request.user
            reply.parent = parent_comment
            reply.save()
            messages.success(request, 'Your reply has been added!')
    
    return redirect('post_detail', pk=parent_comment.post.pk)

@login_required
def like_post(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    
    # If user already liked this post, remove like
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        liked = False
    else:
        # If user disliked this post, remove dislike first
        if post.dislikes.filter(id=request.user.id).exists():
            post.dislikes.remove(request.user)
        
        # Add like
        post.likes.add(request.user)
        liked = True
    
    # If AJAX request
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        data = {
            'liked': liked,
            'likes_count': post.total_likes(),
            'dislikes_count': post.total_dislikes(),
        }
        return JsonResponse(data)
    
    return redirect('post_detail', pk=pk)

@login_required
def dislike_post(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    
    # If user already disliked this post, remove dislike
    if post.dislikes.filter(id=request.user.id).exists():
        post.dislikes.remove(request.user)
        disliked = False
    else:
        # If user liked this post, remove like first
        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
        
        # Add dislike
        post.dislikes.add(request.user)
        disliked = True
    
    # If AJAX request
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        data = {
            'disliked': disliked,
            'likes_count': post.total_likes(),
            'dislikes_count': post.total_dislikes(),
        }
        return JsonResponse(data)
    
    return redirect('post_detail', pk=pk)

@login_required
def like_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    
    # If user already liked this comment, remove like
    if comment.likes.filter(id=request.user.id).exists():
        comment.likes.remove(request.user)
        liked = False
    else:
        # If user disliked this comment, remove dislike first
        if comment.dislikes.filter(id=request.user.id).exists():
            comment.dislikes.remove(request.user)
        
        # Add like
        comment.likes.add(request.user)
        liked = True
    
    # If AJAX request
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        data = {
            'liked': liked,
            'likes_count': comment.total_likes(),
            'dislikes_count': comment.total_dislikes(),
        }
        return JsonResponse(data)
    
    return redirect('post_detail', pk=comment.post.pk)

@login_required
def dislike_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    
    # If user already disliked this comment, remove dislike
    if comment.dislikes.filter(id=request.user.id).exists():
        comment.dislikes.remove(request.user)
        disliked = False
    else:
        # If user liked this comment, remove like first
        if comment.likes.filter(id=request.user.id).exists():
            comment.likes.remove(request.user)
        
        # Add dislike
        comment.dislikes.add(request.user)
        disliked = True
    
    # If AJAX request
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        data = {
            'disliked': disliked,
            'likes_count': comment.total_likes(),
            'dislikes_count': comment.total_dislikes(),
        }
        return JsonResponse(data)
    
    return redirect('post_detail', pk=comment.post.pk)

def category_posts(request, name):
    category = get_object_or_404(Category, name=name)
    posts = BlogPost.objects.filter(category=category, status='published').order_by('-created_at')
    
    paginator = Paginator(posts, 10)  # Show 10 posts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'category': category,
        'page_obj': page_obj,
    }
    
    return render(request, 'blog/category_posts.html', context)

def tag_posts(request, name):
    tag = get_object_or_404(Tag, name=name)
    posts = BlogPost.objects.filter(status='published', tags=tag).order_by('-created_at')
    
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'tag': tag,
        'page_obj': page_obj,
    }
    
    return render(request, 'blog/tag_posts.html', context)

def search_posts(request):
    search_form = SearchForm(request.GET)
    results = []
    
    if 'query' in request.GET:
        query = request.GET.get('query')
        category_id = request.GET.get('category')
        
        if query:
            # Base query
            post_query = BlogPost.objects.filter(status='published')
            
            # Add category filter if selected
            if category_id:
                post_query = post_query.filter(category_id=category_id)
            
            # Search in title and content
            results = post_query.filter(
                Q(title__icontains=query) | 
                Q(content__icontains=query)
            ).order_by('-created_at')
    
    paginator = Paginator(results, 10)  # Show 10 posts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'search_form': search_form,
        'page_obj': page_obj,
        'query': request.GET.get('query', ''),
    }
    
    return render(request, 'blog/search_results.html', context)

@login_required
def admin_panel(request):
    # Check if user is superuser
    if not request.user.is_superuser:
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('home')
    
    total_users = User.objects.count()
    total_posts = BlogPost.objects.count()
    total_comments = Comment.objects.count()
    
    # Recent activity
    recent_posts = BlogPost.objects.order_by('-created_at')[:10]
    recent_comments = Comment.objects.order_by('-created_at')[:10]
    recent_users = User.objects.order_by('-date_joined')[:10]
    
    context = {
        'total_users': total_users,
        'total_posts': total_posts,
        'total_comments': total_comments,
        'recent_posts': recent_posts,
        'recent_comments': recent_comments,
        'recent_users': recent_users,
    }
    
    return render(request, 'blog/admin_panel.html', context)

@login_required
def admin_posts(request):
    # Check if user is superuser
    if not request.user.is_superuser:
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('home')
    
    posts = BlogPost.objects.all().order_by('-created_at')
    
    paginator = Paginator(posts, 20)  # Show 20 posts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
    }
    
    return render(request, 'blog/admin_posts.html', context)

@login_required
def admin_comments(request):
    # Check if user is superuser
    if not request.user.is_superuser:
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('home')
    
    comments = Comment.objects.all().order_by('-created_at')
    
    paginator = Paginator(comments, 20)  # Show 20 comments per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
    }
    
    return render(request, 'blog/admin_comments.html', context)

@login_required
def admin_users(request):
    # Check if user is superuser
    if not request.user.is_superuser:
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('home')
    
    users = User.objects.all().order_by('-date_joined')
    
    paginator = Paginator(users, 20)  # Show 20 users per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
    }
    
    return render(request, 'blog/admin_users.html', context)

def logout_view(request):
    logout(request)
    messages.success(request, 'You have been successfully logged out.')
    return redirect('home')

def create_tag(request):
    if request.method == 'POST':
        form = TagForm(request.POST)
        if form.is_valid():
            tag = form.save()
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'status': 'success',
                    'tag_id': tag.id,
                    'tag_name': tag.name
                })
            messages.success(request, f'Tag "{tag.name}" has been created successfully!')
            return redirect('create_post')
        else:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'status': 'error',
                    'errors': form.errors
                }, status=400)
    else:
        form = TagForm()
    
    return render(request, 'blog/create_tag.html', {'form': form})

def get_tags(request):
    query = request.GET.get('query', '')
    tags = Tag.objects.filter(name__icontains=query).values('id', 'name')[:10]
    return JsonResponse(list(tags), safe=False)
