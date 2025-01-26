from flask import Flask
from app.config import Config
from app.extensions import init_mongo
from flask_cors import CORS
def create_app():
    app = Flask(__name__)
    CORS(app, resources={r"/*": {"origins": "*"}})
    app.config.from_object(Config)
    
    init_mongo(app)
    from app.routes.test_route import test_bp
    from app.routes.project_routes import project_bp
    from app.routes.manager_routes import manager_bp
    from app.routes.worker_routes import worker_bp
    from app.routes.cctv_routes import cctv_bp
    app.register_blueprint(test_bp)
    app.register_blueprint(project_bp)
    app.register_blueprint(manager_bp)
    app.register_blueprint(worker_bp)
    app.register_blueprint(cctv_bp)

    return app