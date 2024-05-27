from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone
from taggit.managers import TaggableManager


# Создание собственного менеджера
class PublishedManager(models.Manager):
    def get_queryset(self):  # Набор queryset, который будет исполнен
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)


# Create your models here.
class Post(models.Model):
    # choices - 'DF', 'Draft', labels - 'Draft', values - 'DF'
    # .name, .value, .label
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'

    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250,
                            unique_for_date='publish')  #
    # метка, содержит только буквы, цифры,
    # знаки подчеркивания или дефисы
    # Удобно использовать для поиска и URL
    # По умолчанию подразумевается индекс

    # Взаимосвязь многие-к-одному
    author = models.ForeignKey(User,  # Модель User из фреймворка аутентификации
                               on_delete=models.CASCADE,
                               related_name='blog_posts'  # Позволит легко обращаться к связанным
                               # объектам, user.blog_posts
                               )

    body = models.TextField()

    publish = models.DateTimeField(default=timezone.now)  # Дата и время публикации поста
    # Проверка на уникальность проводится только по дате (не по времени)!
    created = models.DateTimeField(auto_now_add=True)  # Дата и время создания поста
    # параметр сохраняет дату автоматически при создании
    updated = models.DateTimeField(auto_now=True)
    # auto_now - обновление автоматически времени при сохранении объекта

    status = models.CharField(max_length=2,
                              choices=Status.choices,
                              default=Status.DRAFT)

    tags = TaggableManager()

    # Хранение в обратном хронологическом порядке
    class Meta:
        ordering = ['-publish']  # - дефис = убыващий порядок
        indexes = [
            models.Index(fields=['-publish'])
        ]

    objects = models.Manager()  # Менеджер, применяемый по умолчанию
    published = PublishedManager()  # Если мы переопределяем менеджер, то дефолтный стирается

    # Так что, чтобы сохранить его, мы пишем два менеджера

    def __str__(self):
        return self.title

    # Канонический адрес для модели
    def get_absolute_url(self):
        return reverse('blog_app:post_detail', args=(self.publish.year,
                                                     self.publish.month,
                                                     self.publish.day,
                                                     self.slug,))


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    # Можно использовать post.comments.all()
    # По умолчанию post.comment_set.all()
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)  # Деактивация неуместных комментариев

    class Meta:
        ordering = ['created']
        indexes = [
            models.Index(fields=['created'])
        ]

    def __str__(self):
        return f'Comment by {self.name} on {self.post}'
