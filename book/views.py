from django.shortcuts import redirect, render
from django.contrib import auth
#from django.contrib.auth.models import User
from .models import *

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.contrib import sessions
from .myforms import *


@login_required
def index(request):
	return HttpResponseRedirect('/book/list/')


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
		return render(request,"book/register.html",{'form':form})
	else:
		form = RegisterModelForm()
		return render(request,"book/register.html",{'form':form})


def login(request):
	# 已登录的用户访问登录页面，跳转到主页
	if request.user.is_authenticated:
		return HttpResponseRedirect('/')
	else:
		if request.method == 'POST':
			form = LoginModelForm(request.POST)
			if form.is_valid():
				username = form.cleaned_data.get('username')
				password = form.cleaned_data.get('password')
				user = auth.authenticate(username=username,password=password)
				if user:
					auth.login(request,user)
					return HttpResponseRedirect('/')
			return render(request,'book/login.html', {'form': form})
		else:
			form = LoginModelForm()
			return render(request,'book/login.html', {'form': form})


def logout(request):
	auth.logout(request)
	return HttpResponseRedirect('/login/')


@login_required
def book_list(request):
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


@login_required
def book_detail(request,bid):
	if request.method == 'GET':
		obj_book = Book.objects.filter(id=bid)
		return render(request,'book/detail.html',locals())


@login_required
def book_borrow(request,bid):
	# 需要增加原子性操作
	obj_book = Book.objects.filter(id=bid).first()
	obj_book.count = obj_book.count - 1
	obj_book.save()
	user_id = User.objects.filter(username=request.user).first().id
	obj_record = Record(username_id=user_id,book_id=bid,status=1)
	obj_record.save()
	return HttpResponseRedirect('/book/list/')


@login_required
def book_myborrow(request):
	obj_record = Record.objects.filter(username=request.user,status__lt=4)
	paginator = Paginator(obj_record,10)
	page = request.GET.get('page')
	try:
		obj_record = paginator.page(page)
	except PageNotAnInteger:
		obj_record = paginator.page(1)
	except EmptyPage:
		obj_record = paginator.page(paginator.num_pages)
	return render(request,'book/myborrow.html',locals())


@login_required
def book_return(request,rid):
	# 需要增加原子性操作
	obj_record1 = Record.objects.filter(id=rid).first()
	bid = obj_record1.book_id
	obj_book = Book.objects.filter(id=bid).first()
	obj_book.count = obj_book.count + 1
	obj_book.save()

	obj_record = Record.objects.get(username=request.user,id=rid)
	obj_record.status = 3
	obj_record.save()
	return HttpResponseRedirect('/book/myborrow/')



@login_required
def book_borrowrecord(request):
	obj_record = Record.objects.filter(username=request.user,status=4)
	paginator = Paginator(obj_record,10)
	page = request.GET.get('page')
	try:
		obj_record = paginator.page(page)
	except PageNotAnInteger:
		obj_record = paginator.page(1)
	except EmptyPage:
		obj_record = paginator.page(paginator.num_pages)
	return render(request,'book/borrowrecord.html',locals())


@login_required
def book_usercenter(request):
	pass


@login_required
def search(request):
	pass