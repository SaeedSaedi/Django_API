from unicodedata import category
from django import template
from blog.models import Category, Post
register = template.Library()

@register.simple_tag(name="totalposts")
def total_posts():
    
    posts = Post.objects.filter(status=1).count()
    return posts

@register.simple_tag(name="get_posts")
def get_posts():
    posts = Post.objects.filter(status=1).order_by('-created_on')
    return posts

@register.filter
def snippet(v, n):
    return  v[:n] + "..."

@register.inclusion_tag('blog/popularposts.html')
def popularposts(n=3):
    posts = Post.objects.filter(status=1).order_by('-counted_views')[0:n]
    return {'posts':posts}

@register.inclusion_tag('blog/post-category.html')
def post_category():
    posts = Post.objects.filter(status=1)
    categories = Category.objects.all()
    response = {}
    for name in categories:
        response[name]= posts.filter(category=name).count()
        
    return {'category': response}