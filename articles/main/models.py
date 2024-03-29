from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone
from pytils.translit import slugify


class Post(models.Model):
    title = models.CharField('Заголовок', max_length=100)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    text = models.TextField('Текст', max_length=10000)
    date = models.DateTimeField('Дата публикации', auto_now_add=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts', blank=True,
                               null=True)
    anonimus = models.BooleanField('Аноним', blank=True, default=True)
    anonimus_name = models.CharField('Аноним', max_length=10, blank=True, default='Аноним')
    image = models.ImageField('Изображение', upload_to='post_image', null=True, blank=True)

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        ordering = ['-date']

    def __str__(self):
        return self.title[:20]

    def get_absolute_url(self):
        return reverse('post', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        self.slug = slugify(f'{self.title}{str(timezone.now())[10:]}')
        super().save(*args, **kwargs)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments', verbose_name='Статья', blank=True,
                             null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments', blank=True,
                               null=True)
    anonimus = models.BooleanField('Аноним', blank=True, default=True)
    anonimus_name = models.CharField('Аноним', max_length=10, default='Аноним')
    text = models.CharField('Комментарий', max_length=225)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['-date']

    def __str__(self):
        return f'{self.author} - {self.text[:20]}'
