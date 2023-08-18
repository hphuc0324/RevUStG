# Generated by Django 4.2.1 on 2023-08-18 15:30

from django.db import migrations, models
import shortuuid.django_fields


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_alter_phonecardpayment_value'),
    ]

    operations = [
        migrations.CreateModel(
            name='BankAccountPayment',
            fields=[
                ('id', shortuuid.django_fields.ShortUUIDField(alphabet=None, length=10, max_length=30, prefix='BAP', primary_key=True, serialize=False, unique=True)),
                ('bank', models.CharField(choices=[('Agribank', 'Agribank'), ('Vietcombank', 'Vietcombank'), ('MBBank', 'MBBank')], max_length=100, null=True)),
                ('account', models.CharField(help_text='9 to 14 digits', max_length=14, null=True)),
                ('value', models.PositiveIntegerField(default=0, null=True)),
            ],
        ),
    ]