# Generated by Django 3.0 on 2020-04-04 14:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eunoiaapp', '0003_auto_20200404_2011'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='belongs_to_company',
        ),
        migrations.DeleteModel(
            name='Company',
        ),
    ]