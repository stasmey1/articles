# Generated by Django 4.1.1 on 2023-03-20 11:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_alter_post_unregistered_author'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='comment',
            field=models.CharField(max_length=225, verbose_name='Комментарий'),
        ),
    ]
