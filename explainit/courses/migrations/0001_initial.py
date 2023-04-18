# Generated by Django 4.2 on 2023-04-18 11:01

import ckeditor.fields
import courses.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='OurCourse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_title', models.CharField(max_length=254)),
                ('is_free', models.BooleanField(default=False)),
                ('is_paid', models.BooleanField(default=False)),
                ('course_description', ckeditor.fields.RichTextField()),
                ('course_poster', models.ImageField(upload_to=courses.models.course_poster_image_upload_path, verbose_name='Course poster')),
                ('is_approved', models.BooleanField(default=False)),
                ('publish', models.BooleanField(default=False)),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('date_updated', models.DateTimeField(auto_now=True, null=True)),
                ('course_instructor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='courses', to=settings.AUTH_USER_MODEL)),
                ('students', models.ManyToManyField(blank=True, related_name='students', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
