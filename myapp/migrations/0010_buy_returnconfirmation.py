# Generated by Django 4.2 on 2023-05-07 22:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0009_remove_returnconfirmation_buy_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Buy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('summ', models.IntegerField()),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='myapp.product')),
                ('site_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='buy_users', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ReturnConfirmation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('buy', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='buy_returns', to='myapp.buy')),
                ('site_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='return_users', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
