# Generated by Django 5.1.2 on 2024-12-06 19:28

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_trancasction'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('checkout_id', models.CharField(max_length=100, unique=True)),
                ('mpesa_code', models.CharField(max_length=100, unique=True)),
                ('phone_number', models.CharField(max_length=15)),
                ('status', models.CharField(max_length=20)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.RenameModel(
            old_name='Wishlist',
            new_name='Wishlist_model',
        ),
        migrations.DeleteModel(
            name='Trancasction',
        ),
        migrations.AlterModelOptions(
            name='wishlist_model',
            options={'verbose_name_plural': 'wishlists'},
        ),
    ]
