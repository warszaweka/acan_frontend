# Generated by Django 3.2.13 on 2022-05-15 05:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('acan', '0005_course_order_int'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='image',
            field=models.FileField(null=True, upload_to='article_images/'),
        ),
    ]
