# Generated by Django 5.1 on 2024-09-17 12:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("payment", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="paymentlink",
            name="short_name",
            field=models.CharField(default="short name here", max_length=100),
            preserve_default=False,
        ),
    ]
