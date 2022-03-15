from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# Register your models here.
from book.models import *

admin.site.site_title = '后台管理'
admin.site.site_header = "后台管理"


@admin.register(UserProfile)
class UserProfileAdmin(UserAdmin):
    list_display = ('id','username','mobile','email','gender')
    fieldsets = (
               ('基本信息', {'fields':['username', 'password', 'mobile','gender','email', 'is_staff',]}),
               ('活跃信息', {'fields': ['date_joined', 'last_login']}),
    )
    list_per_page = 50
    list_display_links = ('id','username')
    list_filter = ('username','mobile','email')
#admin.site.register(UserProfile,UserAdmin)

@admin.register(Book)
class BooksAdmin(admin.ModelAdmin):
    list_display = ('id','name','category','author','publisher','count','create_time',)
    list_per_page = 50
    list_filter = ('name','category',)
    list_display_links = ('id','name')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id','name')
    list_display_links = ('id','name')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id','username','book','m_time','status','operator')
    list_per_page = 50
    list_filter = ('status','id','book','username',)
    #list_editable = ('status',)
    list_display_links = ('id','username','book')
