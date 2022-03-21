from django.urls import path,include,re_path
from blog import views
from django.conf import settings
from django.views.static import serve 

urlpatterns = [
    path('',views.index,name='index'),
    path('ueditor/',include('blog.DjangoUeditor.urls')),
    re_path('^media/(?P<path>.*)$',serve,{'document_root':settings.MEDIA_ROOT}),
    path('list-<int:lid>.html',views.list,name='list'),
    path('show-<int:sid>.html',views.show,name='show'),
    path('tag/<tag>',views.tag,name='tags'),
    path('s/',views.search,name='search'),
    path('about/',views.about,name='about'),
]