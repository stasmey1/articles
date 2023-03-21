from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_list_or_404
from django.views.generic import ListView, DeleteView
from django.urls import reverse_lazy, reverse
from django.shortcuts import get_object_or_404

from .forms import PostForm, CommentForm, UserRegistrationForm
from .models import Post, Comment

from django.contrib.auth import login


def register(request):
    form = UserRegistrationForm()
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            login(request, new_user)
            return redirect('posts_list')
    return render(request, 'accounts/register.html', locals())


@login_required
def profile(request):
    profile_ = User.objects.get(pk=request.user.pk)
    profile_posts = Post.objects.filter(author=request.user)
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
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save(commit=False)
            if request.user.is_authenticated:
                form.instance.author = request.user
                form.instance.anonimus = False
            form.save()
            redirect_post = Post.objects.order_by('-pk').first()
            return redirect(reverse_lazy('post', kwargs={'slug': redirect_post.slug}))
    form = PostForm()
    template = 'posts/post_create.html'
    return render(request, template_name=template, context={'form': form})


def update_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    form = PostForm(instance=post)
    template = 'posts/post_update.html'

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect(reverse('post', kwargs={'slug': post.slug}))
    return render(request, template_name=template, context={'form': form, })


def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    author_pk = post.author.pk if post.author else None
    comments = Comment.objects.filter(post=post)
    can_update = True if post.author == request.user or post.anonimus else False

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.post = post
            if request.user.is_authenticated:
                form.author = request.user
                form.anonimus = False
            form.save()
            return redirect(reverse_lazy('post', kwargs={'slug': post.slug}))
    form = CommentForm()
    return render(request, 'posts/post_detail.html', locals())


def author_post_list(request, pk):
    autor = get_object_or_404(User, pk=pk)
    posts = get_list_or_404(Post, author=autor)
    return render(request, 'posts/autor_post_list.html', locals())


class PostDeleteView(DeleteView):
    model = Post
    template_name = 'posts/post_delete.html'
    success_url = reverse_lazy('posts_list')
