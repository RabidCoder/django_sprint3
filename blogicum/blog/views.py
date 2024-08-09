from django.conf import settings
from django.http import HttpResponse, HttpRequest
from django.shortcuts import get_object_or_404, render
from django.utils.timezone import now

from .models import Post, Category


def get_post():
    return Post.objects.select_related(
        'author', 'location', 'category',
    ).filter(
        is_published=True,
        category__is_published=True,
        pub_date__lt=now()
    )


def index(request: HttpRequest) -> HttpResponse:
    posts = get_post()[:settings.POSTS_BY_PAGE]
    return render(request, 'blog/index.html', {'post_list': posts})


def post_detail(request: HttpRequest, post_id: int) -> HttpResponse:
    post = get_object_or_404(get_post(), id=post_id)
    return render(request, 'blog/detail.html', {'post': post})


def category_posts(request: HttpRequest, category_slug: str) -> HttpResponse:
    category = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True
    )
    posts = get_post().filter(category=category)
    context = {
        'post_list': posts,
        'category': category
    }
    return render(request, 'blog/category.html', context)
