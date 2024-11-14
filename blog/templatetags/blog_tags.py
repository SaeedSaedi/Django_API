from django import template
from blog.models import Post
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
def popularposts():
    posts = Post.objects.filter(status=1).order_by('-counted_views')[0:3]
    return {'posts':posts}