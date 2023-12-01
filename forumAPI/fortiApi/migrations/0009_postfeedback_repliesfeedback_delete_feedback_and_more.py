# Generated by Django 4.2.6 on 2023-12-01 06:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fortiApi', '0008_feedback_content_type_feedback_feedback_type_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='PostFeedback',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('feedback_type', models.CharField(choices=[('Like', 'Like'), ('Dislike', 'Dislike')], default='Like')),
                ('created_at', models.DateField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='RepliesFeedback',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('feedback_type', models.CharField(choices=[('Like', 'Like'), ('Dislike', 'Dislike')], default='Like')),
                ('created_at', models.DateField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.DeleteModel(
            name='Feedback',
        ),
        migrations.RenameField(
            model_name='post',
            old_name='user_name',
            new_name='user_id',
        ),
        migrations.RenameField(
            model_name='replies',
            old_name='user_name',
            new_name='user_id',
        ),
        migrations.AddField(
            model_name='post',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='replies',
            name='content',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='replies',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='user',
            name='nomor_induk',
            field=models.CharField(default='', max_length=19),
        ),
        migrations.AddField(
            model_name='user',
            name='password',
            field=models.CharField(default='', max_length=32),
        ),
        migrations.AddField(
            model_name='user',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='content',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='post',
            name='created_at',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='replies',
            name='post_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fortiApi.post'),
        ),
        migrations.AlterField(
            model_name='user',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='user_name',
            field=models.CharField(max_length=30),
        ),
        migrations.AddField(
            model_name='repliesfeedback',
            name='replies_id',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='fortiApi.replies'),
        ),
        migrations.AddField(
            model_name='repliesfeedback',
            name='user_id',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.DO_NOTHING, to='fortiApi.user'),
        ),
        migrations.AddField(
            model_name='postfeedback',
            name='post_id',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='fortiApi.post'),
        ),
        migrations.AddField(
            model_name='postfeedback',
            name='user_id',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.DO_NOTHING, to='fortiApi.user'),
        ),
    ]
