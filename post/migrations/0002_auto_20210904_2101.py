# Generated by Django 3.1.7 on 2021-09-04 15:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ('-created_at',)},
        ),
    ]