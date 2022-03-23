from django.contrib import admin

# Register your models here.
from blog.models import Banner,Category,Tag,Tui,Article,Link

# @admin.register(Article)
# class ArticleAdmin(admin.ModelAdmin):
# 	list_display = ('id','category','title','tui','user','views','created_time')
# 	list_per_page = 50
# 	ordering = ('-created_time',)
# 	list_display_links = ('id','title')

# @admin.register(Category)
# class CategoryAdmin(admin.ModelAdmin):
# 	list_display = ('id','name')

# @admin.register(Tag)
# class TagAdmin(admin.ModelAdmin):
# 	list_display = ('id','name')

# @admin.register(Tui)
# class TuiAdmin(admin.ModelAdmin):
# 	list_display = ('id','name')

# @admin.register(Link)
# class LinkAdmin(admin.ModelAdmin):
# 	list_display = ('id','name','linkurl')



