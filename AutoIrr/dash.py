from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, jsonify
)

from werkzeug.exceptions import abort
from AutoIrr.auth import login_required
from AutoIrr.db import get_db

bp = Blueprint('dash', __name__)

"""@bp.route('/', methods=('GET', 'POST'))
def index():
    db = get_db()
    if request.method == 'POST':
        irrigation = 1 if 'irrigation' in request.form else 0
        crop = request.form.get('crop', 'wheat')

        db.execute(
            'UPDATE settings SET irrigation_status = ?, selected_crop = ? WHERE id = 1', (irrigation, crop)
        )
        db.commit()
        return redirect(url_for('dash.index'))
    
    rows = db.execute(
        'SELECT timestamp, temperature, moisture, irrigation, crop FROM readings ORDER BY id DESC LIMIT 20'
    ).fetchone()

    settings = db.execute(
        'SELECT irrigation_status, selected_crop FROM settings WHERE id = 1'
    ).fetchone()
    
    return render_template('irrigation_dashboard.html', readings=rows, settings=settings)"""

@bp.route('/')
def index():
    db = get_db()
    
    # Fetch the single most recent sensor log entry
    rows = db.execute(
        'SELECT timestamp, temperature, moisture, irrigation, crop FROM readings ORDER BY id DESC LIMIT 20'
    ).fetchone()

    settings = db.execute(
        'SELECT irrigation_status, selected_crop FROM settings WHERE id = 1'
    ).fetchone()

    irrig = db.execute(
        'SELECT irrigation_que from ml'
    ).fetchone()
    
    return render_template('irrigation_dashboard.html', readings=rows, settings=settings, ml_prediction=irrig)

@bp.route('/update-settings', methods=['POST'])
def update_settings():
    db = get_db()
    data = request.get_json() # Catch JSON incoming from JavaScript Fetch API
    
    if not data:
        return jsonify({"status": "error", "message": "No data provided"}), 400
        
    irrigation = int(data.get('irrigation', 0))
    crop = data.get('crop', 'wheat')

    print(f"IRRIGATION: {irrigation} CROP: {crop}")
    
    # Commit configurations to the settings register row
    db.execute(
        'UPDATE settings SET irrigation_status = ?, selected_crop = ? WHERE id = 1',
        (irrigation, crop)
    )
    db.commit()
    
    return jsonify({"status": "success", "irrigation": irrigation, "crop": crop})