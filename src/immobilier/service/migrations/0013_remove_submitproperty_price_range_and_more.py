# Generated by Django 4.1.1 on 2022-10-07 16:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0012_alter_submitproperty_videos2'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='submitproperty',
            name='price_range',
        ),
        migrations.AddField(
            model_name='submitproperty',
            name='price_range_max',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='price_rangemax', to='service.pricerangemax'),
        ),
        migrations.AddField(
            model_name='submitproperty',
            name='price_range_min',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='price_rangemin', to='service.pricerangemin'),
        ),
    ]
