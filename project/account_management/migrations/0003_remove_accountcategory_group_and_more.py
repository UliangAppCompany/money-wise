# Generated by Django 4.1.1 on 2022-09-27 16:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("account_management", "0002_alter_account_number_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="accountcategory",
            name="group",
        ),
        migrations.AlterField(
            model_name="account",
            name="description",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="accountcategory",
            name="description",
            field=models.TextField(blank=True, null=True),
        ),
    ]
