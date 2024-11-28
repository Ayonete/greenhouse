# Generated by Django 5.1.3 on 2024-11-28 15:50

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Crop",
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
                ("name", models.CharField(max_length=100)),
                ("description", models.TextField(max_length=300)),
                ("image", models.ImageField(upload_to="images/")),
                ("temperature", models.DecimalField(decimal_places=2, max_digits=4)),
                ("moisture", models.DecimalField(decimal_places=2, max_digits=4)),
            ],
            options={
                "ordering": ["name"],
            },
        ),
        migrations.CreateModel(
            name="Diagnostics",
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
                ("name", models.CharField(max_length=100, null=True)),
                ("discoloration", models.CharField(max_length=100, null=True)),
                ("deformed", models.TextField(default="None", max_length=300)),
                ("region_affected", models.TextField(max_length=300, null=True)),
            ],
            options={
                "ordering": ["name"],
            },
        ),
    ]