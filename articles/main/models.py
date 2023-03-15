from django.db import models
from django.urls import reverse
from django.utils import timezone
from pytils.translit import slugify


class Post(models.Model):
    title = models.CharField('Заголовок', max_length=100)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    text = models.TextField('Текст', max_length=10000)
    date = models.DateTimeField('Дата публикации', auto_now_add=True)
    autor = models.CharField('Автор', max_length=30, null=True)
    image = models.ImageField('Изображение', upload_to='post_image', null=True, blank=True)
    published = models.BooleanField('Публикация', default=True)

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
    autor = models.CharField('Автор', default='noname', blank=True, max_length=100)
    comment = models.TextField('Комментарий', max_length=225)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.autor} - {self.comment[:20]}'
