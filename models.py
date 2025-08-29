from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Alumni(db.Model):
    __tablename__ = "alumni"
    id = db.Column(db.Integer, primary_key=True)

    # basic identity/contact
    first_name = db.Column(db.String(80))
    last_name  = db.Column(db.String(80))
    email      = db.Column(db.String(120), unique=True, nullable=False)
    mobile     = db.Column(db.String(20), unique=True, nullable=False)

    # location
    city       = db.Column(db.String(80))
    country    = db.Column(db.String(80))

    # orane training basics (from the Start step)
    center     = db.Column(db.String(120))
    program    = db.Column(db.String(120))
    batch_code = db.Column(db.String(40))

    # profile
    about_me   = db.Column(db.Text)
    skills     = db.Column(db.String(255))  # comma-separated for MVP

    # socials
    instagram_url = db.Column(db.String(255))
    youtube_url   = db.Column(db.String(255))
    linkedin_url  = db.Column(db.String(255))
    snapchat_url  = db.Column(db.String(255))

    # consent + workflow
    consent_directory = db.Column(db.Boolean, default=False)
    status     = db.Column(db.String(20), default="draft")  # draft|pending_validation|validated|rejected

    # current status (from Status step)
    current_status = db.Column(db.String(20))  # freelancer|salon|business|not_practicing
    employer_name  = db.Column(db.String(120))
    business_name  = db.Column(db.String(120))
    business_url   = db.Column(db.String(255))
    service_areas  = db.Column(db.String(255))
    started_ym     = db.Column(db.String(7))   # YYYY-MM for current role
    not_practicing_reason = db.Column(db.String(120))
    intent_to_return = db.Column(db.Boolean)

    # education/training (from Education step)
    course_name   = db.Column(db.String(120))
    trainer_name  = db.Column(db.String(120))
    completion_ym = db.Column(db.String(7))    # YYYY-MM
    reference_student_name  = db.Column(db.String(120))
    reference_student_phone = db.Column(db.String(20))

    # validation state
    validation_status = db.Column(db.String(20), default="pending")  # pending|validated|rejected
    validated_by_trainer_id = db.Column(db.Integer, db.ForeignKey("trainers.id"))

    # timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # relations
    media = db.relationship("MediaAsset", backref="alumni", cascade="all, delete-orphan")
    references = db.relationship("Reference", backref="alumni", cascade="all, delete-orphan")
    voucher = db.relationship("Voucher", backref="alumni", uselist=False)

class MediaAsset(db.Model):
    __tablename__ = "media_assets"
    id = db.Column(db.Integer, primary_key=True)
    alumni_id = db.Column(db.Integer, db.ForeignKey("alumni.id"), nullable=False)
    file_path = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Trainer(db.Model):
    __tablename__ = "trainers"
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80), nullable=False)
    last_name  = db.Column(db.String(80), nullable=False)
    email      = db.Column(db.String(120), unique=True)
    mobile     = db.Column(db.String(20), unique=True)
    centers    = db.Column(db.String(255))   # comma-separated
    programs   = db.Column(db.String(255))   # comma-separated
    languages  = db.Column(db.String(255))   # comma-separated
    is_public  = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    approvals = db.relationship("ValidationRequest", backref="trainer")

class ValidationRequest(db.Model):
    __tablename__ = "validation_requests"
    id = db.Column(db.Integer, primary_key=True)
    alumni_id = db.Column(db.Integer, db.ForeignKey("alumni.id"), nullable=False)
    trainer_id = db.Column(db.Integer, db.ForeignKey("trainers.id"), nullable=False)
    message = db.Column(db.String(200))
    status = db.Column(db.String(20), default="pending")  # pending|approved|declined
    acted_at = db.Column(db.DateTime)
    trainer_note = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Reference(db.Model):
    __tablename__ = "references"
    id = db.Column(db.Integer, primary_key=True)
    alumni_id = db.Column(db.Integer, db.ForeignKey("alumni.id"), nullable=False)
    name = db.Column(db.String(120))
    mobile = db.Column(db.String(20))
    ref_type = db.Column(db.String(20), default="peer")  # peer|trainer
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Voucher(db.Model):
    __tablename__ = "vouchers"
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(40), unique=True, nullable=False)
    alumni_id = db.Column(db.Integer, db.ForeignKey("alumni.id"), unique=True, nullable=False)
    status = db.Column(db.String(20), default="active")  # active|redeemed|expired
    valid_until = db.Column(db.DateTime)
    redeemed_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
