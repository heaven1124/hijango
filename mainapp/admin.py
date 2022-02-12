from django.contrib import admin
from mainapp.models import User, CateType, Fruit, Store, RealProfile, FruitCart, Tag


class UserAdmin(admin.ModelAdmin):
    # 列表中显示的字段
    list_display = ('id', 'name', 'phone')
    # 每页显示记录数
    list_per_page = 2
    # 过滤器（一般配置分类字段）
    list_filter = ('id', 'phone')
    # 搜索字段
    search_fields = ('id', 'phone')


class CateTypeAdmin(admin.ModelAdmin):
    # 列表中显示的字段
    list_display = ('id', 'name', 'order_num')
    # 每页显示记录数
    list_per_page = 2
    # 过滤器（一般配置分类字段）
    list_filter = ('id', 'name')
    # 搜索字段
    search_fields = ('id', 'name')


class FruitAdmin(admin.ModelAdmin):
    # 列表中显示的字段
    list_display = ('id', 'name', 'source', 'price', 'category')
    # 每页显示记录数
    list_per_page = 2
    # 过滤器（一般配置分类字段）
    list_filter = ('price', 'name')
    # 搜索字段
    search_fields = ('price', 'name')


class StoreAdmin(admin.ModelAdmin):
    # 列表中显示的字段
    list_display = ('id_', 'name', 'city', 'address', 'store_type', 'logo')
    # 指定表单可以修改的字段
    fields = ('name', 'city', 'address', 'store_type', 'logo', 'summary')


class RealProfileAdmin(admin.ModelAdmin):
    # 列表中显示的字段
    list_display = ('user', 'real_name', 'number', 'certificate_type')


class FruitCartAdmin(admin.ModelAdmin):
    list_display = ('cart', 'fruit', 'unit_price', 'cnt', 'price')

    def unit_price(self,obj):
        return obj.unit_price

    def price(self,obj):
        return obj.price

    unit_price.shot_description = '单价'
    price.shot_description = '小计'


class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'order_num')
    fields = ('name', 'order_num')


# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(CateType, CateTypeAdmin)
admin.site.register(Fruit, FruitAdmin)
admin.site.register(Store, StoreAdmin)
admin.site.register(RealProfile, RealProfileAdmin)
admin.site.register(FruitCart, FruitCartAdmin)
admin.site.register(Tag, TagAdmin)
