from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import ListView, DeleteView
from django.urls import reverse_lazy, reverse
from django.shortcuts import get_object_or_404

from .forms import PostForm, CommentForm, UserRegistrationForm
from .models import Post, Comment


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            return redirect('posts_list')
    else:
        user_form = UserRegistrationForm()
    return render(request, 'accounts/register.html', {'user_form': user_form})


@login_required
def profile(request):
    profile_ = User.objects.get(email=request.user.email)
    profile_posts = Post.objects.filter(registered_author=request.user)
    template = 'accounts/profile.html'
    context = {
        'profile': profile_,
        'profile_posts': profile_posts,
    }
    return render(request, template_name=template, context=context)


class PostsListView(ListView):
    model = Post
    template_name = 'posts/posts_list.html'


def create_post(request):
    form = PostForm()
    template = 'posts/post_create.html'

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            if request.user.is_authenticated:
                form.save(commit=False)
                form.instance.registered_author = request.user
            form.save()
            redirect_post = Post.objects.order_by('-pk').first()
            return redirect(reverse('post', kwargs={'slug': redirect_post.slug}))

    context = {'form': form}
    return render(request, template_name=template, context=context)


def update_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    form = PostForm(instance=post)
    template = 'posts/post_update.html'

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect(reverse('post', kwargs={'slug': post.slug}))

    context = {
        'form': form,
        'can_update': can_update
    }
    return render(request, template_name=template, context=context)


def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    comments = Comment.objects.filter(post=post)
    can_update = True if post.registered_author == request.user or post.unregistered_author else False
    print(post.unregistered_author )

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.post = post
            if request.user.is_authenticated:
                form.registered_author = request.user
            form.save()
            return redirect(reverse_lazy('post', kwargs={'slug': post.slug}))
    else:
        form = CommentForm()
        context = {
            "form": form,
            "post": post,
            "comments": comments,
            'can_update':can_update
        }
        return render(request, template_name='posts/post_detail.html', context=context)


class PostDeleteView(DeleteView):
    model = Post
    template_name = 'posts/post_delete.html'
    success_url = reverse_lazy('posts_list')
