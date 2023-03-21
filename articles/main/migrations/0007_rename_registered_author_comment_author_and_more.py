# Generated by Django 4.1.1 on 2023-03-21 07:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_alter_comment_comment'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='registered_author',
            new_name='author',
        ),
        migrations.RenameField(
            model_name='comment',
            old_name='comment',
            new_name='text',
        ),
        migrations.RenameField(
            model_name='post',
            old_name='registered_author',
            new_name='author',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='unregistered_author',
        ),
        migrations.RemoveField(
            model_name='post',
            name='unregistered_author',
        ),
        migrations.AddField(
            model_name='comment',
            name='anonimus',
            field=models.BooleanField(blank=True, default=True, verbose_name='Аноним'),
        ),
        migrations.AddField(
            model_name='post',
            name='anonimus',
            field=models.BooleanField(blank=True, default=True, verbose_name='Аноним'),
        ),
    ]