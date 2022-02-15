import os
import random
from datetime import datetime

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.db.models import Count, Sum, Min, Max, Avg, F, Q

# Create your views here.
from django.template import loader

from hidjangoProject import settings
from mainapp.models import User, Fruit, Store
from orderapp.models import Order


def user_list(request):
    datas = [
        {'id': 101, 'name': 'sl1'},
        {'id': 102, 'name': 'zh1'},
        {'id': 103, 'name': 'wj1'},
    ]
    return render(request,
                  'user/list.html',
                  {
                      'users': datas,
                      'msg': '最优秀的同学'
                  })


def user_list2(request):
    users = [
        {'id': 101, 'name': 'sl1'},
        {'id': 102, 'name': 'zh1'},
        {'id': 103, 'name': 'wj1'},
    ]
    msg = '最优秀的同学'
    return render(request,
                  'list.html',
                  locals())


def user_list3(request):
    users = User.objects.all()
    msg = '最优秀的同学'
    return render(request,
                  'user/list.html',
                  locals())


def user_list4(request):
    users = User.objects.all()
    msg = '最优秀的同学'
    error_index = random.randint(0, users.count() - 1)
    vip = {
        'name': 'shi',
        'money': 20000
    }
    info = '<h3>user info</h3>'
    now = datetime.now()

    file_dir = os.path.join(settings.BASE_DIR, 'mainapp/')
    files = {file_name: os.stat(file_dir + file_name)
             for file_name in os.listdir(file_dir)
             if os.path.isfile(file_dir + file_name)}

    price = 19.1356

    img_html = "<img width=100 height=100 src='/media/store/default.jpg'/>"
    # # 加载模板
    # template = loader.get_template('user/list_order.html')
    #
    # # 渲染模板
    # html = template.render(context={
    #     'msg': msg,
    #     'users': users
    # })
    html = loader.render_to_string('user/list.html', locals(), request)

    return HttpResponse(html, status=200)


def add_user(request):
    # 获取请求参数
    name = request.GET.get('name', None)
    age = request.GET.get('age', 0)
    phone = request.GET.get('phone', None)
    if not all((name, age, phone)):
        return HttpResponse('<h3 style="color:red">请求参数不完整</h3>', status=400)

    u1 = User()
    u1.name = name
    u1.age = age
    u1.phone = phone
    u1.save()
    return redirect('/user/list')


def update_user(request):
    id = request.GET.get('id', None)
    if not id:
        return HttpResponse('id must be exist', status=400)
    try:
        # 查看数据库中是否存在此ID
        user = User.objects.get(pk=int(id))
        name = request.GET.get('name', None)
        phone = request.GET.get('phone', None)
        if any((name, phone)):  # name,phone任意一个存在
            if name:
                user.name = name
            if phone:
                user.phone = phone
            user.save()
            return redirect('/user/list')
    except:
        return HttpResponse('%s 的用户不存在' % id, status=404)


def delete_user(request):
    id = request.GET.get('id', None)
    if id:
        try:
            user = User.objects.get(pk=id)
            user.delete()
            html = """
            <p>
            %s 删除成功！ 三秒后自动跳转到<a href="/user/list">列表</a>
            </p>
            <script>
                setTimeout(function(){
                    open('/user/list', target='_self');
                }, 3000)
            </script>
            """ % id
            return HttpResponse(html)
        except:
            return HttpResponse('%s 用户不存在' % id)
    else:
        return HttpResponse('必须提供ID参数')


def find_fruit(request):
    p1 = request.GET.get('p1', 0)
    p2 = request.GET.get('p2', 100)

    fruits = Fruit.objects.filter(price__gte=p1, price__lte=p2) \
        .exclude(price=250) \
        .filter(name__contains='果') \
        .filter(price__in=(0, 5)) \
        .all()
    return render(request, 'fruit/list.html', locals())


def find_store(request):
    # 查询2022年开业的水果店
    queryset = Store.objects.filter(create_time__month__lt=6).order_by('-id', 'city')
    first = queryset.first()
    stores = queryset.all()
    return render(request, 'store/list.html', locals())


def all_store(request):
    # 返回所有水果店的json数据
    result = {}
    if Store.objects.exists():
        data = Store.objects.values()
        print(type(data))  # QuerySet<{},{},{}>可迭代对象，里面的每一条数据都是一个字典对象
        total = Store.objects.count()
        store_list = []
        for store in data:
            store_list.append(store)

        result['data'] = store_list
        result['total'] = total
    else:
        result['msg'] = 'data is empty'

    return JsonResponse(result)


def count_fruit(request):
    # 统计每种分类的水果数量。。。
    result = Fruit.objects.aggregate(cnt=Count('name'),
                                     max=Max('price'),
                                     min=Min('price'),
                                     avg=Avg('price'),
                                     total=Sum('price'))

    # 中秋节：全场水果打8.8折，
    # F()函数作用是获取字段的值进行运算作为更新条件
    # round()函数作用四舍五入
    # Fruit.objects.update(price=F('price')*0.88)
    # 返回QuerySet<{},{},{}>可迭代对象，每一项数据都是一个dict
    fruits = Fruit.objects.values()

    # 查询价格低于10，或者高于100，或原产地是西藏且名字中包含“果”的水果
    fruits2 = Fruit.objects.filter(
        Q(price__gte=100) | Q(price__lte=10) | Q(Q(source='西藏') & Q(name__contains="果"))).values()

    # 使用原生SQL查询，包括raw()函数和extra()函数两种方式
    # fruits3 = Fruit.objects.raw('select id, name, price from t_fruit where price < %s order by price DESC LIMIT %s, 10', (10, 0))
    # fruits4 = Fruit.objects.raw('select id, name, price from t_fruit where price < %(price)s order by price DESC LIMIT %(page)s, 10', {'price':10,'page':0})
    # fruits5 = Fruit.objects.extra(where=['price<%s or name like %s', 'source=%s'], params=['10', '果', '天津'])

    # 使用django.db.connection数据库连接对象进行原生SQL查询
    # curor = connection.cursor()
    # curor.excute('select * from t_fruit')
    # for row in curor.fetchall():
    # print(row)
    # curor.rowcount, 统计影响行数
    # connection.commit()
    return JsonResponse({
        'count': result,
        # QuerySet<{},{},{}>可迭代对象，里面的每一条数据都是一个字典对象
        'fruits': [fruit for fruit in fruits],
        'fruits2': [fruit for fruit in fruits2],
        # 'fruits4': [fruit for fruit in fruits4],
        # 'fruits3': [fruit for fruit in fruits3],
        # 'fruits5': [fruit for fruit in fruits5]
    })


def count_order(request):
    total = Order.objects.filter(create_time__year=2022).aggregate(total=Sum('price'))

    return JsonResponse(total)
