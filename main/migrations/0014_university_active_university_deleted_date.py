# Generated by Django 5.1 on 2024-10-21 15:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0013_alter_comments_comment_alter_comments_post_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='university',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='university',
            name='deleted_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]