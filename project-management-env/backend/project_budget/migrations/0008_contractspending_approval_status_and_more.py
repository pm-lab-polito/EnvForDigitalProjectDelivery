# Generated by Django 4.0.3 on 2022-05-20 13:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project_budget', '0007_alter_resourcespending_approval_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='contractspending',
            name='approval_status',
            field=models.CharField(choices=[('approved', 'approved'), ('denied', 'denied')], default='approved', max_length=9),
        ),
        migrations.AlterField(
            model_name='resourcespending',
            name='approval_status',
            field=models.CharField(choices=[('approved', 'approved'), ('denied', 'denied')], default='approved', max_length=9),
        ),
    ]