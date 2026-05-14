from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_user_default_hourly_rate'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_test_account',
            field=models.BooleanField(
                default=False,
                help_text='Test/demo accounts are hidden from pay entry and pay summary',
            ),
        ),
        migrations.AddField(
            model_name='user',
            name='active_from',
            field=models.DateField(
                blank=True,
                null=True,
                help_text='Date this musician joined the band (leave blank = always active from start)',
            ),
        ),
        migrations.AddField(
            model_name='user',
            name='active_until',
            field=models.DateField(
                blank=True,
                null=True,
                help_text='Last date this musician was active (leave blank = still active)',
            ),
        ),
    ]
