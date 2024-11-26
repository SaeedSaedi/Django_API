from django.contrib.syndication.views import Feed
from django.urls import reverse
from blog.models import Post
from django.utils import timezone


class LatestEntriesFeed(Feed):
    title = "Blog newest posts"
    link = "/rss/feed/"
    description = "My blog rss feed"
    now = timezone.now()

    def items(self):
        return Post.objects.filter(status=True, published_at__lte=self.now)[:10]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.content[:100]
