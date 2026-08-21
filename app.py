from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///houses.db'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024 # 5MB max

db = SQLAlchemy(app)

# CREATE UPLOADS FOLDER
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

class House(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    beds = db.Column(db.Integer)
    baths = db.Column(db.Integer)
    location = db.Column(db.String(100))
    description = db.Column(db.Text)
    image_filename = db.Column(db.String(100))
    whatsapp = db.Column(db.String(20))

with app.app_context():
    db.create_all()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg'}

@app.route('/')
def home():
    houses = House.query.all()
    # ADD FILTERS HERE LIKE BEFORE
    return render_template('index.html', houses=houses)

@app.route('/post', methods=['GET', 'POST'])
def post():
    if request.method == 'POST':
        file = request.files['image']
        filename = None
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        new_house = House(
            title=request.form['title'],
            price=request.form['price'],
            beds=request.form['beds'],
            baths=request.form['baths'],
            location=request.form['location'],
            description=request.form['description'],
            image_filename=filename,
            whatsapp=request.form['whatsapp']
        )
        db.session.add(new_house)
        db.session.commit()
        return redirect('/')
    return render_template('post.html')

@app.route('/contact/<int:house_id>')
def contact(house_id):
    house = House.query.get_or_404(house_id)
    whatsapp_msg = f"Hi, I'm interested in: {house.title} for KES {house.price}/month"
    whatsapp_link = f"https://wa.me/{house.whatsapp}?text={whatsapp_msg}"
    return render_template('contact.html', house=house, whatsapp_link=whatsapp_link)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return redirect(url_for('static', filename='../uploads/' + filename), code=301)

if __name__ == '__main__':
    app.run(debug=True)