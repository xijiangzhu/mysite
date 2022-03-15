from django import forms
from .models import *
from django.contrib.auth.forms import UserChangeForm
from captcha.fields import CaptchaField

class RegisterModelForm(forms.ModelForm):
    email = forms.EmailField(min_length=4,max_length=50,widget=forms.EmailInput,label='邮箱')
    password = forms.CharField(min_length=8,max_length=20,widget=forms.widgets.PasswordInput(),label='密码',)
    confirm_password = forms.CharField(widget=forms.widgets.PasswordInput(),label='确认密码')
    #captcha = CaptchaField(label='验证码',required=True,error_messages={'required': '验证码不能为空'})
    class Meta:
        model = UserProfile
        fields = ['username','password','confirm_password','email','mobile','gender',]
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class':'form-control'})   
    def clean_username(self):
        username = self.cleaned_data.get("username")
        user_obj = UserProfile.objects.filter(username=username).first()
        if user_obj:
            raise forms.ValidationError("该用户已经存在！")
        else:
            return username
    def clean_email(self):
        email = self.cleaned_data.get("email")
        user_obj = UserProfile.objects.filter(email=email).first()
        if user_obj:
            raise forms.ValidationError("该邮箱已经存在！")
        else:
            return email
    def clean_mobile(self):
        mobile = self.cleaned_data.get("mobile")
        if mobile is None:
            raise forms.ValidationError("手机号码不能为空！")
        user_obj = UserProfile.objects.filter(mobile=mobile).first()
        if user_obj:
            raise forms.ValidationError("该手机号码已经存在！")
        else:
            return mobile
    def clean_password(self):
        password = self.cleaned_data.get("password")
        if password.isdigit():
            raise forms.ValidationError("密码不能是纯数字！")
        else:
            return password
    def clean_confirm_password(self):
        password = self.cleaned_data.get("password")
        confirm_password = self.cleaned_data.get("confirm_password")
        if password != confirm_password:
            self.add_error("confirm_password",forms.ValidationError("两次密码输入不一致！"))
        else:
            return self.cleaned_data


class LoginModelForm(forms.ModelForm):
    password = forms.CharField(widget=forms.widgets.PasswordInput(),label='密码',)
    #captcha = CaptchaField(label='验证码',required=True,error_messages={'required': '验证码不能为空'})
    class Meta:
        model = UserProfile
        fields = ['username','password',]
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class':'form-control'})
    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = auth.authenticate(username=username,password=password)
        if user is None:
            self.add_error('password','用户或密码错误！')
        else:
            return self.cleaned_data


class UserEdit(UserChangeForm):
    password = forms.CharField(label='密码',required=False)
    last_login = forms.DateTimeField(label='最近登录',disabled=True)
    date_joined = forms.DateTimeField(label='注册日期',disabled=True)
    
    class Meta:
        model = UserProfile
        fields = ('username', 'email', 'mobile', 'password','gender','last_login','date_joined')
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class':'form-control'})