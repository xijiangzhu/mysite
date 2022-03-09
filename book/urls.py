from django.urls import  path
from . import views

urlpatterns = [
    # 用户管理
    path('',views.index,name='index'),
    path('login/',views.login,name='login'),
    path('register/',views.register,name='register'),
    path('logout/',views.logout,name='logout'),

    # 图书管理
    path('book/list/',views.book_list,name='book_list'),
    path('book/<int:sid>/detail/',views.book_detail,name='book_detail'),
    path('book/<int:bid>/borrow/',views.book_borrow,name='book_borrow'),
    path('book/my_borrow/',views.my_borrow,name='my_borrow'),
    path('book/borrow_hostory/',views.borrow_hostory,name='borrow_hostory'),

]