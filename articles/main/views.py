from django.shortcuts import render, redirect
from django.views.generic import ListView, DeleteView
from django.urls import reverse_lazy, reverse
from django.shortcuts import get_object_or_404

from .forms import PostForm, CommentForm
from .models import Post, Comment


class PostsListView(ListView):
    model = Post
    template_name = 'posts/posts_list.html'


def create_post(request):
    form = PostForm()
    template = 'posts/post_create.html'

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            new_post = Post.objects.order_by('-pk').first()
            return redirect(reverse('post', kwargs={'slug': new_post.slug}))

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

    context = {'form': form}
    return render(request, template_name=template, context=context)


def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    comments = Comment.objects.filter(post=post)

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.post = post
            form.save()
            return redirect(reverse_lazy('post', kwargs={'slug': post.slug}))
    else:
        form = CommentForm()
        context = {
            "form": form,
            "post": post,
            "comments": comments,
        }
        return render(request, template_name='posts/post_detail.html', context=context)


class PostDeleteView(DeleteView):
    model = Post
    template_name = 'posts/post_delete.html'
    success_url = reverse_lazy('posts_list')
