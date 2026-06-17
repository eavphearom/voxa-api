import django.db.models.deletion
from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_chat_type_meeting_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChatMessageAttachment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('created_uid', models.BigIntegerField(blank=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('updated_uid', models.BigIntegerField(blank=True, null=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('deleted_uid', models.BigIntegerField(blank=True, null=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('attachment_type', models.CharField(choices=[('image', 'image'), ('file', 'file'), ('audio', 'audio'), ('video', 'video')], max_length=20)),
                ('file_name', models.CharField(max_length=255)),
                ('file_path', models.CharField(max_length=1000)),
                ('file_size', models.BigIntegerField()),
                ('chat_message', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attachments', to='app.chatmessage')),
            ],
            options={
                'db_table': 'chat_message_attachments',
            },
        ),
    ]
