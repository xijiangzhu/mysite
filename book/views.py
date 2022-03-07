from django.shortcuts import render
from django.contrib import auth
#from django.contrib.auth.models import User
from .models import User
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.

# 首页
@csrf_exempt
def index(request):
		username = request.user
		return render(request,'book/index.html',locals())

# 用户注册
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
			return HttpResponseRedirect('/book/')
	return render(request,'book/register.html', {'errors': errors})

# 用户登录
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
					return HttpResponseRedirect('/book/')
				else:
					errors.append('用户名错误')
			else:
				errors.append('用户名或密码错误')
	return render(request,'book/login.html', {'errors': errors})

# 用户注销
def logout(request):
	auth.logout(request)
	return HttpResponseRedirect('/book/')


