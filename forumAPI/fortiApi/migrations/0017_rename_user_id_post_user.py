# Generated by Django 4.2.6 on 2023-12-19 08:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fortiApi', '0016_post_user_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='user_id',
            new_name='user',
        ),
    ]
