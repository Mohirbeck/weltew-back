# Generated by Django 4.1.7 on 2023-04-24 15:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0018_collectioncategorymodel_is_active_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productcategorymodel',
            name='last',
        ),
        migrations.RemoveField(
            model_name='productcategorymodel',
            name='layer',
        ),
        migrations.RemoveField(
            model_name='productcategorymodel',
            name='parent',
        ),
        migrations.AddField(
            model_name='collectioncategorymodel',
            name='order',
            field=models.IntegerField(default=0, verbose_name='Порядок'),
        ),
        migrations.AddField(
            model_name='productcategorymodel',
            name='order',
            field=models.IntegerField(default=0, verbose_name='Порядок'),
        ),
    ]
