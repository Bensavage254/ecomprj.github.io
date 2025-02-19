# Generated by Django 5.1.2 on 2024-12-02 21:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_alter_productreview_product'),
    ]

    operations = [
        migrations.CreateModel(
            name='Trancasction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('checkout_id', models.CharField(max_length=100, unique=True)),
                ('mpesa_code', models.CharField(max_length=100, unique=True)),
                ('phone_number', models.CharField(max_length=10)),
                ('status', models.CharField(max_length=20)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
