# Generated by Django 3.1.4 on 2021-01-09 22:06

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
            name='CoinModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('coin_name', models.TextField(max_length=64)),
                ('coin_avatar', models.ImageField(max_length=500, upload_to='Authentication/static/user/avatar')),
            ],
            options={
                'db_table': 'CoinModel',
            },
        ),
        migrations.CreateModel(
            name='CreditCard',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('card_type', models.CharField(default='Unknown', max_length=64)),
                ('card_no', models.IntegerField()),
                ('card_name', models.CharField(max_length=64)),
                ('expiry_date', models.DateField()),
                ('cvv', models.IntegerField()),
            ],
            options={
                'db_table': 'CreditCard',
            },
        ),
        migrations.CreateModel(
            name='WalletModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('wallet_id', models.CharField(max_length=64)),
                ('balance', models.IntegerField(default=0.0)),
                ('coin', models.ManyToManyField(to='Wallet.CoinModel')),
                ('credit_card', models.ManyToManyField(blank=True, to='Wallet.CreditCard')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'WalletModel',
            },
        ),
        migrations.CreateModel(
            name='VirtualCardModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=101)),
                ('city', models.CharField(max_length=32)),
                ('state', models.CharField(max_length=32)),
                ('postal_code', models.IntegerField()),
                ('country', models.CharField(max_length=32)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'VirtualCardModel',
            },
        ),
    ]
