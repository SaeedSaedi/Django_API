from django import template
from blog.models import Category, Post
from django.core.paginator import Paginator

register = template.Library()


@register.simple_tag(name="totalposts")
def total_posts():

    posts = Post.objects.filter(status=1).count()
    return posts


@register.simple_tag(name="get_posts")
def get_posts(page_number=1):
    posts = Post.objects.filter(status=1).order_by("-created_at")
    paginator = Paginator(posts, 3)
    page = paginator.get_page(page_number)
    return page


@register.filter
def snippet(v, n):
    return v[:n] + "..."


@register.inclusion_tag("blog/popularposts.html")
def popularposts(n=3):
    posts = Post.objects.filter(status=1).order_by("-counted_views")[0:n]
    return {"posts": posts}


@register.inclusion_tag("blog/post-category.html")
def post_category():
    posts = Post.objects.filter(status=1)
    categories = Category.objects.all()
    response = {}
    for name in categories:
        response[name] = posts.filter(category=name).count()

    return {"category": response}


@register.simple_tag(name="get_last_posts")
def get_last_post():
    return Post.objects.filter(status=1).order_by("-created_at")[:6]
