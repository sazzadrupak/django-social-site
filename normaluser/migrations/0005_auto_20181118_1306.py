# Generated by Django 2.1.2 on 2018-11-18 11:06

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('normaluser', '0004_normaluser_email_validation_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='normaluser',
            name='image',
            field=models.ImageField(blank=True, default=django.utils.timezone.now, upload_to='profile_image'),
            preserve_default=False,
        ),
    ]