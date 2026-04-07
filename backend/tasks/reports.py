from celery_worker import celery
from models import Doctor, Appointment

@celery.task(name='tasks.reports.monthly_report')
def monthly_report():

    doctors = Doctor.query.all()

    for doc in doctors:
        appointments = Appointment.query.filter_by(
            doctor_id=doc.id
        ).all()

        print(f"Report for Dr. {doc.user.name} → {len(appointments)} appointments")