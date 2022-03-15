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
	else:
		form = RegisterModelForm()
	return render(request,"book/register.html",{'form':form})


def login(request):
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


@login_required
def detail(request,bid):
	if request.method == 'GET':
		obj_book = Book.objects.filter(id=bid)
		obj_order = Order.objects.filter(username=request.user,book_id=bid,status__lt=4).first()
		return render(request,'book/detail.html',locals())


def borrow(request,bid):
	obj_book = Book.objects.filter(id=bid).first()
	user_id = UserProfile.objects.filter(username=request.user).first().id
	with transaction.atomic():
		obj_book.count = obj_book.count - 1
		obj_order = Order(username_id=user_id,book_id=bid,status=1)
			
		obj_book.save()
		obj_order.save()
		return HttpResponseRedirect(reverse('book_list'))


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


@login_required
def returning(request,oid):
	#obj_order1 = Order.objects.filter(id=rid).first()
	bid = Order.objects.filter(id=oid).first().book_id
	obj_book = Book.objects.filter(id=bid).first()
	#bid = obj_order1.book_id
	obj_order = Order.objects.get(username=request.user,id=oid)
	with transaction.atomic():
		obj_book.count = obj_book.count + 1
		obj_order.status = 3
		obj_book.save()
		obj_order.save()
	return HttpResponseRedirect('/book/myborrow/')


@login_required
def record(request):
	obj_order = Order.objects.filter(username=request.user,status=4).order_by('-m_time')
	paginator = Paginator(obj_order,10)
	page = request.GET.get('page')
	try:
		obj_order = paginator.page(page)
	except PageNotAnInteger:
		obj_order = paginator.page(1)
	except EmptyPage:
		obj_order = paginator.page(paginator.num_pages)
	return render(request,'book/record.html',locals())


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
