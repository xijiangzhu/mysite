from django.urls import  path,re_path,include
from django.views.static import serve
from mysite import settings
from . import views

urlpatterns = [
    path('',views.index,name='book_index'),
    path('login/',views.login,name='book_login'),
    path('register/',views.register,name='book_register'),
    path('logout/',views.logout,name='book_logout'),
    
    # 图片
    re_path(r'media/(?P<path>.*)$',serve,{'document_root':settings.MEDIA_ROOT}),
 
    # 图书管理
    path('list/',views.list,name='book_list'),
    path('<int:bid>/detail/',views.detail,name='book_detail'),
    path('<int:bid>/borrow/',views.borrow,name='book_borrow'),
    path('<int:oid>/return/',views.returning,name='book_returning'),
    path('myborrow/',views.myborrow,name='book_myborrow'),
    path('record/',views.record,name='book_record'),
    path('usercenter/',views.usercenter,name='book_usercenter'),
    path('search/',views.search,name='book_search'),
    path('<int:oid>/cancel_reserve/',views.cancel_reserve,name='book_cancel_reserve'),
    path('<int:oid>/cancel_return/',views.cancel_return,name='book_cancel_return'),

    # 后台审核功能
    path('borrow_out/<int:oid>/',views.borrow_out,name='borrow_out'),
    path('return_in/<int:oid>/',views.return_in,name='renturn_in'),

    #path('captcha/', include('captcha.urls')), # 验证码
    path('password-reset/', include('password_reset.urls')), # 重置密码

]