# Generated by Django 3.0.7 on 2020-12-21 22:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0003_auto_20201221_2037'),
    ]

    operations = [
        migrations.AddField(
            model_name='business',
            name='photo',
            field=models.ImageField(default='avatar.png', upload_to='uploads'),
        ),
        migrations.CreateModel(
            name='BusinessRole',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.PositiveSmallIntegerField(choices=[(1, 'Administrator'), (2, 'Public User'), (3, 'Business Owner'), (4, 'Store Manager'), (5, 'Dispatch Manager')])),
                ('business', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='business.Business')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='business.BaseUser')),
            ],
        ),
    ]