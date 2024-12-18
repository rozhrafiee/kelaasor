# Generated by Django 5.1.2 on 2024-11-03 16:45

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('userapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='OnlineClass',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='created_classes', to='userapp.userprofile')),
            ],
        ),
        migrations.CreateModel(
            name='ClassMembership',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(choices=[('student', 'Student'), ('teacher', 'Teacher'), ('mentor', 'Mentor')], max_length=10)),
                ('user_profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='userapp.userprofile')),
                ('online_class', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='memberships', to='class.onlineclass')),
            ],
            options={
                'unique_together': {('user_profile', 'online_class', 'role')},
            },
        ),
    ]
