import re
import uuid

from django.contrib.auth.hashers import make_password
from django.db import models
from django.core.exceptions import ValidationError
# Create your models here.


# 自定义Manager类，用来创建objects对象
class UserManager(models.Manager):
    def update(self, **kwargs):
        password = kwargs.get('password', None)
        if password and len(password) < 50:
            kwargs['password'] = make_password(password)
        super(UserManager, self).update(**kwargs)


# 验证类，验证模型字段是否符合要求
class UserValidator:
    @classmethod
    def valid_phone(self, value):
        if not re.match(r'1[1-57-9]\d{9}', value):
            raise ValidationError('phone format is not correct')
        return True


class User(models.Model):
    # 默认情况下会自动创建id主键
    name = models.CharField(max_length=20,
                            verbose_name='账号') # 后台管理显示的名称
    age = models.IntegerField(default=0, verbose_name='年龄')
    phone = models.CharField(max_length=11,
                             verbose_name='手机号',
                             # 指定验证类，和验证方法
                             validators=[UserValidator.valid_phone],
                             blank=True, # 后台管理界面添加字段可以为空
                             null=True)  # 数据库的字段可以是null
    password = models.CharField(max_length=100,
                                verbose_name='口令',
                                blank=True,  # 后台管理界面添加字段可以为空
                                null=True)
    objects = UserManager()

    # 重写save方法，密码加密
    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        # 密码长度小于50，未加密
        if len(self.password) < 50:
            # 明文转密文
            self.password = make_password(self.password)

        super().save()

    def __str__(self):
        return self.name

    class Meta:
        # 指定当前模型映射的表名
        db_table = 't_user'
        verbose_name = '客户管理'
        # 设置复数的表示方式
        verbose_name_plural = verbose_name


class RealProfile(models.Model):
    # 声明一对一的关联关系
    user = models.OneToOneField(User,
                                verbose_name='账号',
                                on_delete=models.CASCADE)
    real_name = models.CharField(max_length=20,
                                 verbose_name='真实姓名')
    number = models.CharField(max_length=18,
                              verbose_name='证件号')
    certificate_type = models.IntegerField(choices=((0, '身份证'),
                                                    (1, '护照'),
                                                    (2, '驾驶证')),
                                           verbose_name='证件类型')
    image1 = models.ImageField(verbose_name='正面照', upload_to='user/real')
    image2 = models.ImageField(verbose_name='反面照', upload_to='user/real')

    def __str__(self):
        return self.real_name

    class Meta:
        db_table = 't_user_profile'
        verbose_name = verbose_name_plural = '实名认证表'


# 水果分类模型
class CateType(models.Model):
    name = models.CharField(max_length=20,
                            verbose_name='分类名') # 后台管理显示的名称
    order_num = models.IntegerField(verbose_name='序号')

    def __str__(self):
        return self.name

    class Meta:
        # 指定当前模型映射的表名
        db_table = 't_category'
        # 设置排序字段，-表示降序
        ordering = ['-order_num']
        verbose_name = '水果分类'
        # 设置复数的表示方式
        verbose_name_plural = verbose_name


class Fruit(models.Model):
    name = models.CharField(max_length=20, verbose_name='水果名')
    price = models.FloatField(verbose_name='价格')
    source = models.CharField(max_length=30, verbose_name='原产地')
    category = models.ForeignKey(CateType,
                                 related_name='fruits',
                                 to_field='id', # 一般情况下，和一对多的“一”那一端的哪个属性建立关系
                                 on_delete=models.CASCADE,
                                 blank=True,
                                 null=True)

    # 默认情况下，反向引用的名称是当前类名小写_set
    # 可以通过related_name来指定
    # db_table 表示使用第三张表建立fruit和user的多对多关系
    users = models.ManyToManyField(User,
                                   db_table='t_collect',
                                   related_name='fruits',
                                   verbose_name='收藏用户列表',
                                   blank=True,
                                   null=True)
    tags = models.ManyToManyField('Tag', # 标签类定义在此类的后面
                                  db_table='t_fruit_tags',
                                  related_name='fruits',
                                  verbose_name='所有标签',
                                  blank=True,
                                  null=True)

    def __str__(self):
        return self.name

    class Meta:
        # 指定当前模型映射的表名
        db_table = 't_fruit'
        verbose_name = '水果表'
        # 设置复数的表示方式
        verbose_name_plural = verbose_name


# 声明水果商品和购物车的关系表（多对多关系中间表--购物车详情表）
class FruitCart(models.Model):
    from orderapp.models import Cart
    cart = models.ForeignKey(Cart,
                             on_delete=models.CASCADE,
                             verbose_name='购物车') # 级联删除
    fruit = models.ForeignKey(Fruit,
                              on_delete=models.CASCADE,
                              verbose_name='水果名') # 级联删除
    cnt = models.IntegerField(verbose_name='数量',
                              default=1)

    @property
    def price(self):
        # 属性方法在后台显示时没有verbose_name
        return round(self.cnt*self.fruit.price, 2)

    @property
    def unit_price(self):
        # 从表获取主表的对象属性
        return self.fruit.price

    def __str__(self):
        return self.fruit.name + ':' + self.cart.no

    class Meta:
        # 指定当前模型映射的表名
        db_table = 't_fruit_cart'
        verbose_name_plural = verbose_name = '购物车详情表'


class Store(models.Model):
    id = models.UUIDField(primary_key=True)
    name = models.CharField(max_length=50, verbose_name='店名', unique=True, db_column='name')
    store_type = models.IntegerField(choices=((0, '自营'), (1, '第三方')), verbose_name='类型')
    address = models.CharField(max_length=50, verbose_name='地址')
    city = models.CharField(max_length=50, verbose_name='城市',
                            db_index=True) # 用这个字段创建索引

    # 上传图片字段
    logo = models.ImageField(verbose_name='logo',
                             upload_to='store',  # 上传文件保存的目录
                             width_field='logo_width',
                             height_field='logo_height',
                             null=True,
                             blank=True)
    logo_width = models.IntegerField(verbose_name='logo宽度', null=True)
    logo_height = models.IntegerField(verbose_name='logo高度', null=True)

    summary = models.TextField(verbose_name='介绍',
                               null=True,
                               blank=True)
    create_time = models.DateField(verbose_name='成立时间',
                                   auto_now_add=True, null=True) # 第一次添加字段时创建
    last_time = models.DateField(verbose_name='最后修改时间',
                                 auto_now=True, null=True)  # 每次修改字段时设置

    def __str__(self):
        return self.name

    # 向数据库中添加记录时调用此方法，重写save方法
    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        # 设置ID值
        if not self.id:  # 判断是否是新增，新增才需要产生ID值
            self.id = uuid.uuid4().hex
        # 调用父类save方法
        super().save()

    @property  # 把类方法转成属性
    def id_(self):  # 把ID起一个别名id_，去掉中间'-'后返回
        # return str(self.id).replace('-', '')
        return self.id.hex

    class Meta:
        # 指定当前模型映射的表名
        db_table = 't_store'
        unique_together = (('name', 'city'),)
        verbose_name = '水果店'
        # 设置复数的表示方式
        verbose_name_plural = verbose_name


class Tag(models.Model):
    name = models.CharField(max_length=50, verbose_name='标签名', unique=True)
    order_num = models.IntegerField(verbose_name='序号', default=1)

    def __str__(self):
        return self.name

    class Meta:
        # 指定当前模型映射的表名
        db_table = 't_tag'
        verbose_name_plural = verbose_name = '标签表'
        ordering = ['-order_num']



