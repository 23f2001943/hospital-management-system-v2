import random
from faker import Faker
from datetime import date, time
from app import app
from extensions import db
from models import User, Role, Doctor, Patient, Appointment, Treatment
from flask_security.datastore import SQLAlchemyUserDatastore
from flask_security.utils import hash_password
import uuid

fake = Faker()

with app.app_context():

    datastore = SQLAlchemyUserDatastore(db, User, Role)

    doctor_role = datastore.find_role("doctor")
    patient_role = datastore.find_role("patient")

    # ---- CREATE DOCTORS ----
    for _ in range(10):
        user = datastore.create_user(
        name=fake.name(),
        email=fake.unique.email(),
        password=hash_password("password"),
        fs_uniquifier=str(uuid.uuid4()),
        active=True
    )

    datastore.add_role_to_user(user, doctor_role)

    db.session.flush()   

    doctor = Doctor(
        user_id=user.id,
        specialization_id=1,
        experience_years=random.randint(1, 20),
        consultation_fee=random.randint(300, 1000),
        contact_number=fake.phone_number(),
        is_active=True
    )

    db.session.add(doctor)

    # ---- CREATE PATIENTS ----
    for _ in range(30):
        user = datastore.create_user(
            name=fake.name(),
            email=fake.unique.email(),
            password=hash_password("password"),
            fs_uniquifier=str(uuid.uuid4()),
            active=True
        )

        datastore.add_role_to_user(user, patient_role)

        db.session.flush()

        patient = Patient(
            user_id=user.id,
            contact_number=fake.phone_number(),
            blood_group=random.choice(["A+", "B+", "O+", "AB+"]),
            is_active=True
        )

        db.session.add(patient)

    db.session.commit()

    doctors = Doctor.query.all()
    patients = Patient.query.all()

    
        # ---- CREATE APPOINTMENTS ----
    for _ in range(100):

        status = random.choice(["Booked", "Completed", "Cancelled"])

        appointment = Appointment(
            doctor_id=random.choice(doctors).id,
            patient_id=random.choice(patients).id,
            date=fake.date_this_year(),
            time=time(hour=random.randint(9, 17)),
            status=status
        )

        db.session.add(appointment)
        db.session.flush()   # get appointment.id

        # create treatment only if appointment completed
        if status == "Completed":

            treatment = Treatment(
                appointment_id=appointment.id,
                diagnosis=fake.sentence(nb_words=4),
                prescription=fake.sentence(nb_words=5),
                notes=fake.sentence(nb_words=6)
            )

            db.session.add(treatment)
    print("Database seeded successfully.")