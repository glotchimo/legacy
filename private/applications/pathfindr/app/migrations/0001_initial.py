# Generated by Django 2.1.4 on 2018-12-18 02:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sfid', models.CharField(blank=True, max_length=32, verbose_name='Salesforce ID')),
                ('name', models.CharField(blank=True, max_length=356, verbose_name='Company Name')),
                ('domain', models.URLField(blank=True, null=True, verbose_name='Company Website')),
                ('phone', models.CharField(blank=True, max_length=32, null=True, verbose_name='Office Phone')),
                ('date_created', models.TimeField(auto_now=True, verbose_name='Date Imported')),
                ('date_updated', models.TimeField(auto_now_add=True, verbose_name='Date Updated')),
                ('status', models.CharField(blank=True, max_length=32, verbose_name='Status')),
            ],
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sfid', models.CharField(blank=True, max_length=256, null=True, verbose_name='Salesforce ID')),
                ('dorgid', models.CharField(blank=True, max_length=64, null=True, verbose_name='DiscoverOrg ID')),
                ('name', models.CharField(max_length=256, verbose_name='Name')),
                ('title', models.CharField(blank=True, max_length=256, null=True, verbose_name='Title')),
                ('email', models.EmailField(blank=True, max_length=254, null=True, verbose_name='Email')),
                ('direct', models.CharField(blank=True, max_length=32, null=True, verbose_name='Direct Line')),
                ('mobile', models.CharField(blank=True, max_length=32, null=True, verbose_name='Mobile Phone')),
                ('rating', models.CharField(blank=True, max_length=8, null=True, verbose_name='Rating')),
                ('status', models.CharField(blank=True, max_length=32, verbose_name='Status')),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Account')),
            ],
        ),
    ]