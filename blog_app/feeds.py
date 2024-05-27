import markdown
from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords_html
from django.urls import reverse_lazy

from blog_app.models import Post


class LatestPostFeed(Feed):
    title = 'My blog'  # RSS <title>
    link = reverse_lazy('blog_app:post_list')  # RSS <link>
    # Позволяет использовать URL адрес до того как конфигурация была загружена
    description = 'New posts of my blog'  # RSS <description>

    def items(self):
        return Post.published.all()[:5]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return truncatewords_html(markdown.markdown(item.body), 30)

    def item_pubdate(self, item):
        return item.publish
