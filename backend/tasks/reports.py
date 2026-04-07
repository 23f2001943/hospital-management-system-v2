from celery_worker import celery
from models import Doctor, Appointment
from datetime import datetime, date
from flask_mail import Message
from extensions import mail


@celery.task(name='tasks.reports.monthly_report')
def monthly_report():

    today = datetime.today()
    current_month = today.month
    current_year = today.year

    #  Month range (FIXED)
    start_date = date(current_year, current_month, 1)

    if current_month == 12:
        end_date = date(current_year + 1, 1, 1)
    else:
        end_date = date(current_year, current_month + 1, 1)

    doctors = Doctor.query.all()

    for doc in doctors:

        doctor_name = doc.user.name
        doctor_email = doc.user.email
        department = doc.department.name if doc.department else "N/A"
        phone = doc.contact_number or "N/A"

        #  Get this month's appointments
        appointments = Appointment.query.filter(
            Appointment.doctor_id == doc.id,
            Appointment.date >= start_date,
            Appointment.date < end_date
        ).all()

        total = len(appointments)
        completed = len([a for a in appointments if a.status == "Completed"])
        cancelled = len([a for a in appointments if a.status == "Cancelled"])

        #  Build HTML report
        html = f"""
        <h2>Monthly Report</h2>

        <h3>Doctor Info</h3>
        <p><b>Name:</b> {doctor_name}</p>
        <p><b>Department:</b> {department}</p>
        <p><b>Email:</b> {doctor_email}</p>
        <p><b>Phone:</b> {phone}</p>
        <p><b>Month:</b> {today.strftime('%B %Y')}</p>

        <h3>Appointment Summary</h3>
        <p><b>Total:</b> {total}</p>
        <p><b>Completed:</b> {completed}</p>
        <p><b>Cancelled:</b> {cancelled}</p>

        <h3>Detailed Report</h3>
        <table border="1" cellpadding="5" cellspacing="0">
        <tr>
            <th>Date</th>
            <th>Patient</th>
            <th>Email</th>
            <th>Status</th>
            <th>Diagnosis</th>
            <th>Prescription</th>
        </tr>
        """

        for a in appointments:
            diagnosis = a.treatment.diagnosis if a.treatment else "-"
            prescription = a.treatment.prescription if a.treatment else "-"

            html += f"""
            <tr>
                <td>{a.date}</td>
                <td>{a.patient.user.name}</td>
                <td>{a.patient.user.email}</td>
                <td>{a.status}</td>
                <td>{diagnosis}</td>
                <td>{prescription}</td>
            </tr>
            """

        html += "</table>"

        #  Send email
        try:
            msg = Message(
                subject="Monthly Report",
                recipients=[doctor_email],
                html=html
            )

            mail.send(msg)

            print(f"Report sent to Dr. {doctor_name}")

        except Exception as e:
            print(f"Failed for {doctor_name}: {e}")