# Generated by Django 3.2.5 on 2021-11-23 07:50

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PdfForms',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Current_Date', models.DateField(max_length=100)),
                ('Company_Name', models.CharField(max_length=500)),
                ('Location', models.CharField(max_length=500)),
                ('Role', models.CharField(max_length=100)),
                ('job_Description', models.CharField(max_length=500)),
                ('Email_link', models.CharField(max_length=500)),
            ],
        ),
    ]
