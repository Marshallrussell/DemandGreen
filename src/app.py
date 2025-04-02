from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import CORS
import enum

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:password@localhost/jobsDB'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# ==============================
# ENUMS & MODELS
# ==============================

class RoleEnum(enum.Enum):
    CLIENT = "client"
    WORKER = "worker"

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.Enum(RoleEnum), nullable=False)

class Gig(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class Job(db.Model):
    __tablename__ = 'jobs'  # Ensures it connects to the 'jobs' table

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    location = db.Column(db.String(255), nullable=True)
    salary = db.Column(db.Numeric(10,2), nullable=True)  # Matches DECIMAL(10,2)
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())


# Create tables if they don’t exist
with app.app_context():
    db.create_all()

# ==============================
# ROUTES
# ==============================

@app.route('/')
def home():
    return render_template('index.html')

# ------------------------------
# AUTHENTICATION ROUTES
# ------------------------------

@app.route('/register', methods=['POST'])
def register():
    """Register a new user."""
    data = request.get_json()
    required_fields = {'username', 'email', 'password', 'role'}

    if not data or not required_fields.issubset(data):
        return jsonify({'error': 'Missing required fields'}), 400

    hashed_password = generate_password_hash(data['password'], method='sha256')

    new_user = User(
        username=data['username'],
        email=data['email'],
        password=hashed_password,
        role=RoleEnum(data['role'])
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully'}), 201

@app.route('/login', methods=['POST'])
def login():
    """Authenticate a user."""
    data = request.get_json()
    
    if not data or 'email' not in data or 'password' not in data:
        return jsonify({'error': 'Missing required fields'}), 400

    user = User.query.filter_by(email=data['email']).first()

    if user and check_password_hash(user.password, data['password']):
        return jsonify({'message': 'Login successful', 'user': user.username})
    
    return jsonify({'error': 'Invalid credentials'}), 401

# ------------------------------
# GIG ROUTES
# ------------------------------

@app.route('/gigs', methods=['GET', 'POST'])
def gigs():
    """Get all gigs or create a new gig."""
    if request.method == 'GET':
        gigs = Gig.query.all()
        return jsonify([{
            'id': gig.id,
            'title': gig.title,
            'description': gig.description,
            'client_id': gig.client_id
        } for gig in gigs])

    if request.method == 'POST':
        data = request.get_json()
        required_fields = {'title', 'description', 'client_id'}

        if not data or not required_fields.issubset(data):
            return jsonify({'error': 'Missing required fields'}), 400

        new_gig = Gig(
            title=data['title'],
            description=data['description'],
            client_id=data['client_id']
        )

        db.session.add(new_gig)
        db.session.commit()

        return jsonify({'message': 'Gig created successfully'}), 201

# ------------------------------
# JOB SEARCH ROUTE
# ------------------------------

@app.route('/jobs', methods=['GET'])
def get_jobs():
    """Search jobs based on title, description, or location."""
    search = request.args.get('search', '')

    jobs = Job.query.filter(
        (Job.title.ilike(f"%{search}%")) |
        (Job.description.ilike(f"%{search}%")) |
        (Job.location.ilike(f"%{search}%"))
    ).all()

    return jsonify([{
        'id': job.id,
        'title': job.title,
        'description': job.description,
        'location': job.location,
        'salary': job.salary,
        'created_at': job.created_at
    } for job in jobs])

# ------------------------------
# LIST ROUTES FOR DEBUGGING
# ------------------------------

@app.route('/routes', methods=['GET'])
def list_routes():
    """List all available routes in the app."""
    output = [{"route": rule.rule, "methods": list(rule.methods)} for rule in app.url_map.iter_rules()]
    return jsonify(output)

# ==============================
# RUN THE APP
# ==============================

if __name__ == '__main__':
    app.run(debug=True)
