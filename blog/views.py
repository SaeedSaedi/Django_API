from django.shortcuts import get_object_or_404, render
from blog.models import Post
from django.core.paginator import Paginator


# Create your views here.
def index(request, cat_name=None, username=None):
    posts = Post.objects.filter(status=1)
    if cat_name:
        posts = posts.filter(category__name=cat_name)
    if username:
        posts = posts.filter(author__username=username)

    posts = Paginator(posts, 2)
    page_number = request.GET.get("page", 1)
    posts = posts.get_page(page_number)

    return render(request, "blog/home.html", context={"posts": posts})


def post_single(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=1)
    next_post = Post.objects.filter(id__gt=post.id, status=1).order_by("id").first()
    prev_post = Post.objects.filter(id__lt=post.id, status=1).order_by("-id").first()

    post.counted_views += 1
    post.save()
    return render(
        request,
        "blog/single.html",
        context={"post": post, "next_post": next_post, "prev_post": prev_post},
    )


def blog_search(request):
    search_query = request.GET.get("q", "")
    posts = Post.objects.filter(status=1, content__icontains=search_query)
    return render(request, "blog/home.html", context={"posts": posts})
