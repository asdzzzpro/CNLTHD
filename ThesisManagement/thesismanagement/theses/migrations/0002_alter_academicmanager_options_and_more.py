# Generated by Django 5.0.1 on 2024-02-29 12:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('theses', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='academicmanager',
            options={'verbose_name_plural': 'Giáo vụ'},
        ),
        migrations.AlterModelOptions(
            name='committee',
            options={'verbose_name_plural': 'Hội đồng bảo vệ khóa luận'},
        ),
        migrations.AlterModelOptions(
            name='criteria',
            options={'verbose_name_plural': 'Các tiêu chí chấm điểm'},
        ),
        migrations.AlterModelOptions(
            name='faculty',
            options={'verbose_name_plural': 'Khoa'},
        ),
        migrations.AlterModelOptions(
            name='lecturer',
            options={'verbose_name_plural': 'Giảng viên'},
        ),
        migrations.AlterModelOptions(
            name='major',
            options={'verbose_name_plural': 'Nghành'},
        ),
        migrations.AlterModelOptions(
            name='member',
            options={'verbose_name_plural': 'Thành viên'},
        ),
        migrations.AlterModelOptions(
            name='score',
            options={'verbose_name_plural': 'Điểm'},
        ),
        migrations.AlterModelOptions(
            name='student',
            options={'verbose_name_plural': 'Sinh viên'},
        ),
        migrations.AlterModelOptions(
            name='thesis',
            options={'verbose_name_plural': 'Khóa luận tốt nghiệp'},
        ),
        migrations.AlterUniqueTogether(
            name='student',
            unique_together={('user_ptr', 'thesis')},
        ),
    ]
