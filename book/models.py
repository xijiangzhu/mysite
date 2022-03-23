from django import forms
from django.db import models
from django.contrib import auth

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django import forms
from django.utils.html import format_html


# 用户信息
class UserProfile(AbstractUser):
    choice_gender = (
        ('male','男'),
        ('female','女'),
    )
    gender = models.CharField(max_length=6,choices=choice_gender,default='male',verbose_name='性别')
    mobile = models.IntegerField(null=True,verbose_name='手机号码')
    class Meta:
        verbose_name_plural = '用户列表'
    def __str__(self):
        return self.username

# 图书类别
class Category(models.Model):
    name = models.CharField(max_length=20,blank=True,verbose_name='图书类别')
    class Meta:
        verbose_name_plural = '图书类别'
    def __str__(self):
        return self.name

# 图书列表
class Book(models.Model):
    name = models.CharField(max_length=30,blank=False,verbose_name='书名')
    category = models.ForeignKey(Category,on_delete=models.CASCADE,default='',blank=False,related_name='books_category',verbose_name='类别')
    author = models.CharField(max_length=30,null=True,blank=False,verbose_name='作者')
    publisher = models.CharField(max_length=30,null=True,blank=False,verbose_name='出版社')
    count = models.IntegerField(default=1,verbose_name='库存')
    img = models.ImageField(upload_to='book_img/%Y/%m/%d/',blank=True,null=True,default='book_img/default.jpg',verbose_name='书籍图片')
    content = models.TextField(null=True,blank=True,verbose_name='内容简介')
    create_time = models.DateTimeField(auto_now_add=True,verbose_name='入库时间')
    class Meta:
        verbose_name_plural = '图书列表'
    def __str__(self):
        return self.name

# 订单表
class Order(models.Model):
    choice_status = (
        (1,'预定中'),
        (2,'已借阅'),
        (3,'归还中'),
        (4,'已归还'),
        (5,'已取消'),
    )
    m_time = models.DateTimeField(auto_now=True,verbose_name='更新时间')
    username = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='log_username',verbose_name='用户')
    book = models.ForeignKey(Book,on_delete=models.CASCADE,related_name='log_book',verbose_name='书名')
    status = models.SmallIntegerField(choices=choice_status,verbose_name='状态')
    class Meta:
        verbose_name_plural = '借阅订单'

    def audit(self):
        if self.status == 1:
            return format_html(
                '<button type="button" class="el-button el-button--primary el-button--small"> \
                <a href="/book/borrow_out/{}/"><span style="color:#FFF">借出</span></a></button>',self.id
            )
        elif self.status == 3:
            return format_html(
                '<button type="button" class="el-button stop-submit el-button--danger el-button--small"> \
                <a href="/book/return_in/{}/"><span style="color:#FFF">归还</span></a></button>',self.id
            )
    audit.short_description = '审核'


