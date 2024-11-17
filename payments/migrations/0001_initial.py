# Generated by Django 5.1.3 on 2024-11-17 05:17

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stripe_proudct_id', models.CharField(blank=True, max_length=255, null=True)),
                ('stripe_price_id', models.CharField(blank=True, max_length=255, null=True)),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True)),
                ('currency', models.CharField(default='usd', max_length=10)),
                ('amount', models.PositiveIntegerField(help_text='Amount in sentes, example, 2000 to $20.00')),
                ('quantity', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Product',
                'verbose_name_plural': 'Products',
                'db_table': 'products',
            },
        ),
    ]
