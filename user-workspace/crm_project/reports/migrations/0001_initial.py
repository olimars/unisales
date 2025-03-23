# Generated by Django 4.2.20 on 2025-03-23 23:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("contenttypes", "0002_remove_content_type_name"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Dashboard",
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
                ("name", models.CharField(max_length=200)),
                ("description", models.TextField(blank=True)),
                ("is_public", models.BooleanField(default=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "created_by",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Report",
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
                ("name", models.CharField(max_length=200)),
                ("description", models.TextField(blank=True)),
                (
                    "report_type",
                    models.CharField(
                        choices=[
                            ("sales", "Sales Report"),
                            ("marketing", "Marketing Report"),
                            ("support", "Support Report"),
                            ("activity", "Activity Report"),
                            ("custom", "Custom Report"),
                        ],
                        max_length=20,
                    ),
                ),
                ("query", models.TextField()),
                ("parameters", models.JSONField(default=dict)),
                ("is_scheduled", models.BooleanField(default=False)),
                (
                    "schedule_type",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("daily", "Daily"),
                            ("weekly", "Weekly"),
                            ("monthly", "Monthly"),
                            ("quarterly", "Quarterly"),
                        ],
                        max_length=20,
                        null=True,
                    ),
                ),
                ("last_run", models.DateTimeField(blank=True, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "created_by",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "recipients",
                    models.ManyToManyField(
                        blank=True,
                        related_name="subscribed_reports",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Widget",
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
                ("name", models.CharField(max_length=200)),
                (
                    "widget_type",
                    models.CharField(
                        choices=[
                            ("line_chart", "Line Chart"),
                            ("bar_chart", "Bar Chart"),
                            ("pie_chart", "Pie Chart"),
                            ("metric", "Single Metric"),
                            ("table", "Table"),
                            ("funnel", "Funnel"),
                            ("kanban", "Kanban Board"),
                        ],
                        max_length=20,
                    ),
                ),
                ("query", models.TextField()),
                ("refresh_interval", models.PositiveIntegerField(default=3600)),
                ("position_x", models.PositiveIntegerField()),
                ("position_y", models.PositiveIntegerField()),
                ("width", models.PositiveIntegerField()),
                ("height", models.PositiveIntegerField()),
                ("configuration", models.JSONField(default=dict)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "dashboard",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="widgets",
                        to="reports.dashboard",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ReportExport",
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
                (
                    "format",
                    models.CharField(
                        choices=[("csv", "CSV"), ("xlsx", "Excel"), ("pdf", "PDF")],
                        max_length=10,
                    ),
                ),
                ("file", models.FileField(upload_to="reports/exports/")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "created_by",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "report",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="exports",
                        to="reports.report",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Metric",
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
                ("name", models.CharField(max_length=200)),
                ("description", models.TextField(blank=True)),
                ("object_id", models.PositiveIntegerField()),
                ("value", models.DecimalField(decimal_places=2, max_digits=15)),
                ("timestamp", models.DateTimeField()),
                ("metadata", models.JSONField(default=dict)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "content_type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="contenttypes.contenttype",
                    ),
                ),
            ],
            options={
                "indexes": [
                    models.Index(
                        fields=["content_type", "object_id"],
                        name="reports_met_content_404a96_idx",
                    ),
                    models.Index(
                        fields=["timestamp"], name="reports_met_timesta_27f71d_idx"
                    ),
                ],
            },
        ),
    ]
