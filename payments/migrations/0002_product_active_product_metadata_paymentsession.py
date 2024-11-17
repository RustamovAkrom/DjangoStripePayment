# Generated by Django 5.1.3 on 2024-11-17 05:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='active',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='metadata',
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.CreateModel(
            name='PaymentSession',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stripe_session_id', models.CharField(max_length=255, unique=True)),
                ('customer_email', models.EmailField(blank=True, max_length=254, null=True)),
                ('currency', models.CharField(default='usd', max_length=10)),
                ('amount_total', models.PositiveIntegerField()),
                ('status', models.CharField(blank=True, max_length=50, null=True)),
                ('payment_status', models.CharField(blank=True, max_length=50, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='payments.product')),
            ],
            options={
                'verbose_name': 'Payment Session',
                'verbose_name_plural': 'Pyament Sessions',
                'db_table': 'payment_sessions',
            },
        ),
    ]