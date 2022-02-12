# Generated by Django 4.0.2 on 2022-02-12 03:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orderapp', '0002_cart'),
        ('mainapp', '0005_realprofile'),
    ]

    operations = [
        migrations.CreateModel(
            name='FruitCart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cnt', models.IntegerField(default=1, verbose_name='数量')),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orderapp.cart', verbose_name='购物车')),
                ('fruit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.fruit', verbose_name='水果名')),
            ],
            options={
                'verbose_name': '购物车详情表',
                'verbose_name_plural': '购物车详情表',
                'db_table': 't_fruit_cart',
            },
        ),
    ]
