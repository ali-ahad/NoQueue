# Generated by Django 2.1.7 on 2019-04-09 11:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('launch', '0026_auto_20190409_1009'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='owner',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='launch.OwnerProfile'),
        ),
    ]