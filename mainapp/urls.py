from django.urls import path
from mainapp.views import delete_user, update_user, user_list3, add_user, find_fruit, find_store, all_store, \
    count_fruit, count_order, user_list4

urlpatterns = [
    path('list', user_list4),
    path('add', add_user),
    path('update', update_user),
    path('del', delete_user),
    path('find', find_fruit),
    path('store', find_store),
    path('store_all', all_store),
    path('count', count_fruit),
    path('count_order', count_order),
]
