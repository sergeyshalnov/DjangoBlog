from django.views.generic import View

from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse
from django.shortcuts import get_object_or_404

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Q

from .models import Post, Tag
from .utils import *
from .forms import TagForm, PostForm


# Posts functions

class PostDetail(ObjectDetailMixin, View):
    model = Post
    template = 'blog/post/post_detail.html'


class PostCreate(LoginRequiredMixin, ObjectCreateMixin, View):
    model_form = PostForm
    template = 'blog/post/post_create_form.html'
    raise_exception = True


class PostUpdate(LoginRequiredMixin, ObjectUpdateMixin, View):
    model = Post
    model_form = PostForm
    template = 'blog/post/post_update_form.html'
    raise_exception = True


class PostDelete(LoginRequiredMixin, ObjectDeleteMixin, View):
    model = Post
    template = 'blog/post/post_delete_form.html'
    redirect_url = 'posts_list_url'
    raise_exception = True


def posts_list(request):
    search_query = request.GET.get('search', '')

    if search_query:
        posts = Post.objects.filter(Q(title__icontains=search_query) | Q(body__icontains=search_query))
    else:
        posts = Post.objects.all()

    paginator = Paginator(posts, 2)
    page_number = request.GET.get('page', 1)
    page = paginator.get_page(page_number)

    is_paginated = page.has_other_pages()

    if page.has_previous():
        prev_page_url = '?page={}'.format(page.previous_page_number())
        prev_page_url = prev_page_url + ('&search={}'.format(search_query) if search_query else '')
    else:
        prev_page_url = ''

    if page.has_next():
        next_page_url = '?page={}'.format(page.next_page_number())
        next_page_url = next_page_url + ('&search={}'.format(search_query) if search_query else '')
    else:
        next_page_url = ''

    context = {
        'page_object': page,
        'is_paginated': is_paginated,
        'prev_page_url': prev_page_url,
        'next_page_url': next_page_url,
        'search_query': search_query
    }

    return render(request, 'blog/post/posts_list.html', context=context)


# Tag functions

class TagDetail(ObjectDetailMixin, View):
    model = Tag
    template = 'blog/tag/tag_detail.html'


class TagCreate(LoginRequiredMixin, ObjectCreateMixin, View):
    model_form = TagForm
    template = 'blog/tag/tag_create_form.html'
    raise_exception = True


class TagUpdate(LoginRequiredMixin, ObjectUpdateMixin, View):
    model = Tag
    model_form = TagForm
    template = 'blog/tag/tag_update_form.html'
    raise_exception = True

class TagDelete(LoginRequiredMixin, ObjectDeleteMixin, View):
    model = Tag
    template = 'blog/tag/tag_delete_form.html'
    redirect_url = 'tags_list_url'
    raise_exception = True


def tags_list(request):
    tags = Tag.objects.all()
    return render(request, 'blog/tag/tags_list.html', context={'tags': tags})


