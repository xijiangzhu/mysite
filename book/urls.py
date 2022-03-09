from django.urls import  path,re_path
from django.views.static import serve
from mysite import settings
from . import views

urlpatterns = [
    # 用户管理
    path('',views.index,name='index'),
    path('login/',views.login,name='login'),
    path('register/',views.register,name='register'),
    path('logout/',views.logout,name='logout'),
    
    # 图片
    re_path(r'media/(?P<path>.*)$',serve,{'document_root':settings.MEDIA_ROOT}),
 
    # 图书管理
    path('book/list/',views.book_list,name='book_list'),
    path('book/<int:sid>/detail/',views.book_detail,name='book_detail'),
    path('book/<int:bid>/borrow/',views.book_borrow,name='book_borrow'),
    path('book/myborrow/',views.book_myborrow,name='book_myborrow'),
    path('book/borrowrecord/',views.book_borrowrecord,name='book_borrowrecord'),

]