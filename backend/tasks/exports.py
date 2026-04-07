from celery_worker import celery
from models import Appointment
from datetime import datetime
import csv
import os


@celery.task(name='tasks.exports.export_history')
def export_history(patient_id):

    # create folder if not exists
    folder = "exports"
    os.makedirs(folder, exist_ok=True)

    filename = f"{folder}/patient_{patient_id}_{int(datetime.now().timestamp())}.csv"

    appointments = Appointment.query.filter_by(
        patient_id=patient_id
    ).all()

    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)

        # header
        writer.writerow([
            "Date",
            "Doctor",
            "Department",
            "Status",
            "Diagnosis",
            "Prescription"
        ])

        for a in appointments:
            diagnosis = a.treatment.diagnosis if a.treatment else "-"
            prescription = a.treatment.prescription if a.treatment else "-"

            writer.writerow([
                a.date,
                a.doctor.user.name,
                a.doctor.department.name if a.doctor.department else "N/A",
                a.status,
                diagnosis,
                prescription
            ])

    print(f"CSV generated: {filename}")

    return filename