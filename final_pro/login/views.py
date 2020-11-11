
from django.shortcuts import render,redirect

import hashlib

from . import models
from .forms import UserForm, RegisterForm, UpdateForm
import datetime
from django.conf import settings
def login(request):
    if request.method == "POST":
        login_form = UserForm(request.POST)
        message = "请检查填写的内容！"
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            try:
                user = models.User.objects.get(name=username)
                if not user.has_confirmed:
                    message = "用户未通过邮件确认！"
                    return render(request, 'login/login.html', locals())
                if user.password == hash_code(password):
                    request.session['is_login'] = True
                    request.session['user_id'] = user.id 
                    request.session['user_name'] = user.name
                    request.session.set_expiry(0)
                    return redirect('/index/')
                else:
                    message = "密码不正确！"
            except:
                message = "用户不存在！"
        return render(request, 'login/login.html', locals())

    login_form = UserForm()
    return render(request, 'login/login.html', locals())


def make_confirm_string(user):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    code = hash_code(user.name, now)
    models.ConfirmString.objects.create(code=code, user=user,)
    return code

def send_email(email,code):
    from django.core.mail import EmailMultiAlternatives

    subject, from_email, to = '测试邮件', 'zt23571113@163.com',email
    text_content = '这里是HITSZ'
    html_content = '''
                    <p><a href = "http://{}/confirm/?code={}">确认链接</a></p>
                    <p>请点击以上链接完成注册确认</p>
                    <p>有效期为三天</p>
                    '''.format('127.0.0.1:8000',code)

    msg = EmailMultiAlternatives(subject,text_content,from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()
    print('done')
def register(request):
    if request.session.get('is_login', None):
        # 登录状态不允许注册。你可以修改这条原则！
        return redirect("/index/")
    if request.method == "POST":
        register_form = RegisterForm(request.POST)
        message = "请检查填写的内容！"
        if register_form.is_valid():  # 获取数据
            username = register_form.cleaned_data['username']
            password1 = register_form.cleaned_data['password1']
            password2 = register_form.cleaned_data['password2']
            email = register_form.cleaned_data['email']
            
            if password1 != password2:  # 判断两次密码是否相同
                message = "两次输入的密码不同！"
                return render(request, 'login/register.html', locals())
            else:
                same_name_user = models.User.objects.filter(name=username)
                if same_name_user:  # 用户名唯一
                    message = '用户已经存在，请重新选择用户名！'
                    return render(request, 'login/register.html', locals())
                same_email_user = models.User.objects.filter(email=email)
                if same_email_user:  # 邮箱地址唯一
                    message = '该邮箱地址已被注册，请使用别的邮箱！'
                    return render(request, 'login/register.html', locals())

                # 当一切都OK的情况下，创建新用户

                new_user = models.User.objects.create()
                new_user.name = username
                
                new_user.password = hash_code(password1)
                new_user.email = email
               
                new_user.save()

                code = make_confirm_string(new_user)
                send_email(email,code)

                message = "欢迎您的注册！请前往注册邮箱，进行邮件确认！"
                #return redirect('/login/')  # 自动跳转到登录页面
                return render(request, 'login/confirm.html', locals())
    register_form = RegisterForm()
    return render(request, 'login/register.html', locals())

def update_password(request):
    if request.method == 'POST':
        update_form = UpdateForm(request.POST)
        message = '请检查填写的内容！'
        if update_form.is_valid():  # 获取数据
            username = update_form.cleaned_data['username']
            new_password = update_form.cleaned_data['new_password']
            re_password = update_form.cleaned_data['re_password']
            email = update_form.cleaned_data['email']
            if new_password != re_password:
                message = '两次输入的密码不同！'
            user = models.User.objects.filter(name = username)
            if user is None:
                message = '用户不存在！'
                return render(request, 'update/update_password.html', locals())
            eml = models.User.objects.get(name = username , email = email)
            
           
            print(eml.id)
            #eml_object = model_to_dict(eml)
            if eml is None:
                message = '邮箱输入错误！'
                return render(request, 'update/update_password.html', locals())
            hash_new_password = hash_code(new_password)
            models.User.objects.filter(name = username , email = email).delete()
            new_user = models.User.objects.create(id = eml.id)
            new_user.name = username

            new_user.email =email
            new_user.password = hash_code(new_password)

            new_user.save()
            print(new_user.id)
            code = make_confirm_string(new_user)

            send_update_password_email(email, code)
            message = '您已修改密码，请尽快进入邮箱确认！'
            return render(request, 'update/confirm_password.html',locals())
        '''user = authenticate(username=request.user.email, password=old_password)
        if user is None:
            message = '请检查旧密码输入，并重新输入'
            return render(request, 'update/update_password.html',locals())
        if re_password != new_password:
            message = '两次输入的密码不同！'   
            return render(request, 'update/update_password.html', locals())
        request.user.userinfo.has_confirmed = False
        request.user.userinfo.save()
        request.user.set_password(new_password)
        request.user.save()
        code = make_confirm_string(new_password)
        send_update_password_email(request.user.email, code)
        message = '已经向您注册的邮箱发送修改密码请求，请前往确认'''
    update_form = UpdateForm()
    return render(request, 'update/update_password.html',locals())

def send_update_password_email(email, code):
    from django.core.mail import EmailMultiAlternatives
    subject, from_email, to = '测试邮件', 'zt23571113@163.com',email
    web_name = 'xxx'
    web_url = '127.0.0.1:8000'
    subject = '来自www.{}.com的修改密码确认邮件'.format(web_name)
    text_content = '''欢迎使用www.{}.com,这里是{}大数据平台（若您看到这条
                    信息，说明您的邮箱服务器不提供HTML链接功能，请联系管理员'''.format(web_name,web_name)

    html_content = '''
                    <style type="text/css">
                    a:hover{{ color:red;}}
                    p:hover{{ color:blue }}
                    </style>
                    <p> 感谢使用<a href="http://{}/confirm_update_password/?code={}">xxx</a>
                    <p> 请点击站点链接完成修改请求！</p>
                    <p> 如果不是您发送的修改请求，请即刻向我们反馈</p>
                    <p> 此链接有效期为{}天！ </p>
                    '''.format(web_url,code,settings.CONFIRM_DAYS)
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content,"text/html")
    msg.send()
    print('done_confirm')


def logout(request):
    if not request.session.get('is_login', None):
        # 如果本来就未登录，也就没有登出一说
        return redirect("/index/")
    request.session.flush()
    return redirect("/index/")

def user_confirm(request):
    import pytz
    code = request.GET.get('code',None)
    message = ''
    try:
        confirm = models.ConfirmString.objects.get(code=code)
    except:
        message = '无效的确认请求'
        return render(request, 'login/confirm.html', locals())

    c_time = confirm.c_time
    now = datetime.datetime.now()
    now=now.replace(tzinfo=pytz.timezone('UTC'))
    if now > c_time + datetime.timedelta(settings.CONFIRM_DAYS):
        confirm.user.delete()
        message = '您的邮件已过期！请您重新注册'
        return render(request, 'login/confirm.html', locals())
    else:
        confirm.user.has_confirmed = True
        confirm.user.save()
        confirm.delete()
        message = '感谢确认，欢迎您的访问'
        return render(request, 'login/confirm.html', locals())

def confirm_update_password(request):
    import pytz
    code = request.GET.get('code',None)
    message = ''
    try:
        confirm = models.ConfirmString.objects.get(code=code)
    except:
        message = '无效的确认请求'
        return render(request, 'update/confirm_password.html',locals())
    c_time = confirm.c_time
    now = datetime.datetime.now()
    now = now.replace(tzinfo=pytz.timezone('UTC'))
    if now > c_time + datetime.timedelta(settings.CONFIRM_DAYS):
        confirm
        message = '您的邮件已过期！请您重新注册'
        return render(request, 'update/confirm_update_password.html',locals())
    else:
        confirm.user.has_confirmed = True
        confirm.user.save()
        confirm.delete()
        logout(request)
        message =  '恭喜您修改密码成功，赶快尝试登陆吧！'
        return render(request, 'update/confirm_password.html',locals())

def hash_code(s, salt='mysite'):
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())
    return h.hexdigest()

def download(request):
    if request.method == "POST":
        #URL =request.POST.get('url')
        URL = 'county-level-data-sets_description'
        baseurl = 'http://10.250.168.225:50070/webhdfs/v1/input/data/county-level-data-sets/'
        url_tail ='.txt?op=OPEN'
        path = baseurl + URL + url_tail
        print(path)
        return redirect(path)




    
	