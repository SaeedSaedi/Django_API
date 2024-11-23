from django import template
from blog.models import Category, Post
from django.core.paginator import Paginator
from django.utils import timezone

register = template.Library()


@register.simple_tag(name="totalposts")
def total_posts():
    now = timezone.now()
    posts = Post.objects.filter(status=1, published_at__lte=now).count()
    return posts


@register.simple_tag(name="get_posts")
def get_posts(page_number=1):
    now = timezone.now()
    posts = Post.objects.filter(status=1, published_at__lte=now).order_by("-created_at")
    paginator = Paginator(posts, 3)
    page = paginator.get_page(page_number)
    return page


@register.filter
def snippet(v, n):
    return v[:n] + "..."


@register.inclusion_tag("blog/popularposts.html")
def popularposts(n=3):
    now = timezone.now()
    posts = Post.objects.filter(status=1, published_at__lte=now).order_by(
        "-counted_views"
    )[0:n]
    return {"posts": posts}


@register.inclusion_tag("blog/post-category.html")
def post_category():
    now = timezone.now()
    posts = Post.objects.filter(status=1, published_at__lte=now)
    categories = Category.objects.all()
    response = {}
    for name in categories:
        response[name] = posts.filter(category=name).count()

    return {"category": response}


@register.simple_tag(name="get_last_posts")
def get_last_post():
    now = timezone.now()
    return Post.objects.filter(status=1, published_at__lte=now).order_by("-created_at")[
        :6
    ]
