from celery_worker import celery
from models import Appointment
from datetime import date
from flask_mail import Message
from extensions import mail


@celery.task(name='tasks.reminders.daily_reminder')
def daily_reminder():

    today = date.today()

    appointments = Appointment.query.filter_by(
        date=today,
        status='Booked'
    ).all()

    for appt in appointments:

        patient_email = appt.patient.user.email
        patient_name = appt.patient.user.name
        doctor_name = appt.doctor.user.name

        subject = "Appointment Reminder"

        body = f"""
Hello {patient_name},

This is a reminder that you have an appointment TODAY.

Doctor: Dr. {doctor_name}
Date: {today}

Please be on time.

Regards,
Hospital Team
        """

        try:
            msg = Message(
                subject=subject,
                recipients=[patient_email],
                body=body
            )

            mail.send(msg)

            print(f"Email sent to {patient_email}")

        except Exception as e:
            print(f"Failed to send email: {e}")