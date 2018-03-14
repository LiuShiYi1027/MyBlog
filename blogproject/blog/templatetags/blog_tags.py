# -*- coding: utf-8 -*-
# @Time    : 2018/2/21 下午10:48
# @Author  : LiuShiYi
# @Site    : 
# @File    : blog_tags.py

from ..models import Tag
from django import template
from django.db.models.aggregates import Count

register = template.Library()


@register.simple_tag
def get_tags():
    return Tag.objects.annotate(num_posts=Count('post')).filter(num_posts__gt=0)
