from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///houses.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = os.path.join('static', 'uploads')
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

db = SQLAlchemy(app)

class House(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    location = db.Column(db.String(100))
    price = db.Column(db.Integer)
    beds = db.Column(db.String(10))
    phone = db.Column(db.String(20))
    description = db.Column(db.Text)
    image = db.Column(db.String(100))
    date = db.Column(db.DateTime, default=db.func.current_timestamp())

with app.app_context():
    try:
        db.create_all()
    except:
        pass

@app.route('/')
def home():
    location = request.args.get('location','')
    max_price = request.args.get('max_price','')
    beds = request.args.get('beds','')
    query = House.query
    if location:
        query = query.filter(House.location.ilike(f"%{location}%"))
    if max_price and max_price.isdigit():
        query = query.filter(House.price <= int(max_price))
    if beds:
        query = query.filter(House.beds == beds)
    houses = query.order_by(House.date.desc()).all()
    return render_template('index.html', houses=houses)

@app.route('/post', methods=['GET','POST'])
def post_house():
    if request.method == 'POST':
        file = request.files.get('image')
        filename = ''
        if file and file.filename:
            filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        
        house = House(
            title=request.form.get('title'),
            location=request.form.get('location'),
            price=int(request.form.get('price',0) or 0),
            beds=request.form.get('beds'),
            phone=request.form.get('phone'),
            description=request.form.get('description'),
            image=filename
        )
        db.session.add(house)
        db.session.commit()
        return redirect('/')
    return render_template('post.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

if __name__ == '__main__':
    app.run(debug=True)