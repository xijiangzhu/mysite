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
    path('book/<int:sid>/show/',views.book_show,name='book_show'),
    path('book/<int:bid>/borrow/',views.book_borrow,name='book_borrow'),

]