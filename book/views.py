from asyncio.proactor_events import _ProactorBaseWritePipeTransport
from threading import local
from django.shortcuts import render
from django.contrib import auth
#from django.contrib.auth.models import User
from .models import *
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.utils import timezone
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required
def index(request):
	return HttpResponseRedirect('/book/list/')


@csrf_exempt
def register(request):
	errors = []
	account = None
	password = None
	password2 = None
	email = None
	CompareFlag = False
	if request.method == 'POST':
		if not request.POST.get('account'):
			errors.append('用户名不能为空')
		else:
			account = request.POST.get('account')
		if not request.POST.get('password'):
			errors.append('密码不能为空')
		else:
			password = request.POST.get('password')
		if not request.POST.get('password2'):
			errors.append('确认密码不能为空')
		else:
			password2 = request.POST.get('password2')
		if not request.POST.get('email'):
			errors.append('邮箱不能为空')
		else:
			email = request.POST.get('email')
		if not request.POST.get('mobile'):
			errors.append('手机号码不能为空')
		else:
			mobile = request.POST.get('mobile')
		if password is not None:
			if password == password2:
				CompareFlag = True
			else:
				errors.append('两次输入密码不一致')
		if account is not None and password is not None and password2 is not None and email is not None and mobile is not None and CompareFlag :
			user = User.objects.create_user(account,email,password)
			user.save()
			userlogin = auth.authenticate(username = account,password = password,mobile=mobile)
			auth.login(request,userlogin)
			return HttpResponseRedirect('/')
	return render(request,'book/register.html', {'errors': errors})


@csrf_exempt
def login(request):
	errors =[]
	account = None
	password = None
	if request.method == "POST":
		if not request.POST.get('account'):
			errors.append('用户名或密码不能为空')
		else:
			account = request.POST.get('account')
		if not request.POST.get('password'):
			errors = request.POST.get('密码不能为空')
		else:
			password = request.POST.get('password')
		if account is not None and password is not None:
			user = auth.authenticate(username=account,password=password)
			if user is not None:
				if user.is_active:
					auth.login(request,user)
					return HttpResponseRedirect('/')
				else:
					errors.append('用户名错误')
			else:
				errors.append('用户名或密码错误')
	return render(request,'book/login.html', {'errors': errors})


def logout(request):
	auth.logout(request)
	return HttpResponseRedirect('/login/')


@login_required
def book_list(request):
	list = Book.objects.all()
	paginator = Paginator(list,2)
	page = request.GET.get('page')
	try:
		list = paginator.page(page)
	except PageNotAnInteger:
		list = paginator.page(1)
	except EmptyPage:
		list = paginator.page(paginator.num_pages)
	return render(request,'book/list.html',locals())


@login_required
def book_detail(request,sid):
	if request.method == 'GET':
		obj_book = Book.objects.filter(id=sid)
		return render(request,'book/detail.html',locals())


@login_required
def book_borrow(request,bid):
	# 需要增加原子性操作
	obj_book = Book.objects.filter(id=bid).first()
	obj_book.count = obj_book.count -1
	obj_book.save()

	user_id = User.objects.filter(username=request.user).first().id
	obj_record = Record(username_id=user_id,book_id=bid,status=1)
	obj_record.save()
	return HttpResponseRedirect('/book/list/')


@login_required
def book_return(request):
	pass


@login_required
def book_myborrow(request):
	pass


@login_required
def book_borrowrecord(request):
	pass


@login_required
def user_center(request):
	pass

