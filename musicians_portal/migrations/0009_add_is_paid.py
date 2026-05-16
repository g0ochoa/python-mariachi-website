from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('musicians_portal', '0008_event_end_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='is_paid',
            field=models.BooleanField(default=False, help_text='Marked by admin/lead once the client has paid the band'),
        ),
        migrations.AddField(
            model_name='musicianpay',
            name='is_paid',
            field=models.BooleanField(default=False, help_text='Set by admin/lead once this musician has been paid'),
        ),
    ]
