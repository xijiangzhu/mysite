from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.conf import settings

# 用户信息
class User(AbstractUser):
    choice_gender = (
        ('male','男'),
        ('female','女'),
    )
    gender = models.CharField(max_length=6,choices=choice_gender,default='male',verbose_name='性别')
    mobile = models.IntegerField(null=True,blank=False,verbose_name='手机号')
    class Meta:
        verbose_name_plural = '用户'
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
    #choice_status = ((0,'正常'),(1,'预定中'),(2,'已借阅'),(3,'归还中'),)
    name = models.CharField(max_length=30,blank=False,verbose_name='书名')
    category = models.ForeignKey(Category,on_delete=models.CASCADE,default='',blank=False,related_name='books_category',verbose_name='类别')
    author = models.CharField(max_length=30,null=True,blank=False,verbose_name='作者')
    publisher = models.CharField(max_length=30,null=True,blank=False,verbose_name='出版社')
    count = models.IntegerField(default=1,verbose_name='库存')
    img = models.ImageField(upload_to='book_img/%Y/%m/%d/',blank=True,null=True,default='book_img/default.jpg',verbose_name='书籍图片')
    content = models.TextField(null=True,blank=True,verbose_name='内容简介')
    create_time = models.DateTimeField(auto_now_add=True,verbose_name='入库时间')
    #status = models.SmallIntegerField(choices=choice_status,default=0,verbose_name='书籍状态')
    #borrower = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,null=True,blank=True,related_name='books_borrower',verbose_name='借阅人')
    #borrow_time = models.DateTimeField(null=True,blank=True,verbose_name='借阅时间')
    class Meta:
        verbose_name_plural = '图书列表'
    def __str__(self):
        return self.name

# 日志
class Record(models.Model):
    choice_status = (
        (1,'预定中'),
        (2,'已借阅'),
        (3,'归还中'),
        (4,'已归还'),
    )
    m_time = models.DateTimeField(auto_now=True,verbose_name='更新时间')
    username = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='log_username',verbose_name='用户')
    book = models.ForeignKey(Book,on_delete=models.CASCADE,related_name='log_book',verbose_name='书名')
    status = models.SmallIntegerField(choices=choice_status,verbose_name='状态')
    class Meta:
        verbose_name_plural = '借阅记录'

