from django.shortcuts import render, HttpResponse, redirect
from .models import ArticlePost, ArticleColumn
from .forms import ArticlePostForm
from django.contrib.auth.models import User
import markdown
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from comment.models import Comment


# Create your views here.

def article_list(request):
    search = request.GET.get('search')
    order = request.GET.get('order')
    column = request.GET.get('column')
    tag = request.GET.get('tags')
    articles = ArticlePost.objects.all()

    if search:
        articles = articles.filter(
            Q(title__icontains=search) |
            Q(body__icontains=search)
        )
    else:
        print('search:', search, '-------------')
        search = ''

    if column is not None and column.isdigit():
        articles = articles.filter(column=column)

    if tag and tag != 'None':
        articles = articles.filter(tags__name__in=[tag])

    if order == 'total_views':
        articles = articles.order_by('-total_views')

    paginator = Paginator(articles, 6)
    page = request.GET.get('page')
    articles = paginator.get_page(page)
    context = {'articles': articles,
               'order': order,
               'search': search,
               'tag': tag,
               }
    return render(request, 'article/list.html', context)


@login_required(login_url='/userprofile/login/')
def article_delete(request, id):
    if request.method == 'POST':
        article = ArticlePost.objects.get(id=id)
        article.delete()
        return redirect("app01:article_list")
    else:
        return HttpResponse("仅允许post请求")


def article_detail(request, id):
    # 取出 相应 的文章
    article = ArticlePost.objects.get(id=id)
    comments = Comment.objects.filter(article=id)
    article.total_views += 1
    # update_fields=[]指定了数据库只更新total_views字段
    article.save(update_fields=['total_views'])
    md = markdown.Markdown(
        extensions=[
            # 包含 缩写、表格等常用扩展
            'markdown.extensions.extra',
            # 语法高亮扩展
            'markdown.extensions.codehilite',
            # 目录扩展
            'markdown.extensions.toc',
        ])
    article.body = md.convert(article.body)
    context = {'article': article, 'toc': md.toc, 'comments': comments}
    return render(request, 'article/detail.html', context)


# 写文章的视图
@login_required(login_url='/userprofile/login/')
def article_create(request):
    # 判断用户是否提交数据
    if request.method == "POST":
        # 将提交的数据赋值到表单实例中
        article_post_form = ArticlePostForm(data=request.POST, request.FILES)
        # 判断提交的数据是否满足模型的要求
        if article_post_form.is_valid():
            # 保存数据，但暂时不提交到数据库中
            # 因为POST的表单中包含了图片文件，所以要将request.FILES也一并绑定到表单类中，否则图片无法正确保存
            new_article = article_post_form.save(commit=False)
            # 指定数据库中 id=1 的用户为作者
            # 如果你进行过删除数据表的操作，可能会找不到id=1的用户
            # 此时请重新创建用户，并传入此用户的id
            new_article.author = User.objects.get(id=request.user.id)
            if request.POST['column'] != 'none':
                new_article.cloumn = ArticleColumn.objects.get(id=request.POST['column'])
            # 将新文章保存到数据库中
            new_article.save()
            # 保存 tags 的多对多关系
            article_post_form.save_m2m()
            # 完成后返回到文章列表
            return redirect("app01:article_list")
        # 如果数据不合法，返回错误信息
        else:
            return HttpResponse("表单内容有误，请重新填写。")
    # 如果用户请求获取数据
    else:
        # 创建表单类实例
        article_post_form = ArticlePostForm()
        columns = ArticleColumn.objects.all()
        # 赋值上下文
        context = {'article_post_form': article_post_form, 'columns': columns}
        # 返回模板
        return render(request, 'article/create.html', context)


@login_required(login_url='/userprofile/login/')
def article_update(request, id):
    article = ArticlePost.objects.get(id=id)
    if request.method == 'POST':
        # 将提交的数据赋值到表单实例中
        article_post_form = ArticlePostForm(data=request.POST)
        print(article_post_form)
        # 判断提交的数据是否满足模型的要求
        if article_post_form.is_valid():
            # 保存新写入的 title、body 数据并保存
            article.title = request.POST['title']
            article.body = request.POST['body']
            if request.POST['column'] != 'none':
                article.column = ArticleColumn.objects.get(id=request.POST['column'])
            else:
                article.column = None
            article.save()
            # 完成后返回到修改后的文章中。需传入文章的 id 值
            return redirect("app01:article_detail", id=id)
        # 如果数据不合法，返回错误信息
        else:
            return HttpResponse("表单内容有误，请重新填写。")

        # 如果用户 GET 请求获取数据
    else:
        # 创建表单类实例
        article_post_form = ArticlePostForm()
        columns = ArticleColumn.objects.all()
        # 赋值上下文，将 article 文章对象也传递进去，以便提取旧的内容
        context = {'article': article, 'article_post_form': article_post_form, 'columns': columns, }
        # 将响应返回到模板中
        return render(request, 'article/update.html', context)
