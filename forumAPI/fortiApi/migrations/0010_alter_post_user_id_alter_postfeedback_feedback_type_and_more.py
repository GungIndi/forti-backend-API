# Generated by Django 4.2.6 on 2023-12-01 06:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fortiApi', '0009_postfeedback_repliesfeedback_delete_feedback_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='fortiApi.user'),
        ),
        migrations.AlterField(
            model_name='postfeedback',
            name='feedback_type',
            field=models.CharField(choices=[('Like', 'Like'), ('Dislike', 'Dislike')]),
        ),
        migrations.AlterField(
            model_name='postfeedback',
            name='post_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fortiApi.post'),
        ),
        migrations.AlterField(
            model_name='postfeedback',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='fortiApi.user'),
        ),
        migrations.AlterField(
            model_name='replies',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='fortiApi.user'),
        ),
        migrations.AlterField(
            model_name='repliesfeedback',
            name='replies_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fortiApi.replies'),
        ),
        migrations.AlterField(
            model_name='repliesfeedback',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='fortiApi.user'),
        ),
        migrations.AlterField(
            model_name='user',
            name='nomor_induk',
            field=models.CharField(max_length=19),
        ),
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.CharField(max_length=32),
        ),
    ]
