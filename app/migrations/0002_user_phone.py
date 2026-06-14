# Generated manually for adding phone to users.

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="phone",
            field=models.CharField(default="", max_length=30, unique=True),
            preserve_default=False,
        ),
    ]
