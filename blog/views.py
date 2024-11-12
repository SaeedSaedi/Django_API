from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from blog.models import Post

# Create your views here.
def index(request):
    now = timezone.now()
    post = Post.objects.filter(published_at__lte=now)
    return render(request, 'blog/home.html',context={'posts':post})

def post_single(request,post_id):
    post = get_object_or_404(Post,id=post_id)
    post.counted_views += 1
    post.save()
    return render(request, 'blog/single.html',context={'post':post})