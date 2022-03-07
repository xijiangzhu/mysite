from django.shortcuts import render
from django.contrib import auth
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.

def index(request):
    pass
    return render(request,'book/index.html')

def login(request):
    pass
    return render(request,'book/login.html')

def register(request):
    pass
    return render(request,'book/register.html')

def book_list(request):
    pass
    return render(request,'book/book_list.html')

@csrf_exempt
def index(request):
		username = request.user
		return render(request,'login/index.html',locals())
# 用户注册
@csrf_exempt
def my_register(request):
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
		if password is not None:
			if password == password2:
				CompareFlag = True
			else:
				errors.append('两次输入密码不一致')
		if account is not None and password is not None and password2 is not None and email is not None and CompareFlag :
			user = User.objects.create_user(account,email,password)
			user.save()
			userlogin = auth.authenticate(username = account,password = password)
			auth.login(request,userlogin)
			return HttpResponseRedirect('/')
	return render(request,'login/register.html', {'errors': errors})

@csrf_exempt
def my_login(request):
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
	return render(request,'login/login.html', {'errors': errors})

def my_logout(request):
	auth.logout(request)
	return HttpResponseRedirect('/')