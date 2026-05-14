from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('musicians_portal', '0004_gig'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='rate_per_hour',
            field=models.DecimalField(
                blank=True,
                decimal_places=2,
                help_text='Rate charged per hour (admin/lead only)',
                max_digits=8,
                null=True,
            ),
        ),
        migrations.AddField(
            model_name='event',
            name='total_charged',
            field=models.DecimalField(
                blank=True,
                decimal_places=2,
                help_text='Total amount charged to client (admin/lead only)',
                max_digits=10,
                null=True,
            ),
        ),
    ]
