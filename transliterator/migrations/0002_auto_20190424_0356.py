# Generated by Django 2.2 on 2019-04-23 19:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transliterator', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userdict',
            old_name='chinese_words',
            new_name='chinese_word',
        ),
    ]
