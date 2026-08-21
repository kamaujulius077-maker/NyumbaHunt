import os
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO
from werkzeug.utils import secure_filename
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'softech_secret_ke'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///softech.db'
app.config['UPLOAD_FOLDER'] = 'static/uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs('static/css', exist_ok=True)
os.makedirs('static/js', exist_ok=True)

db = SQLAlchemy(app)
socketio = SocketIO(app, cors_allowed_origins="*")

class House(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150))
    location = db.Column(db.String(100))
    price = db.Column(db.Integer)
    beds = db.Column(db.String(20))
    phone = db.Column(db.String(20))
    description = db.Column(db.Text)
    image = db.Column(db.String(200))
    date = db.Column(db.DateTime, default=datetime.utcnow)

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    location = request.args.get('location','')
    max_price = request.args.get('max_price','')
    beds = request.args.get('beds','')
    query = House.query
    if location:
        query = query.filter(House.location.ilike(f'%{location}%'))
    if max_price and max_price.isdigit():
        query = query.filter(House.price <= int(max_price))
    if beds:
        query = query.filter(House.beds == beds)
    houses = query.order_by(House.date.desc()).all()
    return render_template('index.html', houses=houses)

@app.route('/post', methods=['GET','POST'])
def post_house():
    if request.method == 'POST':
        file = request.files.get('photo')
        filename = ''
        if file and file.filename:
            filename = datetime.now().strftime("%H%M%S_") + secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        house = House(
            title=request.form['title'],
            location=request.form['location'],
            price=int(request.form['price']),
            beds=request.form['beds'],
            phone=request.form['phone'],
            description=request.form['description'],
            image=filename
        )
        db.session.add(house)
        db.session.commit()
        socketio.emit('new_house', {
            'title': house.title, 'location': house.location,
            'price': house.price, 'beds': house.beds,
            'phone': house.phone, 'description': house.description,
            'image': filename
        })
        return redirect('/')
    return render_template('post.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

if __name__ == '__main__':
    socketio.run(app, debug=True, port=5001)
