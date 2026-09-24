import os
import sys
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# fix paths
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

# Create app with absolute paths for Vercel
app = Flask(__name__,
    template_folder=os.path.join(parent_dir, 'templates'),
    static_folder=os.path.join(parent_dir, 'static')
)

app.config['SECRET_KEY'] = 'nyumba-hunt-secret'
# Use /tmp which IS writable on Vercel
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/houses.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = '/tmp/uploads'

db = SQLAlchemy(app)

class House(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(100))
    price = db.Column(db.Integer)
    beds = db.Column(db.String(20))
    phone = db.Column(db.String(20))
    description = db.Column(db.Text)
    image = db.Column(db.String(200))
    date = db.Column(db.DateTime, default=datetime.utcnow)

# Create tables safely
try:
    os.makedirs('/tmp/uploads', exist_ok=True)
    with app.app_context():
        db.create_all()
except Exception as e:
    print(f"DB init error: {e}")

# Now import your routes from app.py
# If you have routes in app.py, we need to copy them here
# For now, let's import them:
try:
    from app import *
    # re-assign the working app to Vercel's app
    # your routes will be registered on the imported app object
    # so we need to use that one
    import app as main_app
    app = main_app.app
    db = main_app.db
except Exception as e:
    print(f"Route import error: {e}")

# Simple home if import fails
@app.route('/')
def home():
    try:
        houses = House.query.order_by(House.date.desc()).all()
        return f"Nyumba Hunt is live - Found {len(houses)} houses. Fix routes import."
    except:
        return "Nyumba Hunt is live on Vercel!" 