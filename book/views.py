from urllib.request import HTTPRedirectHandler
from django.shortcuts import redirect, render
from django.contrib import auth
#from django.contrib.auth.models import User

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .forms import *
from .models import *
from django.db import transaction

# 首页
@login_required
def index(request):
	return HttpResponseRedirect('/book/list/')

# 注册
def register(request):
	if request.method == "POST":
		form = RegisterModelForm(request.POST)
		if form.is_valid():
			# 密码加密
			user = form.save()
			user.set_password(user.password)
			user.save()
			# 注册成功后自动登录
			user = auth.authenticate(username=form.cleaned_data.get('username'), password=form.cleaned_data.get('password'))
			auth.login(request, user)
			return HttpResponseRedirect('/book/list/')
	else:
		form = RegisterModelForm()
	return render(request,"book/register.html",{'form':form})

# 登录
def login(request):
	if request.user.is_authenticated:
		return HttpResponseRedirect('/book/')
	else:
		if request.method == 'POST':
			form = LoginModelForm(request.POST)
			if form.is_valid():
				username = form.cleaned_data.get('username')
				password = form.cleaned_data.get('password')
				user = auth.authenticate(username=username,password=password)
				if user:
					auth.login(request,user)
					return HttpResponseRedirect('/book/list/')
			return render(request,'book/login.html', {'form': form})
		else:
			form = LoginModelForm()
			return render(request,'book/login.html', {'form': form})

# 注销
def logout(request):
	auth.logout(request)
	return HttpResponseRedirect('/book/login/')

# 图书列表
@login_required
def list(request):
	obj_book = Book.objects.all()
	paginator = Paginator(obj_book,10)
	page = request.GET.get('page')
	try:
		obj_book = paginator.page(page)
	except PageNotAnInteger:
		obj_book = paginator.page(1)
	except EmptyPage:
		obj_book = paginator.page(paginator.num_pages)
	return render(request,'book/list.html',locals())

# 图书详情页
@login_required
def detail(request,bid):
	if request.method == 'GET':
		obj_book = Book.objects.filter(id=bid)
		obj_order = Order.objects.filter(username=request.user,book_id=bid,status__lt=4).first()
		return render(request,'book/detail.html',locals())

# 借阅
def borrow(request,bid):
	obj_book = Book.objects.filter(id=bid).first()
	user_id = UserProfile.objects.filter(username=request.user).first().id
	with transaction.atomic():
		obj_book.count = obj_book.count - 1
		obj_order = Order(username_id=user_id,book_id=bid,status=1)	
		obj_book.save()
		obj_order.save()
		return redirect('book_detail',bid=obj_book.id)

# 取消预定
def cancel_reserve(request,oid):
	book_id = Order.objects.filter(id=oid).first().book_id
	obj_book = Book.objects.filter(id=book_id).first()
	obj_order = Order.objects.filter(id=oid).first()
	with transaction.atomic():
		obj_book.count = obj_book.count + 1
		obj_order.status = 5
		obj_book.save()
		obj_order.save()
		return redirect('book_myborrow')

# 我的借阅
@login_required
def myborrow(request):
	obj_order = Order.objects.filter(username=request.user,status__lt=4).order_by('-m_time')
	paginator = Paginator(obj_order,10)
	page = request.GET.get('page')
	try:
		obj_order = paginator.page(page)
	except PageNotAnInteger:
		obj_order = paginator.page(1)
	except EmptyPage:
		obj_order = paginator.page(paginator.num_pages)
	return render(request,'book/myborrow.html',locals())

# 归还
@login_required
def returning(request,oid):
	obj_order = Order.objects.get(username=request.user,id=oid)
	with transaction.atomic():
		obj_order.status = 3
		obj_order.save()
		return HttpResponseRedirect('/book/myborrow/')

# 取消归还
def cancel_return(request,oid):
	obj_order = Order.objects.get(username=request.user,id=oid)
	with transaction.atomic():
		obj_order.status = 2
		obj_order.save()
		return HttpResponseRedirect('/book/myborrow/')

# 借阅记录
@login_required
def record(request):
	obj_order = Order.objects.filter(username=request.user,status__gte=4).order_by('-m_time')
	paginator = Paginator(obj_order,10)
	page = request.GET.get('page')
	try:
		obj_order = paginator.page(page)
	except PageNotAnInteger:
		obj_order = paginator.page(1)
	except EmptyPage:
		obj_order = paginator.page(paginator.num_pages)
	return render(request,'book/record.html',locals())

# 个人中心
@login_required
def usercenter(request, slug=None):
	username = request.user
	form = UserEdit(instance=username)
	password_old = UserProfile.objects.get(username=username).password
	if request.method == 'POST':
		form = UserEdit(request.POST, instance=username)
		if form.is_valid():
			password_new = request.POST.get('password')
			user = form.save()
			if password_new != password_old:
				# 密码加密
				user.set_password(user.password)
			user.save()
			return HttpResponseRedirect('/book/usercenter/')	
	return render(request, 'book/usercenter.html', {'form':form})

# 图书搜索
@login_required
def search(request):
	search = request.GET.get('search')
	obj_book = Book.objects.filter(name__icontains=search)
	paginator = Paginator(obj_book,10)
	page = request.GET.get('page')
	try:
		obj_book = paginator.page(page)
	except PageNotAnInteger:
		obj_book = paginator.page(1)
	except EmptyPage:
		obj_book = paginator.page(paginator.num_pages)
	return render(request,'book/list.html',locals())

# 后台审核：借出
def borrow_out(request,oid):
	obj_order = Order.objects.filter(id=oid).first()
	with transaction.atomic():
		obj_order.status = 2
		obj_order.save()
		return HttpResponse('已借出!')

# 后台审核：归还
def return_in(request,oid):
	bid = Order.objects.filter(id=oid).first().book_id
	obj_book = Book.objects.filter(id=bid).first()
	obj_order = Order.objects.get(id=oid)
	with transaction.atomic():
		obj_book.count = obj_book.count + 1
		obj_order.status = 4
		obj_book.save()
		obj_order.save()
		return HttpResponse('归还成功！')
