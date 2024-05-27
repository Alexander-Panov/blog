from django.contrib.sitemaps import Sitemap

from blog_app.models import Post


class PostSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.9

    def items(self):
        return Post.published.all()  # По умолчанию Django применяет get_absolute_url
    # location для указания url каждого объекта

    def lastmod(self, obj):  # получает возвращаемый методом items(), возвращает время его последнего обновления
        return obj.updated
