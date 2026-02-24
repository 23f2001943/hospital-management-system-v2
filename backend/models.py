from extensions import db
from datetime import datetime, timezone
from flask_security import UserMixin, RoleMixin


# base model
class BaseModel(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )
    updated_at = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc)
    )

class User(BaseModel, UserMixin):
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)

    fs_uniquifier = db.Column(db.String(255), unique=True, nullable=False)
    active = db.Column(db.Boolean(), default=True)

    roles = db.relationship(
        'Role',
        secondary='user_role',
        back_populates='users'
    )
    doctor = db.relationship(
    'Doctor',
    back_populates='user',
    uselist=False
)
    patient = db.relationship(
    'Patient',
    back_populates='user',
    uselist=False
)
class Role(BaseModel, RoleMixin):
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String(200))

    users = db.relationship(
        'User',
        secondary='user_role',
        back_populates='roles'
    )


class UserRole(BaseModel):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False)

class Department(BaseModel):
    name = db.Column(db.String(100), unique=True, nullable=False)
    code = db.Column(db.String(10), unique=True, nullable=False)
    description = db.Column(db.Text)
    floor = db.Column(db.String(20))
    is_active = db.Column(db.Boolean, default=True)

    doctors = db.relationship('Doctor', back_populates='department', lazy=True)
class Doctor(BaseModel):
    specialization_id = db.Column(db.Integer, db.ForeignKey('department.id'), nullable=False)

    qualification = db.Column(db.String(100))
    experience_years = db.Column(db.Integer)
    consultation_fee = db.Column(db.Numeric(10, 2))

    contact_number = db.Column(db.String(20))
    room_number = db.Column(db.String(20))

    availability = db.Column(db.JSON)
    is_active = db.Column(db.Boolean, default=True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', back_populates='doctor')

    appointments = db.relationship('Appointment', back_populates='doctor', lazy=True)
    department = db.relationship('Department', back_populates='doctors')


class Patient(BaseModel):
    date_of_birth = db.Column(db.Date)
    gender = db.Column(db.Enum('Male', 'Female', 'Other'))
    blood_group = db.Column(db.String(5))

    contact_number = db.Column(db.String(20))
    emergency_contact = db.Column(db.String(20))
    address = db.Column(db.Text)

    medical_notes = db.Column(db.Text)

    is_active = db.Column(db.Boolean, default=True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', back_populates='patient')

    appointments = db.relationship('Appointment', back_populates='patient', lazy=True)

class Appointment(BaseModel):
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)

    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)

    status = db.Column(
        db.Enum('Booked', 'Completed', 'Cancelled'),
        default='Booked'
    )

    treatment = db.relationship('Treatment', back_populates='appointment', uselist=False)
    doctor = db.relationship('Doctor', back_populates='appointments')
    patient = db.relationship('Patient', back_populates='appointments')

class Treatment(BaseModel):
    appointment_id = db.Column(db.Integer, db.ForeignKey('appointment.id'), nullable=False)
    diagnosis = db.Column(db.Text)
    prescription = db.Column(db.Text)
    notes = db.Column(db.Text)
    appointment = db.relationship(
    'Appointment',
    back_populates='treatment'
)
    
