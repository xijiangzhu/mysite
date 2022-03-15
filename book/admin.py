from django.contrib import admin

# Register your models here.
from book.models import *

admin.site.site_title = '后台管理'
admin.site.site_header = "后台管理"

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id','username','mobile','email','gender')
    list_per_page = 50
    ordering = ('-id',)
    list_filter = ('username','mobile','email')

@admin.register(Book)
class BooksAdmin(admin.ModelAdmin):
    list_display = ('id','name','category','author','publisher','count','create_time',)
    list_per_page = 50
    ordering = ('id',)
    list_filter = ('name','category',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id','name')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id','username','book','m_time','status')
    list_per_page = 50
    list_filter = ('status','id','book','username')