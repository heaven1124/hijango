from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
# Create your views here.
from django.urls import reverse


def order_list(request, order_num, city_code):
    print(order_num, city_code)
    return render(request, 'list_order.html', locals())


def cancel_order(request, order_num):
    # order_num订单编号是UUID类型
    return render(request, 'list_order.html', locals())


def search(request, phone):
    return HttpResponse('hi, phone: %s' % phone)


def query(request):
    # 查询参数code（1：按城市和订单号num查询，2：按手机号phone查询）
    # url = reverse('order:list', args=('tj', 1009))
    url = reverse('order:list', kwargs=dict(city_code='tj', order_num=1002))
    # return redirect(url)
    print(type(request.GET), request.GET)
    return HttpResponseRedirect(url)

    # url = reverse('order:search', args=('13655623245',))
    # return HttpResponse('hi, query %s' % url)