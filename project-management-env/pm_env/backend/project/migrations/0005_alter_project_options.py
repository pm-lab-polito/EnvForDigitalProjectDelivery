# Generated by Django 4.0.3 on 2022-05-02 20:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0004_remove_project_oa'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='project',
            options={'ordering': ('project_name',), 'permissions': (('add_project_charter', 'Can add project charter / to project charter'), ('change_project_charter', 'Can change project charter'), ('delete_project_charter', 'Can delete project charter'), ('view_project_charter', 'Can view project charter'))},
        ),
    ]