# Generated by Django 4.2.6 on 2023-12-19 09:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fortiApi', '0020_alter_post_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='content',
            field=models.TextField(default=''),
        ),
    ]