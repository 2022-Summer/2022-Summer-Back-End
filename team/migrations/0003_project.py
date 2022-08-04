# Generated by Django 3.2.5 on 2022-08-04 12:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
        ('team', '0002_rename_group_membership_team'),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=20)),
                ('start_time', models.DateTimeField(auto_now_add=True)),
                ('description', models.CharField(default='', max_length=255)),
                ('recycled', models.BooleanField(default=False)),
                ('leader', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.user')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='team.team')),
            ],
        ),
    ]
