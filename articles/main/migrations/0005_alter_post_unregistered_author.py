# Generated by Django 4.1.1 on 2023-03-20 07:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_alter_comment_options_alter_post_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='unregistered_author',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='Незарегистрированный автор'),
        ),
    ]
