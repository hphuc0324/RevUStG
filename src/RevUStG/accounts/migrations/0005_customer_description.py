# Generated by Django 4.2.1 on 2023-07-30 14:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_customer_profile_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='description',
            field=models.TextField(default='A new member of RevustG', max_length=100, null=True),
        ),
    ]