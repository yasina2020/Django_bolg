from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from app01.models import ArticlePost
from .forms import CommentFrom

# Create your views here.
@login_required(login_url='/userprofile/login')
def post_comment(request, article_id):
    article = get_object_or_404(ArticlePost, id=article_id)

    if request.method == 'POST':
        comment_form = CommentFrom(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.article = article
            new_comment.user = request.user
            new_comment.save()
            return redirect(article)
            """
            redirect()：返回到一个适当的url中：
            即用户发送评论后，重新定向到文章详情页面。
            当其参数是一个Model对象时，
            会自动调用这个Model对象的get_absolute_url()方法。
            """
        else:
            return HttpResponse('内容有误')
    else:
        return HttpResponse('发表评论仅接受post请求')