# Generated by Django 4.0.2 on 2022-02-12 06:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0006_fruitcart'),
    ]

    operations = [
        migrations.AddField(
            model_name='fruit',
            name='users',
            field=models.ManyToManyField(db_table='t_collect', related_name='fruits', to='mainapp.User', verbose_name='收藏的用户列表'),
        ),
    ]
