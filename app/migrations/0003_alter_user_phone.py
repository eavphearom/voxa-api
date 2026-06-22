from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("app", "0002_folder_meeting"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="phone",
            field=models.CharField(blank=True, max_length=30, null=True, unique=True),
        ),
    ]
