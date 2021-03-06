from django.db import models

from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from PIL import Image

from taggit.managers import TaggableManager


class ArticleColumn(models.Model):
    title = models.CharField(max_length=100, blank=True)
    created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title


class ArticlePost(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    avatar = models.ImageField(upload_to='article/%Y%m%d', blank=True)
    body = models.TextField()  # 保存大量文本用TextField
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(auto_now=True)
    total_views = models.PositiveIntegerField(default=0)
    tags = TaggableManager(blank=True)
    column = models.ForeignKey(
        ArticleColumn,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='article'
    )

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('article:article_detail', args=[self.id])

    # 修改尺寸
    # save()是models内置 每次保存都会调用该方法
    def save(self, *args, **kwargs):
        # 作用是先把数据先给保存了
        article = super(ArticlePost, self).save(*args, **kwargs)
        # self.avater 判断该文章是否有标题图
        # not kwargs.get('update_fields')
        if self.avatar and not kwargs.get('update_fields'):
            # 打开图片
            image = Image.open(self.avatar)
            # 获取分辨率
            (x, y) = image.size
            # 新设分辨率
            _x = 400
            _y = int(_x * (y / x))
            resized_image = image.resize((_x, _y), Image.ANTIALIAS)
            # 保存修改后的图片
            resized_image.save(self.avatar.path)
        return article
