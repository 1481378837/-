from django.shortcuts import render
from django.views.generic import ListView

from blog.models import Post
from blog.views import CommonViewMixin

class HottestView(CommonViewMixin, ListView):
    queryset = Post.hot_posts()
    paginate_by = 5
    context_object_name = 'hottest_list'
    template_name = 'blog/list_hot.html'

class LatestView(CommonViewMixin, ListView):
    queryset = Post.latest_posts()
    paginate_by = 5
    context_object_name = 'latest_list'
    template_name = 'blog/list_late.html'