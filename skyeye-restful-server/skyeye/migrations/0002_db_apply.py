import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("skyeye", "0001_initial"),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            database_operations=[
                migrations.CreateModel(
                    name="Scan360Config",
                    fields=[
                        ("id", models.AutoField(help_text="auto increment PK", primary_key=True, serialize=False)),
                        ("step_angle", models.FloatField(blank=True, help_text="회전 각도", null=True)),
                        ("pitch", models.FloatField(blank=True, help_text="Pitch", null=True)),
                        ("zoom_level", models.IntegerField(blank=True, help_text="줌레벨", null=True)),
                        ("dwell_seconds", models.IntegerField(default=20, help_text="체류 시간(초)")),
                        (
                            "site",
                            models.OneToOneField(
                                db_column="site_id",
                                help_text="사이트 번호",
                                on_delete=django.db.models.deletion.CASCADE,
                                related_name="scan360",
                                to="skyeye.site",
                            ),
                        ),
                    ],
                    options={
                        "db_table": "scan360_config",
                        "managed": True,
                    },
                ),
                migrations.CreateModel(
                    name="Poi",
                    fields=[
                        ("id", models.AutoField(help_text="auto increment PK", primary_key=True, serialize=False)),
                        ("date", models.DateTimeField(auto_now=True, help_text="날짜")),
                        ("name", models.CharField(blank=True, help_text="지점명", max_length=100, null=True)),
                        ("latitude", models.FloatField(blank=True, help_text="위도", null=True)),
                        ("longitude", models.FloatField(blank=True, help_text="경도", null=True)),
                        ("altitude", models.FloatField(blank=True, help_text="고도", null=True)),
                        ("zoom_level", models.IntegerField(blank=True, help_text="줌레벨", null=True)),
                        ("dwell_seconds", models.IntegerField(default=20, help_text="체류 시간(초)")),
                        ("pitch", models.FloatField(blank=True, help_text="Pitch", null=True)),
                        ("order", models.IntegerField(blank=True, help_text="순서", null=True)),
                        (
                            "site",
                            models.ForeignKey(
                                db_column="site_id",
                                help_text="사이트 번호",
                                on_delete=django.db.models.deletion.CASCADE,
                                to="skyeye.site",
                            ),
                        ),
                    ],
                    options={
                        "db_table": "poi",
                        "managed": True,
                    },
                ),
            ],
            state_operations=[],
        ),
    ]