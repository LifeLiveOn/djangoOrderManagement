# Generated by Django 4.2.5 on 2023-10-17 03:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0010_alter_customer_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='profile_pic',
            field=models.ImageField(blank=True, default='images/profile_pic.jgp', null=True, upload_to=''),
        ),
    ]
