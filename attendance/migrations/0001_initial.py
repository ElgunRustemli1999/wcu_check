# Generated by Django 5.1.6 on 2025-04-16 10:51

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Attendance",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("check_in_time", models.DateTimeField(null=True)),
                ("check_out_time", models.DateTimeField(blank=True, null=True)),
                ("is_checked_in", models.BooleanField(default=False)),
                ("extra_hours", models.FloatField(default=0)),
                ("late_minutes", models.IntegerField(default=0)),
                ("is_holiday", models.BooleanField(default=False)),
                (
                    "early_leave",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                ("is_approved_leave", models.BooleanField(default=False)),
                ("is_absent", models.BooleanField(default=False)),
                (
                    "status",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("ontime", "Vaxtında gəlib"),
                            ("late", "Gec gəlib"),
                            ("absent", "Gəlməyib"),
                            ("early_leave", "Tez çıxıb"),
                        ],
                        max_length=20,
                        null=True,
                    ),
                ),
            ],
        ),
    ]
