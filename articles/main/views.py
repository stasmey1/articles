from django.shortcuts import render, redirect
from django.views.generic import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from .forms import *

from .models import *


class PostsListView(ListView):
    model = Post
    template_name = 'posts/posts_list.html'


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    # fields = ['title', 'body', 'image', ]
    template_name = 'posts/post_create.html'
    login_url = 'login'

    def form_valid(self, form):
        form.instance.autor = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    # fields = ['title', 'body', ]
    template_name = 'posts/post_update.html'
    login_url = 'login'


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = Comment.objects.filter(post=post)

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.autor = request.user
            form.post = post
            new_comment = form.save()
            return redirect(reverse_lazy('post', kwargs={'slug': new_comment.slug}))
    else:
        form = CommentForm()
        context = {
            "form": form,
            "post": post,
            "comments": comments,
        }
        return render(request, template_name='posts/post_detail.html', context=context)


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'posts/post_delete.html'
    success_url = reverse_lazy('posts_list')
    login_url = 'login'
