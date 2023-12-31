# Generated by Django 4.2.5 on 2023-12-07 08:39

import Air_Condition.models
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("Air_Condition", "0004_message_room_id"),
    ]

    operations = [
        migrations.DeleteModel(
            name="Server",
        ),
        migrations.AddField(
            model_name="room",
            name="serve_duration",
            field=models.IntegerField(default=0, verbose_name="服务时长"),
        ),
        migrations.AddField(
            model_name="room",
            name="serve_end_time",
            field=models.DateTimeField(blank=True, null=True, verbose_name="服务结束时间"),
        ),
        migrations.AddField(
            model_name="room",
            name="serve_start_time",
            field=models.DateTimeField(blank=True, null=True, verbose_name="服务开始时间"),
        ),
        migrations.AlterField(
            model_name="room",
            name="fan_speed",
            field=models.IntegerField(
                choices=[(3, "LOW"), (2, "MIDDLE"), (1, "HIGH")],
                default=2,
                verbose_name="风速",
            ),
        ),
        migrations.AlterField(
            model_name="room",
            name="request_time",
            field=models.DateTimeField(
                default=Air_Condition.models.time_now, verbose_name="请求发出时间"
            ),
        ),
    ]
