# Generated by Django 4.2.6 on 2024-02-13 09:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0009_payment_payment_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='payment_status',
            field=models.CharField(choices=[('REQUIRE_PAYMENT_METHOD', 'requires_payment_method'), ('REQUIRES_ACTION', 'requires_action'), ('SUCCEEDED', 'succeeded'), ('FAILED', 'Failed')], default='PENDING', max_length=50),
        ),
    ]