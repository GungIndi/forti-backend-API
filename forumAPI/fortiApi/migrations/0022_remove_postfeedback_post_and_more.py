# Generated by Django 4.2.6 on 2023-12-19 09:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fortiApi', '0021_alter_post_content'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='postfeedback',
            name='post',
        ),
        migrations.RemoveField(
            model_name='repliesfeedback',
            name='replies',
        ),
        migrations.AddField(
            model_name='post',
            name='feedback',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='fortiApi.postfeedback'),
        ),
        migrations.AddField(
            model_name='reply',
            name='feedback',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='fortiApi.repliesfeedback'),
        ),
        migrations.AlterField(
            model_name='repliesfeedback',
            name='feedback_type',
            field=models.CharField(choices=[('Like', 'Like'), ('Dislike', 'Dislike')], default='Like', null=True),
        ),
    ]
