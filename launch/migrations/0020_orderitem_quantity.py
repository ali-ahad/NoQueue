# Generated by Django 2.1.7 on 2019-04-03 18:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('launch', '0019_customerprofile_cart'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='quantity',
            field=models.IntegerField(default=1),
        ),
    ]
