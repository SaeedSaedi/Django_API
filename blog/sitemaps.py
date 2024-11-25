from django.contrib.sitemaps import Sitemap
from blog.models import Post
from django.utils import timezone


class BlogSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.5

    def items(self):
        now = timezone.now()
        return Post.objects.filter(status=True, published_at__lte=now)

    def lastmod(self, obj):
        return obj.published_at
