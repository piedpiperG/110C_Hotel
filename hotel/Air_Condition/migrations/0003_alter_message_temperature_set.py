# Generated by Django 4.2.5 on 2023-11-25 12:12

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("Air_Condition", "0002_message"),
    ]

    operations = [
        migrations.AlterField(
            model_name="message",
            name="temperature_set",
            field=models.CharField(default="1", max_length=10),
        ),
    ]
