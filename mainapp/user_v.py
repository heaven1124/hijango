from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import check_password
from django.views.decorators.csrf import csrf_exempt

from mainapp.models import User


# 在此方法中CsrfViewMiddleware中间件失效，即取消Csrf验证
@csrf_exempt
def login(request: HttpRequest):
    if request.method == 'POST':
        name = request.POST.get('name')
        password = request.POST.get('password')
        if not all((name, password)):
            error_msg = '用户名或口令不能为空'
        else:
            qs = User.objects.filter(name=name)
            if qs.exists():
                login_user: User = qs.first()
                if check_password(password, login_user.password):
                    # 登陆成功 将登陆用户信息写入session中
                    request.session['login_user'] = {
                        'name': login_user.name,
                        'user_id': login_user.id,
                        'phone': login_user.phone
                    }
                    return redirect('/user/list')
                else:
                    error_msg = '口令错误'
            else:
                error_msg = '用户未注册，<a href="/user/regist">去注册</a>'

    return render(request, 'user/login.html', locals())