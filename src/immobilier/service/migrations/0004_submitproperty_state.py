# Generated by Django 4.1.1 on 2022-09-29 12:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0003_alter_submitproperty_name_alter_submitproperty_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='submitproperty',
            name='state',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='property_state', to='service.state'),
        ),
    ]
