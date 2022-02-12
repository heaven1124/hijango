from django.db import models
from django.db.models import Q


class BaseModel(models.Model):
    create_time = models.DateTimeField(verbose_name='创建时间',
                                       auto_now_add=True)
    last_time = models.DateTimeField(verbose_name='更新时间',
                                     auto_now=True)

    class Meta:
        # 抽象模型类，不会创建对应的数据库表
        abstract = True


# 为了过滤掉已取消状态的数据，自定义Queryset或Manager
class OrderManager(models.Manager):
    # 获取查询结果集对象（Queryset）
    def get_queryset(self):
        return super().get_queryset().filter(~Q(pay_status=5))


# Create your models here.
class Order(BaseModel):
    num = models.CharField(max_length=20,
                           primary_key=True,
                           verbose_name='订单号')
    title = models.CharField(max_length=100,
                             verbose_name='订单名称')
    price = models.DecimalField(max_digits=10,
                                decimal_places=2,
                                verbose_name='订单金额')
    pay_type = models.IntegerField(choices=((0, '余额'),
                                            (1, '银行卡'),
                                            (2, '微信'),
                                            (3, '支付宝')),
                                   verbose_name='支付方式',
                                   default=0)
    pay_status = models.IntegerField(choices=((0, '待支付'),
                                              (1, '已支付'),
                                              (2, '待收货'),
                                              (3, '已收货'),
                                              (4, '已完成'),
                                              (5, '已取消')),
                                     verbose_name='订单状态',
                                     default=0)
    receiver = models.CharField(verbose_name='收货人',
                                max_length=20)
    receiver_phone = models.CharField(verbose_name='收货人电话',
                                      max_length=11)
    receiver_address = models.TextField(verbose_name='收货地址')

    # 为了过滤掉已取消状态的数据，显示创建objects
    objects = OrderManager()

    def __str__(self):
        return self.title

    class Meta:
        db_table = 't_order'
        verbose_name = verbose_name_plural = '订单表'


class Cart(BaseModel):
    from mainapp.models import User
    user = models.OneToOneField(User,
                                verbose_name='账号',
                                on_delete=models.CASCADE)
    no = models.CharField(max_length=10,
                          primary_key=True,
                          verbose_name='购物车编号')

    def __str__(self):
        return self.no

    class Meta:
        db_table = 't_cart'
        verbose_name = verbose_name_plural = '购物车表'



