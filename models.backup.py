from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Alumni(db.Model):
    __tablename__ = "alumni"
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80))
    last_name  = db.Column(db.String(80))
    email      = db.Column(db.String(120), unique=True, nullable=False)
    mobile     = db.Column(db.String(20), unique=True, nullable=False)

    city       = db.Column(db.String(80))
    country    = db.Column(db.String(80))

    center     = db.Column(db.String(120))
    program    = db.Column(db.String(120))
    batch_code = db.Column(db.String(40))

    # education/completion
    start_ym   = db.Column(db.String(7))   # YYYY-MM
    end_ym     = db.Column(db.String(7))   # YYYY-MM
    enrollment_id = db.Column(db.String(120))
    certificate_path = db.Column(db.String(255))

    about_me   = db.Column(db.Text)
    skills     = db.Column(db.String(255))  # comma-separated for MVP

    instagram_url = db.Column(db.String(255))
    youtube_url   = db.Column(db.String(255))
    linkedin_url  = db.Column(db.String(255))
    snapchat_url  = db.Column(db.String(255))

    consent_directory = db.Column(db.Boolean, default=False)
    status     = db.Column(db.String(20), default="draft")  # draft|pending_validation|validated|rejected

    # current status
    current_status = db.Column(db.String(20))  # freelancer|salon|business|not_practicing
    employer_name  = db.Column(db.String(120))
    business_name  = db.Column(db.String(120))
    business_url   = db.Column(db.String(255))
    service_areas  = db.Column(db.String(255))
    started_ym     = db.Column(db.String(7))    # YYYY-MM for current role
    not_practicing_reason = db.Column(db.String(120))
    intent_to_return = db.Column(db.Boolean)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    media = db.relationship("MediaAsset", backref="alumni", cascade="all, delete-orphan")

class MediaAsset(db.Model):
    __tablename__ = "media_assets"
    id = db.Column(db.Integer, primary_key=True)
    alumni_id = db.Column(db.Integer, db.ForeignKey("alumni.id"), nullable=False)
    file_path = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
