from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('musicians_portal', '0007_event_billed_hours'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='end_date',
            field=models.DateField(
                blank=True,
                null=True,
                help_text='Last day of multi-day events (leave blank for single-day)',
            ),
        ),
    ]
