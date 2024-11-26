from django.shortcuts import get_object_or_404, render, redirect
from django.utils import timezone
from blog.models import Post
from django.core.paginator import Paginator
from blog.forms import ContactForm, NewsletterForm
from django.contrib import messages
from blog.forms import CommentForm


# Create your views here.
def index(request, cat_name=None, username=None, tag_name=None):
    if request.method == "POST":
        form = NewsletterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Thank you for subscribing to our newsletter!")
            return redirect("blog:index")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.capitalize()}: {error}")
    else:
        form = NewsletterForm()

    now = timezone.now()
    posts = Post.objects.filter(status=1, published_at__lte=now)
    if cat_name:
        posts = posts.filter(category__name=cat_name)
    if username:
        posts = posts.filter(author__username=username)
    if tag_name:
        posts = posts.filter(tags__name__in=[tag_name])

    posts = Paginator(posts, 2)
    page_number = request.GET.get("page", 1)
    posts = posts.get_page(page_number)

    return render(
        request, "blog/home.html", context={"posts": posts, "newsletter_form": form}
    )


def post_single(request, post_id):
    now = timezone.now()
    post = get_object_or_404(Post, id=post_id, status=1, published_at__lte=now)
    comments = post.comments.filter(approved=True).order_by("-created_at")
    next_post = (
        Post.objects.filter(id__gt=post.id, status=1, published_at__lte=now)
        .order_by("id")
        .first()
    )
    prev_post = (
        Post.objects.filter(id__lt=post.id, status=1, published_at__lte=now)
        .order_by("-id")
        .first()
    )

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect("blog:post_detail", post_id=post.id)
    else:
        form = CommentForm()

    context = {
        "post": post,
        "comments": comments,
        "next_post": next_post,
        "prev_post": prev_post,
        "form": form,
    }

    post.counted_views += 1
    post.save()
    return render(
        request,
        "blog/single.html",
        context=context,
    )


def blog_search(request):
    now = timezone.now()
    search_query = request.GET.get("q", "")
    posts = Post.objects.filter(
        status=1, published_at__lte=now, content__icontains=search_query
    )
    return render(request, "blog/home.html", context={"posts": posts})


def contact_us(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            contact_instance = form.save(commit=False)
            contact_instance.name = "anonymous"
            contact_instance.save()
            form.save()
            messages.success(
                request, "Thank you! Your message has been sent successfully."
            )
            return redirect("blog:contact")
    else:
        form = ContactForm()
    return render(request, "blog/contact.html", {"form": form})
