import os
from uuid import uuid4
from datetime import datetime, timedelta
from PIL import Image
from flask import Flask, render_template, request, redirect, url_for, flash
from dotenv import load_dotenv

from models import db, Alumni, MediaAsset, Trainer, ValidationRequest, Reference, Voucher
from forms import StartForm, StatusForm, EducationForm, ReferencesForm

load_dotenv()

ALLOWED_EXTS = {"jpg", "jpeg", "png"}
MAX_FILES = 6

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.getenv("FLASK_SECRET_KEY", "dev-not-secure")

    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
        "SQLALCHEMY_DATABASE_URI",
        "sqlite:///" + os.path.join(basedir, "orane.db")
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    app.config["UPLOAD_FOLDER"] = os.path.join(basedir, "static", "uploads")
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

    db.init_app(app)

    @app.get("/")
    def index():
        return render_template("index.html")

    @app.route("/start", methods=["GET", "POST"])
    def start():
        form = StartForm()
        if form.validate_on_submit():
            existing = Alumni.query.filter(
                (Alumni.email == form.email.data) | (Alumni.mobile == form.mobile.data)
            ).first()
            alum = existing or Alumni(email=form.email.data, mobile=form.mobile.data)
            if not existing:
                db.session.add(alum)

            alum.first_name = form.first_name.data
            alum.last_name  = form.last_name.data
            alum.city       = form.city.data
            alum.country    = form.country.data
            alum.center     = form.center.data
            alum.program    = form.program.data
            alum.batch_code = form.batch_code.data
            alum.about_me   = form.about_me.data
            alum.skills     = form.skills.data
            alum.instagram_url = form.instagram_url.data
            alum.youtube_url   = form.youtube_url.data
            alum.linkedin_url  = form.linkedin_url.data
            alum.snapchat_url  = form.snapchat_url.data
            alum.consent_directory = bool(form.consent_directory.data)
            alum.status = "draft"

            files = request.files.getlist("showcase")
            if files:
                current_count = len(alum.media)
                room = max(0, MAX_FILES - current_count)
                for f in files[:room]:
                    if not f or f.filename == "":
                        continue
                    ext = f.filename.rsplit(".", 1)[-1].lower()
                    if ext not in ALLOWED_EXTS:
                        flash(f"Skipped {f.filename}: unsupported type", "warning")
                        continue
                    fn = f"{uuid4().hex}.{ext}"
                    dest = os.path.join(app.config["UPLOAD_FOLDER"], fn)
                    f.save(dest)
                    try:
                        with Image.open(dest) as im:
                            im = im.convert("RGB")
                            im.thumbnail((1200, 1200))
                            im.save(dest, quality=85)
                    except Exception:
                        flash(f"Image failed to process: {f.filename}", "danger")
                        try:
                            os.remove(dest)
                        except Exception:
                            pass
                        continue
                    db.session.add(MediaAsset(alumni=alum, file_path=f"uploads/{fn}"))

            db.session.commit()
            flash("Saved. Step 1 complete.", "success")
            return redirect(url_for("status", id=alum.id))

        return render_template("start.html", form=form)

    @app.route("/status", methods=["GET", "POST"])
    def status():
        alum_id = request.args.get("id", type=int)
        if not alum_id:
            flash("Missing profile reference. Please start again.", "danger")
            return redirect(url_for("start"))

        alum = Alumni.query.get_or_404(alum_id)
        form = StatusForm(obj=alum)

        if form.validate_on_submit():
            alum.current_status = form.current_status.data
            alum.employer_name  = form.employer_name.data
            alum.business_name  = form.business_name.data
            alum.business_url   = form.business_url.data
            alum.service_areas  = form.service_areas.data
            alum.started_ym     = form.started_ym.data
            alum.not_practicing_reason = form.not_practicing_reason.data
            intent = form.intent_to_return.data
            alum.intent_to_return = True if intent == "yes" else False if intent == "no" else None

            db.session.commit()
            flash("Status saved.", "success")
            return redirect(url_for("education", id=alum.id))

        return render_template("status.html", form=form, alum=alum)

    @app.route("/education", methods=["GET", "POST"])
    def education():
        alum_id = request.args.get("id", type=int)
        if not alum_id:
            flash("Missing profile reference. Please start again.", "danger")
            return redirect(url_for("start"))

        alum = Alumni.query.get_or_404(alum_id)
        form = EducationForm(obj=alum)

        if form.validate_on_submit():
            alum.course_name   = form.course_name.data
            alum.trainer_name  = form.trainer_name.data
            alum.completion_ym = form.completion_ym.data
            alum.reference_student_name  = form.reference_student_name.data
            alum.reference_student_phone = form.reference_student_phone.data

            db.session.commit()
            flash("Education saved.", "success")
            return redirect(url_for("references", id=alum.id))

        return render_template("education.html", form=form, alum=alum)

    @app.route("/references", methods=["GET", "POST"])
    def references():
        alum_id = request.args.get("id", type=int)
        if not alum_id:
            flash("Missing profile reference. Please start again.", "danger")
            return redirect(url_for("start"))

        alum = Alumni.query.get_or_404(alum_id)
        form = ReferencesForm()

        # build trainer choices each request
        trainers = Trainer.query.filter_by(is_public=True).all()
        form.trainer_id.choices = [(t.id, f"{t.first_name} {t.last_name} • {t.centers} • {t.programs}") for t in trainers]

        if form.validate_on_submit():
            # optional peer refs
            rows = []
            if form.peer1_name.data or form.peer1_mobile.data:
                rows.append(Reference(alumni_id=alum.id, name=form.peer1_name.data, mobile=form.peer1_mobile.data, ref_type="peer"))
            if form.peer2_name.data or form.peer2_mobile.data:
                rows.append(Reference(alumni_id=alum.id, name=form.peer2_name.data, mobile=form.peer2_mobile.data, ref_type="peer"))
            for r in rows:
                db.session.add(r)

            # one pending validation request
            if ValidationRequest.query.filter_by(alumni_id=alum.id, status="pending").first():
                flash("You already have a pending validation request.", "warning")
            else:
                db.session.add(ValidationRequest(alumni_id=alum.id, trainer_id=form.trainer_id.data, message=form.message.data or ""))
                alum.validation_status = "pending"

            db.session.commit()
            return redirect(url_for("done", id=alum.id))

        return render_template("references.html", form=form, alum=alum)

    @app.route("/done")
    def done():
        alum_id = request.args.get("id", type=int)
        if not alum_id:
            flash("Missing profile reference. Please start again.", "danger")
            return redirect(url_for("start"))

        alum = Alumni.query.get_or_404(alum_id)

        # issue voucher if not already
        if not alum.voucher:
            code = f"ORANE-ALUM-{alum.id:06d}"
            v = Voucher(code=code, alumni_id=alum.id, status="active", valid_until=datetime.utcnow() + timedelta(days=90))
            db.session.add(v)
            db.session.commit()

        return render_template("done.html", alum=alum)

    @app.cli.command("init-db")
    def init_db():
        db.create_all()
        print("Database tables created.")

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
