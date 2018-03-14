# -*- coding: utf-8 -*-
# @Time    : 2018/2/17 下午4:33
# @Author  : LiuShiYi
# @Site    : 
# @File    : urls.py
from django.conf.urls import url
from . import views
from django.conf.urls.static import static
from django.conf import settings

app_name = 'blog'
urlpatterns = [
                  url(r'^$', views.HomePageView.as_view(), name='homepage'),  # 首页
                  url(r'homepage/', views.homepage),
                  url(r'^blog/', views.BlogView.as_view(), name='blog'),  # 博客视图
                  url(r'^img/', views.img, name='img'),  # 图库视图
                  # url(r'^img/', views.ImgView.as_view(), name='img'),
                  url(r'^timeline', views.timeline, name='timeline'),  # 时间轴
                  url(r'^post/(?P<pk>[0-9]+)/$', views.PostDetailView.as_view(), name='article'),  # 文章详情
                  url(r'^category/(?P<pk>[0-9]+)/$', views.CategoryView.as_view(), name='category'),
                  url(r'^tag/(?P<pk>[0-9]+)/$', views.TagView.as_view(), name='tag'),
                  url(r'^search/$', views.search, name='search'),
                  url(r'^test/', views.test),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
