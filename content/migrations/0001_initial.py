# Generated by Django 5.0.3 on 2024-06-19 23:32

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('slug', models.SlugField(max_length=255, unique=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('slug', models.SlugField(max_length=255, unique=True)),
                ('is_sub', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('sub', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sub_cate', to='content.category')),
            ],
        ),
        migrations.CreateModel(
            name='Advertisement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('body', models.TextField()),
                ('image', models.ImageField(upload_to='advertisements/')),
                ('status', models.CharField(choices=[('new', 'نو'), ('like-new', 'در حد نو'), ('used', 'کارکرده'), ('need-repair', 'نیاز به تعمیر')], max_length=11)),
                ('price', models.BigIntegerField()),
                ('fixed_price', models.BooleanField(default=False)),
                ('wiling_excheng', models.BooleanField(default=False)),
                ('slug', models.SlugField(max_length=255, unique=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_advertisement', to=settings.AUTH_USER_MODEL)),
                ('category', models.ManyToManyField(related_name='cate_advertisement', to='content.category')),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='city_advertisement', to='content.city')),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
    ]
