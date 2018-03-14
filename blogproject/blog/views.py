import markdown
from markdown.extensions.toc import TocExtension
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.utils.text import slugify
from comments.forms import CommentForm
from .models import Post, Category, Tag, ChikenSoup, Img


# Create your views here.

class HomePageView(ListView):
    """
    首页视图
    """
    model = Post
    template_name = 'blog/homepage.html'
    context_object_name = 'post_list'
    paginate_by = 2

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        paginator = context.get('paginator')
        page = context.get('page_obj')
        is_paginated = context.get('is_paginated')

        pagination_data = self.pagination_data(paginator, page, is_paginated)
        context.update(pagination_data)
        chicken_soup_data = self.chicken_soup_data()
        tag_data = self.tag_data()
        context.update(chicken_soup_data)
        context.update(tag_data)
        return context

    def chicken_soup_data(self):
        return {
            'chicken_soup_list': ChikenSoup.objects.all()
        }

    def tag_data(self):
        return {
            'tag_list': Tag.objects.all()
        }

    def pagination_data(self, paginator, page, is_paginated):
        if not is_paginated:
            return {}

        left = []

        right = []

        left_has_more = False

        right_has_more = False

        first = False

        last = False

        page_number = page.number

        total_pages = paginator.num_pages

        page_range = paginator.page_range

        if page_number == 1:

            right = page_range[page_number:page_number + 2]

            if right[-1] < total_pages - 1:
                right_has_more = True

            if right[-1] < total_pages:
                last = True

        elif page_number == total_pages:

            left = page_range[(page_number - 3) if (page_number - 3) > 0 else 0:page_number - 1]

            if left[0] > 2:
                left_has_more = True

            if left[0] > 1:
                first = True
        else:
            left = page_range[(page_number - 3) if (page_number - 3) > 0 else 0:page_number - 1]
            right = page_range[page_number:page_number + 2]

            # 是否需要显示最后一页和最后一页前的省略号
            if right[-1] < total_pages - 1:
                right_has_more = True
            if right[-1] < total_pages:
                last = True

            # 是否需要显示第 1 页和第 1 页后的省略号
            if left[0] > 2:
                left_has_more = True
            if left[0] > 1:
                first = True

        data = {
            'left': left,
            'right': right,
            'left_has_more': left_has_more,
            'right_has_more': right_has_more,
            'first': first,
            'last': last,
        }

        return data


class BlogView(ListView):
    """
    博客视图
    """
    model = Post
    template_name = 'blog/blog.html'
    context_object_name = 'post_list'
    paginate_by = 8

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        paginator = context.get('paginator')
        page = context.get('page_obj')
        is_paginated = context.get('is_paginated')

        pagination_data = self.pagination_data(paginator, page, is_paginated)
        tag_data = self.tag_data()
        context.update(pagination_data)
        context.update(tag_data)
        return context

    def tag_data(self):
        return {
            'tag_list': Tag.objects.all()
        }

    def pagination_data(self, paginator, page, is_paginated):
        if not is_paginated:
            return {}

        left = []

        right = []

        left_has_more = False

        right_has_more = False

        first = False

        last = False

        page_number = page.number

        total_pages = paginator.num_pages

        page_range = paginator.page_range

        if page_number == 1:

            right = page_range[page_number:page_number + 2]

            if right[-1] < total_pages - 1:
                right_has_more = True

            if right[-1] < total_pages:
                last = True

        elif page_number == total_pages:

            left = page_range[(page_number - 3) if (page_number - 3) > 0 else 0:page_number - 1]

            if left[0] > 2:
                left_has_more = True

            if left[0] > 1:
                first = True
        else:
            left = page_range[(page_number - 3) if (page_number - 3) > 0 else 0:page_number - 1]
            right = page_range[page_number:page_number + 2]

            # 是否需要显示最后一页和最后一页前的省略号
            if right[-1] < total_pages - 1:
                right_has_more = True
            if right[-1] < total_pages:
                last = True

            # 是否需要显示第 1 页和第 1 页后的省略号
            if left[0] > 2:
                left_has_more = True
            if left[0] > 1:
                first = True

        data = {
            'left': left,
            'right': right,
            'left_has_more': left_has_more,
            'right_has_more': right_has_more,
            'first': first,
            'last': last,
        }

        return data


class CategoryView(BlogView):
    """
    分类视图
    """

    def get_queryset(self):
        cate = get_object_or_404(Category, pk=self.kwargs.get('pk'))
        return super(CategoryView, self).get_queryset().filter(category=cate)


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/article.html'
    context_object_name = 'post'

    def get(self, request, *args, **kwargs):
        response = super(PostDetailView, self).get(request, *args, **kwargs)

        self.object.increase_views()

        return response

    def get_object(self, queryset=None):
        post = super(PostDetailView, self).get_object(queryset=None)
        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            TocExtension(slugify=slugify),
        ])

        post.body = md.convert(post.body)
        post.toc = md.toc
        return post

    def tag_data(self):
        return {
            'tag_list': Tag.objects.all()
        }

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        form = CommentForm()
        comment_list = self.object.comment_set.all()
        tag_data = self.tag_data()
        context.update(tag_data)
        context.update({
            'form': form,
            'comment_list': comment_list
        })

        return context


class TagView(ListView):
    model = Post
    template_name = 'blog/blog.html'
    context_object_name = 'post_list'

    def get_queryset(self):
        tag = get_object_or_404(Tag, pk=self.kwargs.get('pk'))
        return super(TagView, self).get_queryset().filter(tags=tag)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag_data = self.tag_data()

        context.update(tag_data)
        return context

    def tag_data(self):
        return {
            'tag_list': Tag.objects.all()
        }


def homepage(request):
    """
    首页视图
    :param request:
    :return:
    """
    # 获取文章
    post_list = Post.objects.all().order_by('-created_time')
    # 获取鸡汤
    chiken_soup_list = ChikenSoup.objects.all().order_by('-created_time')
    return render(request, 'blog/homepage.html',
                  context={'post_list': post_list, 'chicken_soup_list': chiken_soup_list})


def blog(request):
    """
    博客视图
    :param request:
    :return:
    """
    post_list = Post.objects.all().order_by('-created_time')
    chiken_soup_list = ChikenSoup.objects.all().order_by('-created_time')  # 暂时返回前三个
    return render(request, 'blog/blog.html',
                  context={'post_list': post_list, 'chicken_soup_list': chiken_soup_list})


def img(request):
    """
    图库视图
    :param request:
    :return:
    """
    img_list = Img.objects.all().order_by('-upload_time')
    tag_list = Tag.objects.all()
    #
    # for i in img_list:
    #     print(i.img.url)
    return render(request, 'blog/img.html', context={'img_list': img_list, 'tag_list': tag_list})


def timeline(request):
    """
    时间轴
    :param request:
    :return:
    """
    # 获得全部文章
    post_list = Post.objects.all().order_by('-created_time')

    return render(request, 'blog/timeline.html', context={'post_list': post_list})


def article(request, pk):
    """
    文章详情
    :param request:
    :param pk: 文章id
    :return:
    """
    post = get_object_or_404(Post, pk=pk)
    post.increase_views()
    # 使用markdown渲染文章
    post.body = markdown.markdown(post.body,
                                  extensions=[
                                      'markdown.extensions.extra',
                                      'markdown.extensions.codehilite',
                                      'markdown.extensions.toc',
                                  ])
    form = CommentForm()
    comment_list = post.comment_set.all()
    context = {
        'post': post,
        'form': form,
        'comment_list': comment_list
    }

    return render(request, 'blog/article.html', context=context)


def category(request, pk):
    """
    分类视图
    :param request:
    :param pk:
    :return:
    """
    cate = get_object_or_404(Category, pk=pk)
    post_list = Post.objects.filter(category=cate).order_by('-created_time')
    return render(request, 'blog/blog.html', context={'post_list': post_list})

def search(request):
    q = request.GET.get('q')
    error_msg = ''
    print(q)

    if not q:
        error_msg = "请输入关键词"
        return render(request, 'blog/blog.html', {'error_msg': error_msg})

    post_list = Post.objects.filter(Q(title__icontains=q) | Q(body__icontains=q))
    return render(request, 'blog/blog.html', {'error_msg': error_msg,
                                               'post_list': post_list})


def test(request):
    """
    测试视图
    :param request:
    :return:
    """
    # 获取文章
    post_list = Post.objects.all().order_by('-created_time')
    # 获取鸡汤
    chiken_soup_list = ChikenSoup.objects.all().order_by('-created_time')
    print(chiken_soup_list)
    return render(request, 'blog/tem.html',
                  context={'post_list': post_list, 'chicken_soup_list': chiken_soup_list})