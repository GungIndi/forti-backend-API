# Generated by Django 4.2.6 on 2023-11-30 13:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fortiApi', '0005_alter_post_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='created_at',
            field=models.DateField(auto_now=True),
        ),
    ]