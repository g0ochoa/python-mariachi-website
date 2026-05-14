from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('musicians_portal', '0006_musicianpay'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='billed_hours',
            field=models.DecimalField(
                blank=True,
                decimal_places=2,
                help_text='Actual hours billed (overrides start/end time calculation)',
                max_digits=5,
                null=True,
            ),
        ),
    ]
