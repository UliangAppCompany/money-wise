# Generated by Django 4.1.2 on 2022-10-29 02:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("account_management", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="account",
            name="is_control",
            field=models.BooleanField(default=False),
        ),
    ]
