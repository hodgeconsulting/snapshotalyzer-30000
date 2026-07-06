"""Sacramental records application for a parish of the
Orthodox Church in America.

Records Baptisms/Chrismations, Receptions into the Church, Marriages,
and Funerals; prints certificates and register pages for permanent
record keeping in physical binders.

Run:  python3 app.py   then open http://localhost:5000
"""

import csv
import io
import json
import os
import sqlite3
from datetime import datetime

from flask import (Flask, abort, flash, g, redirect, render_template,
                   request, url_for, Response)

from config import (SACRAMENTS, SETTINGS_FIELDS, REGISTER_FIELDS,
                    all_field_keys, field_map)

APP_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.environ.get("SACRAMENTS_DB",
                         os.path.join(APP_DIR, "sacraments.db"))

app = Flask(__name__)
app.secret_key = os.environ.get("SACRAMENTS_SECRET_KEY", "parish-records")


# ---------------------------------------------------------------- database

def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DB_PATH)
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys = ON")
    return g.db


@app.teardown_appcontext
def close_db(exc):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    db = sqlite3.connect(DB_PATH)
    db.executescript("""
        CREATE TABLE IF NOT EXISTS records (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            sacrament     TEXT NOT NULL,
            record_number TEXT DEFAULT '',
            volume        TEXT DEFAULT '',
            page          TEXT DEFAULT '',
            primary_date  TEXT DEFAULT '',
            display_name  TEXT DEFAULT '',
            data          TEXT NOT NULL,
            created_at    TEXT NOT NULL,
            updated_at    TEXT NOT NULL
        );
        CREATE INDEX IF NOT EXISTS idx_records_sacrament
            ON records (sacrament, primary_date);
        CREATE TABLE IF NOT EXISTS settings (
            key   TEXT PRIMARY KEY,
            value TEXT
        );
    """)
    db.commit()
    db.close()


def get_settings():
    rows = get_db().execute("SELECT key, value FROM settings").fetchall()
    return {row["key"]: row["value"] for row in rows}


# ---------------------------------------------------------------- helpers

def valid_sacrament(stype):
    if stype not in SACRAMENTS:
        abort(404)
    return SACRAMENTS[stype]


def compute_display_name(stype, data):
    if stype == "marriage":
        groom = data.get("groom_name", "").strip()
        bride = data.get("bride_name", "").strip()
        return f"{groom} and {bride}".strip()
    return data.get("full_name", "").strip()


def parse_form(stype):
    """Extract, trim, and validate submitted fields.

    Returns (data, register, errors) where data holds the sacrament
    fields, register holds the register-book reference fields, and
    errors is a list of validation messages.
    """
    fmap = field_map(stype)
    data, errors = {}, []
    for key, field in fmap.items():
        value = request.form.get(key, "").strip()
        if field.get("required") and not value:
            errors.append(f"{field['label']} is required.")
        if value and field["type"] == "date":
            try:
                datetime.strptime(value, "%Y-%m-%d")
            except ValueError:
                errors.append(f"{field['label']} must be a valid date.")
        if value and field["type"] == "select" \
                and value not in field["options"]:
            errors.append(f"{field['label']} has an invalid choice.")
        data[key] = value
    register = {f["key"]: request.form.get(f["key"], "").strip()
                for f in REGISTER_FIELDS}
    return data, register, errors


def suggest_record_number(stype):
    """Suggest the next sequential register entry number."""
    rows = get_db().execute(
        "SELECT record_number FROM records WHERE sacrament = ?",
        (stype,)).fetchall()
    numbers = [int(r["record_number"]) for r in rows
               if r["record_number"].isdigit()]
    return str(max(numbers) + 1) if numbers else "1"


def fetch_record(stype, record_id):
    row = get_db().execute(
        "SELECT * FROM records WHERE id = ? AND sacrament = ?",
        (record_id, stype)).fetchone()
    if row is None:
        abort(404)
    record = dict(row)
    record["data"] = json.loads(row["data"])
    return record


# ---------------------------------------------------------- template utils

@app.template_filter("longdate")
def longdate(value):
    """Render an ISO date as e.g. 'January 6, 2026' for certificates."""
    if not value:
        return ""
    try:
        d = datetime.strptime(value, "%Y-%m-%d")
        return f"{d:%B} {d.day}, {d.year}"
    except ValueError:
        return value


@app.context_processor
def inject_globals():
    return {
        "SACRAMENTS": SACRAMENTS,
        "REGISTER_FIELDS": REGISTER_FIELDS,
        "settings": get_settings(),
        "today": datetime.now().strftime("%Y-%m-%d"),
    }


# ------------------------------------------------------------------ routes

@app.route("/")
def index():
    db = get_db()
    counts = {stype: db.execute(
        "SELECT COUNT(*) AS n FROM records WHERE sacrament = ?",
        (stype,)).fetchone()["n"] for stype in SACRAMENTS}
    recent = db.execute(
        "SELECT * FROM records ORDER BY updated_at DESC LIMIT 10").fetchall()
    return render_template("index.html", counts=counts, recent=recent)


@app.route("/records/<stype>")
def record_list(stype):
    sac = valid_sacrament(stype)
    q = request.args.get("q", "").strip()
    sql = "SELECT * FROM records WHERE sacrament = ?"
    params = [stype]
    if q:
        sql += " AND (display_name LIKE ? OR data LIKE ?)"
        params += [f"%{q}%", f"%{q}%"]
    sql += " ORDER BY primary_date DESC, id DESC"
    rows = get_db().execute(sql, params).fetchall()
    records = []
    for row in rows:
        record = dict(row)
        record["data"] = json.loads(row["data"])
        records.append(record)
    return render_template("list.html", stype=stype, sac=sac,
                           records=records, q=q)


@app.route("/records/<stype>/new", methods=["GET", "POST"])
def record_new(stype):
    sac = valid_sacrament(stype)
    if request.method == "POST":
        data, register, errors = parse_form(stype)
        if errors:
            for e in errors:
                flash(e, "error")
            return render_template("form.html", stype=stype, sac=sac,
                                   data=data, register=register,
                                   record=None), 400
        now = datetime.now().isoformat(timespec="seconds")
        db = get_db()
        cur = db.execute(
            """INSERT INTO records (sacrament, record_number, volume, page,
                   primary_date, display_name, data, created_at, updated_at)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (stype, register["record_number"], register["volume"],
             register["page"], data.get(sac["date_field"], ""),
             compute_display_name(stype, data), json.dumps(data), now, now))
        db.commit()
        flash(f"{sac['singular']} record saved.", "ok")
        return redirect(url_for("record_detail", stype=stype,
                                record_id=cur.lastrowid))
    register = {"record_number": suggest_record_number(stype),
                "volume": "", "page": ""}
    return render_template("form.html", stype=stype, sac=sac,
                           data={}, register=register, record=None)


@app.route("/records/<stype>/<int:record_id>")
def record_detail(stype, record_id):
    sac = valid_sacrament(stype)
    record = fetch_record(stype, record_id)
    return render_template("detail.html", stype=stype, sac=sac,
                           record=record, fmap=field_map(stype))


@app.route("/records/<stype>/<int:record_id>/edit", methods=["GET", "POST"])
def record_edit(stype, record_id):
    sac = valid_sacrament(stype)
    record = fetch_record(stype, record_id)
    if request.method == "POST":
        data, register, errors = parse_form(stype)
        if errors:
            for e in errors:
                flash(e, "error")
            return render_template("form.html", stype=stype, sac=sac,
                                   data=data, register=register,
                                   record=record), 400
        now = datetime.now().isoformat(timespec="seconds")
        db = get_db()
        db.execute(
            """UPDATE records SET record_number = ?, volume = ?, page = ?,
                   primary_date = ?, display_name = ?, data = ?,
                   updated_at = ?
               WHERE id = ?""",
            (register["record_number"], register["volume"], register["page"],
             data.get(sac["date_field"], ""),
             compute_display_name(stype, data), json.dumps(data), now,
             record_id))
        db.commit()
        flash("Record updated.", "ok")
        return redirect(url_for("record_detail", stype=stype,
                                record_id=record_id))
    register = {f["key"]: record[f["key"]] for f in REGISTER_FIELDS}
    return render_template("form.html", stype=stype, sac=sac,
                           data=record["data"], register=register,
                           record=record)


@app.route("/records/<stype>/<int:record_id>/delete", methods=["POST"])
def record_delete(stype, record_id):
    valid_sacrament(stype)
    fetch_record(stype, record_id)
    db = get_db()
    db.execute("DELETE FROM records WHERE id = ?", (record_id,))
    db.commit()
    flash("Record deleted.", "ok")
    return redirect(url_for("record_list", stype=stype))


@app.route("/records/<stype>/<int:record_id>/certificate")
def certificate(stype, record_id):
    sac = valid_sacrament(stype)
    record = fetch_record(stype, record_id)
    return render_template(f"certificate_{stype}.html", stype=stype,
                           sac=sac, record=record, data=record["data"])


@app.route("/records/<stype>/register")
def register_print(stype):
    sac = valid_sacrament(stype)
    rows = get_db().execute(
        "SELECT * FROM records WHERE sacrament = ?"
        " ORDER BY primary_date, id", (stype,)).fetchall()
    records = []
    for row in rows:
        record = dict(row)
        record["data"] = json.loads(row["data"])
        records.append(record)
    return render_template("register_print.html", stype=stype, sac=sac,
                           records=records, fmap=field_map(stype))


@app.route("/records/<stype>/export.csv")
def export_csv(stype):
    sac = valid_sacrament(stype)
    keys = all_field_keys(stype)
    fmap = field_map(stype)
    rows = get_db().execute(
        "SELECT * FROM records WHERE sacrament = ?"
        " ORDER BY primary_date, id", (stype,)).fetchall()
    out = io.StringIO()
    writer = csv.writer(out)
    writer.writerow([f["label"] for f in REGISTER_FIELDS] +
                    [fmap[k]["label"] for k in keys])
    for row in rows:
        data = json.loads(row["data"])
        writer.writerow([row[f["key"]] for f in REGISTER_FIELDS] +
                        [data.get(k, "") for k in keys])
    filename = f"{stype}-register.csv"
    return Response(out.getvalue(), mimetype="text/csv",
                    headers={"Content-Disposition":
                             f"attachment; filename={filename}"})


@app.route("/settings", methods=["GET", "POST"])
def settings_page():
    if request.method == "POST":
        db = get_db()
        for field in SETTINGS_FIELDS:
            value = request.form.get(field["key"], "").strip()
            db.execute(
                "INSERT INTO settings (key, value) VALUES (?, ?)"
                " ON CONFLICT(key) DO UPDATE SET value = excluded.value",
                (field["key"], value))
        db.commit()
        flash("Parish settings saved.", "ok")
        return redirect(url_for("settings_page"))
    return render_template("settings.html", fields=SETTINGS_FIELDS)


init_db()

if __name__ == "__main__":
    app.run(debug=True, port=int(os.environ.get("PORT", 5000)))
