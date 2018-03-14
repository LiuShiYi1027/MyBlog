# -*- coding: utf-8 -*-
# @Time    : 2018/2/21 下午12:39
# @Author  : LiuShiYi
# @Site    : 
# @File    : forms.py

from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['name', 'email', 'url', 'text']
