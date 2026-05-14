import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('musicians_portal', '0005_event_add_financials'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='MusicianPay',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, help_text='Amount paid to this musician for this event', max_digits=8)),
                ('notes', models.CharField(blank=True, help_text='Optional note (e.g. cash, Venmo, etc.)', max_length=200)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(
                    null=True,
                    on_delete=django.db.models.deletion.SET_NULL,
                    related_name='pay_records_created',
                    to=settings.AUTH_USER_MODEL,
                )),
                ('event', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='musician_pays',
                    to='musicians_portal.event',
                )),
                ('musician', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='pay_records',
                    to=settings.AUTH_USER_MODEL,
                )),
            ],
            options={
                'ordering': ['event__date', 'musician__first_name'],
                'unique_together': {('event', 'musician')},
            },
        ),
    ]
