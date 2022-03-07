from attr import field
from django.contrib import admin

# Register your models here.
from book.models import *

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id','username','mobile','email','gender')
    list_per_page = 50
    ordering = ('-id',)

@admin.register(Books)
class BooksAdmin(admin.ModelAdmin):
    list_display = ('id','name','author','publisher','status','create_time','borrower','borrow_time')
    list_per_page = 50
    ordering = ('id',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id','name')
    