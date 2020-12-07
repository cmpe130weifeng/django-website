# Generated by Django 3.1.2 on 2020-12-02 17:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('employee_page', '0003_delete_profile'),
        ('homepage', '0012_auto_20201202_0954'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='emp_no',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, to='employee_page.employees'),
            preserve_default=False,
        ),
    ]