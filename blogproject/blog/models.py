from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
import markdown
from django.utils.html import strip_tags


# Create your models here.

class Category(models.Model):
    """
    文章分类
    """
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('blog:category', kwargs={'pk': self.pk})


class Tag(models.Model):
    """
    文章标签
    """
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Post(models.Model):
    """
    文章详情
    """
    title = models.CharField(max_length=70)  # 标题
    body = models.TextField()  # 正文
    created_time = models.DateTimeField()  # 文章创建时间
    modified_time = models.DateTimeField()  # 文章修改时间
    excerpt = models.CharField(max_length=200, blank=True)  # 文章摘要
    category = models.ForeignKey(Category)  # 文章分类(一篇文章只有一个分类)
    tags = models.ManyToManyField(Tag, blank=True)  # 一篇文章可以有多个标签
    author = models.ForeignKey(User)  # 文章作者
    img = models.ImageField(upload_to='img')

    views = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

    def increase_views(self):
        self.views += 1
        self.save(update_fields=['views'])

    def get_absolute_url(self):
        return reverse('blog:article', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['-created_time']

    def save(self, *args, **kwargs):
        # 如果没有填写摘要
        if not self.excerpt:
            # 首先实例化一个 Markdown 类，用于渲染 body 的文本
            md = markdown.Markdown(extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
            ])
            self.excerpt = strip_tags(md.convert(self.body))[:54]

        # 调用父类的 save 方法将数据保存到数据库中
        super(Post, self).save(*args, **kwargs)


class ChikenSoup(models.Model):
    """
    心灵鸡汤
    """
    content = models.TextField()  # 鸡汤内容
    img = models.ImageField(upload_to='img')
    reference = models.CharField(max_length=100)  # 出处
    created_time = models.DateField()  # 构建时间

    def __str__(self):
        return self.content


class Img(models.Model):
    """
    图片
    """
    name = models.CharField(max_length=100)  # 图片名称
    img = models.ImageField(upload_to='img')  # 图片
    description = models.TextField(blank=True)  # 描述
    upload_time = models.DateTimeField(blank=True)  # 上传时间

    def __str__(self):
        return self.name
