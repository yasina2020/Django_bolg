from django.urls import path
from app01 import tests
from app01 import views

app_name = 'app01'

urlpatterns = [
    path('test/', tests.test),
    path('article_list/', views.article_list, name='article_list'),

    # 这里需要传递名叫id的整数到视图函数中去。

    path('article_detail/<int:id>/', views.article_detail, name='article_detail'),
    path('article_create/', views.article_create, name='article_create'),
    path('article_delete/<int:id>/', views.article_delete, name='article_delete'),
    path('article_update/<int:id>/', views.article_update, name='article_update'),



]

