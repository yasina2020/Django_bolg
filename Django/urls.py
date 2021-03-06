from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from app01 import views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', views.article_list, name='index'),

    path('article/', include('app01.urls', namespace='article')),

    path('userprofile/', include('userprofile.urls', namespace='userprofile')),

    path('comment/', include('comment.urls', namespace='comment')),

    path('password-reset/', include('password_reset.urls')),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)