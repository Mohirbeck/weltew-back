# Generated by Django 4.1.7 on 2023-03-30 20:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_collectionmodel_description_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='collectioncategorymodel',
            name='url',
            field=models.URLField(default=''),
        ),
    ]
