from flask_wtf import FlaskForm
from wtforms import (
    StringField, TextAreaField, BooleanField, SelectField,
    MultipleFileField, RadioField
)
from wtforms.validators import (
    DataRequired, Email, Length, Optional, Regexp, URL
)

# Choices for Start step
CENTER_CHOICES = [
    ("", "Select center"),
    ("Delhi", "Delhi"),
    ("Mumbai", "Mumbai"),
    ("Chandigarh", "Chandigarh"),
    ("Bengaluru", "Bengaluru"),
]

PROGRAM_CHOICES = [
    ("", "Select program"),
    ("Beauty Therapy", "Beauty Therapy"),
    ("Makeup Artistry", "Makeup Artistry"),
    ("Hair Styling", "Hair Styling"),
    ("Nail Art", "Nail Art"),
]

class StartForm(FlaskForm):
    first_name = StringField("First name", validators=[Optional(), Length(max=80)])
    last_name  = StringField("Last name", validators=[Optional(), Length(max=80)])
    email      = StringField("Email", validators=[DataRequired(), Email(), Length(max=120)])
    mobile     = StringField("Mobile", validators=[DataRequired(), Regexp(r"^[0-9]{10,15}$", message="Enter 10–15 digits")])

    city       = StringField("City", validators=[Optional(), Length(max=80)])
    country    = StringField("Country", validators=[Optional(), Length(max=80)])

    center     = SelectField("Center attended", choices=CENTER_CHOICES, validators=[DataRequired()])
    program    = SelectField("Program", choices=PROGRAM_CHOICES, validators=[DataRequired()])
    batch_code = StringField("Batch / Month & Year", validators=[Optional(), Length(max=40)])

    about_me   = TextAreaField("Brief description", validators=[Length(max=1000)])
    skills     = StringField("What you’re good at (comma-separated)", validators=[Optional(), Length(max=255)])

    instagram_url = StringField("Instagram", validators=[Optional(), URL(require_tld=False)])
    youtube_url   = StringField("YouTube", validators=[Optional(), URL(require_tld=False)])
    linkedin_url  = StringField("LinkedIn", validators=[Optional(), URL(require_tld=False)])
    snapchat_url  = StringField("Snapchat", validators=[Optional(), URL(require_tld=False)])

    showcase      = MultipleFileField("Showcase images (up to 6)")
    consent_directory = BooleanField("I agree to be listed in the directory", validators=[DataRequired(message="Consent is required")])

# Choices for Status step
NOT_PRACTICING_REASONS = [
    ("", "Select reason"),
    ("career_change", "Career change"),
    ("family_break", "Family/personal break"),
    ("studies", "Further studies"),
    ("other", "Other"),
]

class StatusForm(FlaskForm):
    current_status = RadioField(
        "What are you doing currently?",
        choices=[
            ("freelancer", "Freelancer"),
            ("salon", "Working with a salon"),
            ("business", "Own business"),
            ("not_practicing", "Not practicing"),
        ],
        validators=[DataRequired(message="Select one option")]
    )

    employer_name = StringField("Salon name", validators=[Optional(), Length(max=120)])
    business_name = StringField("Business name", validators=[Optional(), Length(max=120)])
    business_url  = StringField("Business Instagram/Website", validators=[Optional(), URL(require_tld=False)])
    service_areas = StringField("Service areas (city/localities)", validators=[Optional(), Length(max=255)])
    started_ym    = StringField("Start month/year (YYYY-MM)", validators=[Optional(), Regexp(r"^\d{4}-\d{2}$", message="Use YYYY-MM")])
    not_practicing_reason = SelectField("Reason", choices=NOT_PRACTICING_REASONS, validators=[Optional()])
    intent_to_return = RadioField("Plan to return later?", choices=[("yes","Yes"),("no","No")], validators=[Optional()])

class EducationForm(FlaskForm):
    course_name   = StringField("Course name", validators=[DataRequired(), Length(max=120)])
    trainer_name  = StringField("Trainer name", validators=[Optional(), Length(max=120)])
    completion_ym = StringField("Completion date (YYYY-MM)", validators=[Optional(), Regexp(r"^\d{4}-\d{2}$", message="Use YYYY-MM")])
    reference_student_name  = StringField("Reference student name", validators=[Optional(), Length(max=120)])
    reference_student_phone = StringField("Reference student phone", validators=[Optional(), Length(max=20)])

class ReferencesForm(FlaskForm):
    peer1_name   = StringField("Peer name (optional)",  validators=[Optional(), Length(max=120)])
    peer1_mobile = StringField("Peer mobile",           validators=[Optional(), Regexp(r"^[0-9]{10,15}$")])
    peer2_name   = StringField("Peer name (optional)",  validators=[Optional(), Length(max=120)])
    peer2_mobile = StringField("Peer mobile",           validators=[Optional(), Regexp(r"^[0-9]{10,15}$")])

    trainer_id   = SelectField("Select a trainer to request validation", choices=[], coerce=int, validators=[DataRequired(message="Pick a trainer")])
    message      = StringField("Message to trainer (optional)", validators=[Optional(), Length(max=200)])
