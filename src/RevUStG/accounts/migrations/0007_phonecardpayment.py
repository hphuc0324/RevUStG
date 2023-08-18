# Generated by Django 4.2.1 on 2023-08-17 16:25

from django.db import migrations, models
import shortuuid.django_fields


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_orderproduct_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='PhoneCardPayment',
            fields=[
                ('id', shortuuid.django_fields.ShortUUIDField(alphabet=None, length=10, max_length=30, prefix='PCP', primary_key=True, serialize=False, unique=True)),
                ('mobile_carrier', models.CharField(choices=[('Viettel', 'Viettel'), ('Mobifone', 'Mobifone'), ('Vinaphone', 'Vinaphone')], max_length=100, null=True)),
                ('serial_code', models.CharField(help_text='15 Digits', max_length=15, null=True)),
                ('card_code', models.CharField(help_text='14 Digits', max_length=14, null=True)),
            ],
        ),
    ]