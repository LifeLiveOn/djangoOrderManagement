# Generated by Django 4.2.5 on 2023-09-24 19:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_customer_date_created_customer_email_customer_phone_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, null=True)),
                ('price', models.FloatField(null=True)),
                ('category', models.CharField(choices=[('Indoor', 'Indoor'), ('Outdoor', 'Outdoor')], max_length=200, null=True)),
                ('description', models.CharField(max_length=200, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True)),
            ],
        ),
        migrations.AlterField(
            model_name='customer',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('status', models.CharField(choices=[('Pending', 'Pending'), ('Out for delivery', 'Out for delivery'), ('Delivered', 'Delivered')], max_length=200, null=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.customer')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.product')),
            ],
        ),
    ]