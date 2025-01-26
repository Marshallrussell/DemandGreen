from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import CORS
import enum

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Enum for user roles
class RoleEnum(enum.Enum):
    CLIENT = "client"
    WORKER = "worker"

# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.Enum(RoleEnum), nullable=False)

# Gig model
class Gig(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

# Initialize database
with app.app_context():
    db.create_all()

# Root route
@app.route('/')
def home():
    return render_template('index.html')

# Register route
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data or not all(key in data for key in ('username', 'email', 'password', 'role')):
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

# Login route
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or not all(key in data for key in ('email', 'password')):
        return jsonify({'error': 'Missing required fields'}), 400

    user = User.query.filter_by(email=data['email']).first()
    if user and check_password_hash(user.password, data['password']):
        return jsonify({'message': 'Login successful', 'user': user.username})
    return jsonify({'error': 'Invalid credentials'}), 401

# Gigs route
@app.route('/gigs', methods=['GET', 'POST'])
def gigs():
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
        if not data or not all(key in data for key in ('title', 'description', 'client_id')):
            return jsonify({'error': 'Missing required fields'}), 400

        new_gig = Gig(
            title=data['title'],
            description=data['description'],
            client_id=data['client_id']
        )
        db.session.add(new_gig)
        db.session.commit()
        return jsonify({'message': 'Gig created successfully'}), 201

# List all routes
@app.route('/routes', methods=['GET'])
def list_routes():
    output = []
    for rule in app.url_map.iter_rules():
        output.append({
            "route": rule.rule,
            "methods": list(rule.methods)
        })
    return jsonify(output)

if __name__ == '__main__':
    app.run(debug=True)
