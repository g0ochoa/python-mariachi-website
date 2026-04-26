from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('musicians_portal', '0002_event_eventattendance'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='google_event_id',
            field=models.CharField(blank=True, db_index=True, max_length=300),
        ),
    ]
