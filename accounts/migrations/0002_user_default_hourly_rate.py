from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='default_hourly_rate',
            field=models.DecimalField(
                blank=True,
                decimal_places=2,
                help_text='Default hourly pay rate for this musician (used in auto-calculate)',
                max_digits=6,
                null=True,
            ),
        ),
    ]
