# Generated by Django 3.1.4 on 2021-01-04 08:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ProfileModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=6)),
                ('phone', models.IntegerField(blank=True, null=True)),
                ('avatar', models.ImageField(blank=True, max_length=500, upload_to='Authentication/static/user/avatar')),
                ('bio', models.CharField(max_length=101)),
                ('tag', models.CharField(max_length=32, unique=True)),
                ('location', models.CharField(max_length=64)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'ProfileModel',
            },
        ),
    ]
