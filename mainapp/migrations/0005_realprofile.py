# Generated by Django 4.0.2 on 2022-02-11 21:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0004_store_logo_store_logo_height_store_logo_width_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='RealProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('real_name', models.CharField(max_length=20, verbose_name='真实姓名')),
                ('number', models.CharField(max_length=18, verbose_name='证件号')),
                ('certificate_type', models.IntegerField(choices=[(0, '身份证'), (1, '护照'), (2, '驾驶证')], verbose_name='证件类型')),
                ('image1', models.ImageField(upload_to='user/real', verbose_name='正面照')),
                ('image2', models.ImageField(upload_to='user/real', verbose_name='反面照')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='mainapp.user', verbose_name='账号')),
            ],
            options={
                'verbose_name': '实名认证表',
                'verbose_name_plural': '实名认证表',
                'db_table': 't_user_profile',
            },
        ),
    ]
