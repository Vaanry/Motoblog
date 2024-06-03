import datetime
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Post, Category, Comments, Follow, Location
from .forms import PostForm, CommentForm, LocationForm
from users.forms import UserUpdateForm
from django.urls import reverse_lazy
from django.views.generic import (ListView, CreateView,
                                  UpdateView, DeleteView, DetailView)
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from users.models import Owners


User = get_user_model()

now = datetime.datetime.now()
# Create your views here.


class BlogListView(ListView):
    queryset = Post.objects.filter(
        is_published=True,
        category__is_published=True,
        pub_date__lte=now,
    ).prefetch_related(
        'comments'
    )

    ordering = '-pub_date'
    paginate_by = 10
    template_name = 'blog/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        if user.is_authenticated:
            context['unreaded_dialogs_counter'] = user.chat_set.unreaded(user=user).count()
        for post in context['post_list']:
            post.comments_count = len(
                post._prefetched_objects_cache['comments'])
        return context


class CategoryListView(ListView):

    def get_queryset(self):
        self.category = self.kwargs["category_slug"]
        return Post.objects.filter(
            category__slug=self.category,
            is_published=True,
            category__is_published=True,
            pub_date__lte=now).prefetch_related(
            'category', 'comments')

    ordering = '-pub_date'
    paginate_by = 10
    template_name = 'blog/category.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = Category.objects.values(
            'title',
            'description'
        ).filter(slug=self.kwargs["category_slug"]).first()
        user = self.request.user
        if user.is_authenticated:
            context['unreaded_dialogs_counter'] = user.chat_set.unreaded(user=user).count()
        for post in context['post_list']:
            post.comments_count = len(
                post._prefetched_objects_cache['comments'])
        return context


class LocationListView(ListView):

    def get_queryset(self):
        self.location = self.kwargs["location"]
        return Post.objects.filter(
            location__name=self.location,
            is_published=True,
            category__is_published=True,
            pub_date__lte=now).prefetch_related('comments')

    ordering = '-pub_date'
    paginate_by = 10
    template_name = 'blog/location.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)       
        context['location'] = self.location
        user = self.request.user
        if user.is_authenticated:
            context['unreaded_dialogs_counter'] = user.chat_set.unreaded(user=user).count()
        for post in context['post_list']:
            post.comments_count = len(
                post._prefetched_objects_cache['comments'])
        return context
    

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        if user.is_authenticated:
            context['unreaded_dialogs_counter'] = user.chat_set.unreaded(user=user).count()
        context['form'] = CommentForm()
        context['comments'] = (
            self.object.comments.select_related(
                'author').order_by('-created_at')
        )
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    login_url = '/auth/login/'
    redirect_field_name = 'next'
    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('blog:profile', kwargs={'username':
                            self.request.user.username})
        

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        return context


class EditPostView(UpdateView, LoginRequiredMixin):
    model = Post
    template_name = 'blog/create.html'
    form_class = PostForm

    def form_valid(self, form):
        return super().form_valid(form)

    def get_success_url(self):
        pk = self.request.resolver_match.kwargs['pk']
        return reverse_lazy('blog:post_detail', kwargs={'pk':
                            pk})

    def dispatch(self, request, *args, **kwargs):
        instance = get_object_or_404(Post, pk=kwargs['pk'])
        if instance.author != request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class DeletePostView(DeleteView, LoginRequiredMixin):
    model = Post
    template_name = 'blog/create.html'

    def get_success_url(self):
        # Здесь 'blog:profile'-это имя URL-адреса страницы профиля пользователя
        return reverse_lazy('blog:profile', kwargs={'username':
                            self.request.user.username})

    def dispatch(self, request, *args, **kwargs):
        instance = get_object_or_404(Post, pk=kwargs['pk'])
        if instance.author != request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


def profile(request, username):
    template_name = 'blog/profile.html'
    profile = get_object_or_404(User.objects.filter(username=username))
    posts = Post.objects.filter(
        author__username=username,
    ).prefetch_related(
        'comments'
    )
    for post in posts:
        post.comments_count = len(
            post._prefetched_objects_cache['comments'])
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    following = request.user.is_authenticated and (
        request.user.follower.filter(author=profile).exists()
    )
    bikes = Owners.objects.filter(owner=profile)
    context = {
        'profile': profile,
        'page_obj': page_obj,
        'following': following,
        'bikes': bikes,
    }
    if request.user.is_authenticated:
        user = get_object_or_404(User.objects.filter(username=request.user.username))
        context['unreaded_dialogs_counter'] = user.chat_set.unreaded(user=user).count()
    return render(request, template_name, context)


class EditProfileView(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'blog/user.html'
    form_class = UserUpdateForm
    slug_url_kwarg = "username"
    slug_field = "username"
    login_url = '/auth/login/'
    redirect_field_name = 'next'

    def form_valid(self, form):
        return super().form_valid(form)
    
    def get_success_url(self):
        username = self.request.resolver_match.kwargs['username']
        return reverse_lazy('blog:profile', kwargs={'username':
                            username})
    
    def dispatch(self, request, *args, **kwargs):
        instance = get_object_or_404(User, username=kwargs['username'])
        if not request.user.is_authenticated:
            return redirect(self.login_url)
            
        if instance.username != str(request.user):
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


@login_required
def add_comment(request, pk):
    post = get_object_or_404(Post, pk=pk)
    form = CommentForm(request.POST)
    id = post.id
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
    return redirect('blog:post_detail', id)


@login_required
def edit_comment(request, id, pk):
    instance = get_object_or_404(Comments, pk=pk)
    if instance.author != request.user:
        raise PermissionDenied
    form = CommentForm(request.POST or None, instance=instance)
    context = {'form': form,
               'comment': instance}
    if form.is_valid():
        form.save()
        return redirect('blog:post_detail', id)
    return render(request, 'blog/comment.html', context)


@login_required
def delete_comment(request, id, pk):
    instance = get_object_or_404(Comments, pk=pk)
    if instance.author != request.user:
        raise PermissionDenied
    form = CommentForm(instance=instance)
    context = {'form': form}
    if request.method == 'POST':
        instance.delete()
        return redirect('blog:post_detail', id)
    return render(request, 'blog/comment.html', context)



class FollowListView(ListView,  LoginRequiredMixin):

    def get_queryset(self):
        self.username = self.request.user
        return Post.objects.filter(
            author__following__user=self.username,
            is_published=True,
            category__is_published=True,
            pub_date__lte=now).prefetch_related(
        'comments'
    )

    ordering = '-pub_date'
    paginate_by = 10
    template_name = 'blog/follow.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['unreaded_dialogs_counter'] = user.chat_set.unreaded(user=user).count()
        for post in context['post_list']:
            post.comments_count = len(
                post._prefetched_objects_cache['comments'])
        return context

    
@login_required
def profile_follow(request, username):
    author = get_object_or_404(User, username=username)
    if request.user != author:
        Follow.objects.get_or_create(user=request.user, author=author)
    return redirect('blog:profile', username=username)


@login_required
def profile_unfollow(request, username):
    author = get_object_or_404(User, username=username)
    Follow.objects.filter(user=request.user, author=author).delete()
    return redirect('blog:profile', username=username)


class LocationCreateView(LoginRequiredMixin, CreateView):
    redirect_field_name = 'next'
    model = Location
    form_class = LocationForm
    template_name = 'blog/create_location.html'

    def get_success_url(self):
        return reverse_lazy('blog:create_post')

    def form_valid(self, form):
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['unreaded_dialogs_counter'] = user.chat_set.unreaded(user=user).count()
        return context