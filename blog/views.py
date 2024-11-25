from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from blog.models import Post
from django.core.paginator import Paginator
from blog.forms import ContactForm, NewsletterForm
from django.contrib import messages


# Create your views here.
def index(request, cat_name=None, username=None):
    if request.method == "POST":
        form = NewsletterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Thank you for subscribing to our newsletter!")
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

    posts = Paginator(posts, 2)
    page_number = request.GET.get("page", 1)
    posts = posts.get_page(page_number)

    return render(
        request, "blog/home.html", context={"posts": posts, "newsletter_form": form}
    )


def post_single(request, post_id):
    now = timezone.now()
    post = get_object_or_404(Post, id=post_id, status=1, published_at__lte=now)
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

    post.counted_views += 1
    post.save()
    return render(
        request,
        "blog/single.html",
        context={"post": post, "next_post": next_post, "prev_post": prev_post},
    )


def blog_search(request):
    now = timezone.now()
    search_query = request.GET.get("q", "")
    posts = Post.objects.filter(
        status=1, published_at__lte=now, content__icontains=search_query
    )
    return render(request, "blog/home.html", context={"posts": posts})


def contact_us(request):
    success_message = None
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            success_message = "Thank you! Your message has been sent successfully."
            return render(
                request,
                "blog/contact.html",
                {"form": ContactForm(), "success_message": success_message},
            )
    else:
        form = ContactForm()
    return render(
        request, "blog/contact.html", {"form": form, "success_message": success_message}
    )
