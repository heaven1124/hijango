
from django.urls import path, re_path

from orderapp import views

app_name = 'orderapp'
urlpatterns = [
    path('list/<city_code>/<order_num>', views.order_list, name='list'),
    # 兼容1.0老版本---不行 --- url(r'^list2$', views.order_list)
    path('cancel/<uuid:order_num>', views.cancel_order, name='cancel'),
    re_path(r'^search/(?P<phone>1[3-57-9][\d]{9})$', views.search, name='search'),
    path('query', views.query)

]