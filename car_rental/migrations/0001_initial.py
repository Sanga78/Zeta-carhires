# Generated by Django 5.0.6 on 2024-08-02 14:02

import django.contrib.auth.models
import django.contrib.auth.validators
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="CarImage",
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
                ("image", models.ImageField(upload_to="car_images/")),
            ],
        ),
        migrations.CreateModel(
            name="Fleet",
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
                ("full_name", models.CharField(max_length=200)),
                ("company_name", models.CharField(max_length=200)),
                ("email", models.EmailField(max_length=254)),
                ("phone_number", models.IntegerField()),
                ("no_of_cars", models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name="Responses",
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
                ("customer_name", models.CharField(max_length=200)),
                ("email", models.EmailField(max_length=254)),
                ("phone_number", models.IntegerField()),
                ("message", models.CharField(max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name="Tours_request",
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
                ("full_name", models.CharField(max_length=200)),
                ("email", models.EmailField(max_length=254)),
                ("phone_number", models.IntegerField()),
                ("message", models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name="Vehicle",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("car_name", models.CharField(max_length=20)),
                (
                    "car_image",
                    models.ImageField(
                        blank=True,
                        default="static/car-1.png",
                        null=True,
                        upload_to="vehicle_images",
                    ),
                ),
                ("color", models.CharField(max_length=10)),
                ("capacity", models.CharField(max_length=2)),
                ("price", models.FloatField()),
                ("is_available", models.BooleanField(default=True)),
                ("description", models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name="CustomUser",
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
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                (
                    "is_superuser",
                    models.BooleanField(
                        default=False,
                        help_text="Designates that this user has all permissions without explicitly assigning them.",
                        verbose_name="superuser status",
                    ),
                ),
                (
                    "username",
                    models.CharField(
                        error_messages={
                            "unique": "A user with that username already exists."
                        },
                        help_text="Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.",
                        max_length=150,
                        unique=True,
                        validators=[
                            django.contrib.auth.validators.UnicodeUsernameValidator()
                        ],
                        verbose_name="username",
                    ),
                ),
                (
                    "first_name",
                    models.CharField(
                        blank=True, max_length=150, verbose_name="first name"
                    ),
                ),
                (
                    "last_name",
                    models.CharField(
                        blank=True, max_length=150, verbose_name="last name"
                    ),
                ),
                (
                    "email",
                    models.EmailField(
                        blank=True, max_length=254, verbose_name="email address"
                    ),
                ),
                (
                    "is_staff",
                    models.BooleanField(
                        default=False,
                        help_text="Designates whether the user can log into this admin site.",
                        verbose_name="staff status",
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(
                        default=True,
                        help_text="Designates whether this user should be treated as active. Unselect this instead of deleting accounts.",
                        verbose_name="active",
                    ),
                ),
                (
                    "date_joined",
                    models.DateTimeField(
                        default=django.utils.timezone.now, verbose_name="date joined"
                    ),
                ),
                (
                    "user_type",
                    models.CharField(
                        choices=[(1, "Dealer"), (2, "Customer")],
                        default=1,
                        max_length=10,
                    ),
                ),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True,
                        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.group",
                        verbose_name="groups",
                    ),
                ),
                (
                    "user_permissions",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Specific permissions for this user.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.permission",
                        verbose_name="user permissions",
                    ),
                ),
            ],
            options={
                "verbose_name": "user",
                "verbose_name_plural": "users",
                "abstract": False,
            },
            managers=[
                ("objects", django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name="CarDealer",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now_add=True)),
                (
                    "admin",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Car",
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
                ("model", models.CharField(max_length=100)),
                ("price", models.CharField(max_length=20)),
                ("description", models.TextField()),
                ("colors", models.CharField(max_length=100)),
                ("seats", models.IntegerField()),
                ("main_image", models.ImageField(upload_to="cars/")),
                (
                    "additional_images",
                    models.ManyToManyField(
                        related_name="cars", to="car_rental.carimage"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Customer",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("profile_pic", models.FileField(upload_to="")),
                ("address", models.TextField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now_add=True)),
                (
                    "admin",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Hire_Request",
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
                ("full_name", models.CharField(max_length=200)),
                ("destination", models.CharField(max_length=200)),
                ("phone_number", models.IntegerField()),
                ("rented_on", models.DateTimeField(auto_now_add=True)),
                ("rented_to", models.DateTimeField(auto_now_add=True)),
                (
                    "car_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="car_rental.vehicle",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Booking",
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
                    "booking_date",
                    models.DateTimeField(default=django.utils.timezone.now),
                ),
                ("return_date", models.DateTimeField(blank=True, null=True)),
                ("total_cost", models.FloatField(blank=True, null=True)),
                (
                    "customer_name",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="car_rental.customer",
                    ),
                ),
                (
                    "car",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="car_rental.vehicle",
                    ),
                ),
            ],
        ),
    ]
