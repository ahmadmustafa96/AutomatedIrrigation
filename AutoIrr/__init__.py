import os
import threading
import functools
from flask import Flask, render_template

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'autoirr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)        

    # ensure the instance folder exists
    os.makedirs(app.instance_path, exist_ok=True)
        
    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import dash
    app.register_blueprint(dash.bp)
    app.add_url_rule('/', endpoint='index')

    if not app.debug or os.environ.get("WERKZEUG_RUN_MAIN") == "true":
        from .machine_learnt import ml_pipeline
        from .serial_worker import serial_reader_worker
        db_path = app.config['DATABASE']
        
        serial_thread = threading.Thread(target=serial_reader_worker, args=(db_path,), daemon=True)
        serial_thread.start()

        serial_thread = threading.Thread(target=ml_pipeline, args=(db_path,), daemon=True)
        serial_thread.start()

    return app