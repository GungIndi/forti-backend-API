# Generated by Django 4.2.6 on 2023-12-01 06:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fortiApi', '0011_rename_replies_reply_user_email'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='nomor_induk',
            new_name='identity_number',
        ),
    ]
