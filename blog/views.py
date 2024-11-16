from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from blog.models import Post

# Create your views here.
def index(request,cat_name=None):
    now = timezone.now()
    posts = Post.objects.filter(status=1,published_at__lte=now)
    if cat_name:
        posts = posts.filter(category__name=cat_name)
    return render(request, 'blog/home.html',context={'posts':posts})

def post_single(request,post_id):
    now = timezone.now()
    post = get_object_or_404(Post,id=post_id,status=1,published_at__lte=now)
    next_post = Post.objects.filter(id__gt=post.id,status=1).order_by('id').first()
    prev_post = Post.objects.filter(id__lt=post.id,status=1).order_by('-id').first()
    
    post.counted_views += 1
    post.save()
    return render(request, 'blog/single.html',context={'post':post,'next_post':next_post,'prev_post':prev_post})

