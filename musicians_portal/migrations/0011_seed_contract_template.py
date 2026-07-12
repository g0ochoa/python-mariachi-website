# Seeds the default bilingual contract terms. Edit the live wording anytime in
# django-admin → Contract templates; contracts snapshot the terms at creation,
# so edits never change already-sent contracts.

from django.db import migrations

STARTER_TERMS_EN = """\
1. BOOKING & DEPOSIT
A non-refundable deposit in the amount shown in the Event Details above is
required to reserve the performance date. The date is not reserved until the
deposit is received. The deposit is applied toward the total price.

2. PAYMENT
The remaining balance is due in full before the start of the performance.
Accepted payment methods: cash, Zelle, or Venmo, unless otherwise agreed in
writing. If the balance is not paid before the scheduled start time, the band
is not obligated to perform and the deposit is forfeited.

3. PERFORMANCE TIME & OVERTIME
The band will perform during the hours listed in the Event Details above.
Additional time may be requested on the day of the event, subject to the
band's availability, at the overtime rate shown above, billed in 30-minute
increments and payable the same day before the extended time begins. The band
will arrive with enough time to be ready to play at the scheduled start time.

4. CANCELLATION & RESCHEDULING
If the client cancels, the deposit is forfeited. If the client gives at least
14 days' written notice, the deposit may be transferred one time to a new
date within 12 months, subject to the band's availability. If the band
cancels for any reason other than those described in Section 7, all payments
received, including the deposit, will be refunded in full.

5. OUTDOOR EVENTS & WEATHER
For outdoor performances the client will provide a shaded or covered, dry,
level area for the musicians. Instruments cannot be exposed to rain, direct
extended sunlight, or temperatures below 40°F (4°C) or above 100°F (38°C).
In case of rain, lightning, or other unsafe weather, the client will provide
a covered or indoor alternative space. If no safe performing area is
available, the band's obligations are considered fulfilled and no refund is
owed.

6. TRAVEL
Performances outside the band's home area may include a travel fee, agreed
upon in advance and included in the total price shown above.

7. FORCE MAJEURE
Neither party is liable for failure to perform caused by events beyond its
reasonable control, including natural disasters, severe weather, government
orders, or serious illness or injury. The band will make reasonable efforts
to provide substitute musicians or to reschedule. If performance is
impossible, the deposit will be refunded and neither party will owe anything
further.

8. ELECTRONIC ACCEPTANCE
By typing your full name and checking the acceptance box on this page, you
agree that this constitutes your electronic signature and that this agreement
is legally binding, with the same effect as a handwritten signature.
"""

STARTER_TERMS_ES = """\
1. RESERVACIÓN Y DEPÓSITO
Se requiere un depósito no reembolsable, por la cantidad indicada en los
Detalles del Evento arriba, para reservar la fecha de la presentación. La
fecha no queda reservada hasta recibir el depósito. El depósito se aplica al
precio total.

2. PAGO
El saldo restante debe pagarse en su totalidad antes del inicio de la
presentación. Métodos de pago aceptados: efectivo, Zelle o Venmo, salvo
acuerdo por escrito. Si el saldo no se paga antes de la hora de inicio
programada, el grupo no está obligado a tocar y el depósito no será
reembolsado.

3. HORARIO Y TIEMPO EXTRA
El grupo tocará durante el horario indicado en los Detalles del Evento. Se
puede solicitar tiempo adicional el día del evento, sujeto a la
disponibilidad del grupo, a la tarifa de tiempo extra indicada arriba,
cobrado en incrementos de 30 minutos y pagadero el mismo día antes de
comenzar el tiempo adicional. El grupo llegará con suficiente anticipación
para estar listo a la hora de inicio programada.

4. CANCELACIÓN Y CAMBIO DE FECHA
Si el cliente cancela, el depósito no será reembolsado. Si el cliente avisa
por escrito con al menos 14 días de anticipación, el depósito podrá
transferirse una sola vez a una nueva fecha dentro de los próximos 12 meses,
sujeto a la disponibilidad del grupo. Si el grupo cancela por cualquier
motivo distinto a los descritos en la Sección 7, se reembolsará la totalidad
de los pagos recibidos, incluido el depósito.

5. EVENTOS AL AIRE LIBRE Y CLIMA
Para presentaciones al aire libre, el cliente proporcionará un área seca,
nivelada y con sombra o techo para los músicos. Los instrumentos no pueden
exponerse a la lluvia, al sol directo por tiempo prolongado, ni a
temperaturas menores de 40°F (4°C) o mayores de 100°F (38°C). En caso de
lluvia, relámpagos u otro clima peligroso, el cliente proporcionará un
espacio techado o interior. Si no hay un área segura disponible, las
obligaciones del grupo se considerarán cumplidas y no se deberá ningún
reembolso.

6. TRASLADO
Las presentaciones fuera del área local del grupo pueden incluir un cargo por
traslado, acordado con anticipación e incluido en el precio total indicado
arriba.

7. FUERZA MAYOR
Ninguna de las partes será responsable por incumplimiento causado por
circunstancias fuera de su control razonable, incluyendo desastres naturales,
clima severo, órdenes gubernamentales, o enfermedad o lesión grave. El grupo
hará esfuerzos razonables por conseguir músicos sustitutos o cambiar la
fecha. Si la presentación resulta imposible, se reembolsará el depósito y
ninguna de las partes deberá nada más.

8. ACEPTACIÓN ELECTRÓNICA
Al escribir su nombre completo y marcar la casilla de aceptación en esta
página, usted acepta que esto constituye su firma electrónica y que este
acuerdo es legalmente válido, con el mismo efecto que una firma manuscrita.
"""


def seed_template(apps, schema_editor):
    ContractTemplate = apps.get_model('musicians_portal', 'ContractTemplate')
    ContractTemplate.objects.get_or_create(
        name='Standard Gig Contract',
        defaults={
            'terms_en': STARTER_TERMS_EN,
            'terms_es': STARTER_TERMS_ES,
            'is_active': True,
        },
    )


def remove_template(apps, schema_editor):
    ContractTemplate = apps.get_model('musicians_portal', 'ContractTemplate')
    ContractTemplate.objects.filter(name='Standard Gig Contract').delete()


class Migration(migrations.Migration):

    dependencies = [
        ('musicians_portal', '0010_contract_and_client_contact'),
    ]

    operations = [
        migrations.RunPython(seed_template, remove_template),
    ]
