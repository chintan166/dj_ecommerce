# Generated by Django 4.2.17 on 2025-01-19 17:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ecomm_app', '0013_cartitem_color'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='color',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='ecomm_app.color'),
        ),
    ]
