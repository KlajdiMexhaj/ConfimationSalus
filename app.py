from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

app = Flask(__name__)

# Configure the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///form_data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your_secret_key'
db = SQLAlchemy(app)

# Create the model to store the form data
class FormData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    emer = db.Column(db.String(100), nullable=False)
    mbiemer = db.Column(db.String(100), nullable=False)
    specialiteti = db.Column(db.String(100), nullable=False)
    confirmation = db.Column(db.String(10), nullable=True)

# Create the admin panel
admin = Admin(app, name='Form Admin')
admin.add_view(ModelView(FormData, db.session))

# Initialize the database
with app.app_context():
    db.create_all()

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        emer = request.form['emer']
        mbiemer = request.form['mbiemer']
        specialiteti = request.form['specialiteti']
        
        # If the "Po" checkbox is checked, save it as 'Po', otherwise save None (no confirmation)
        confirmation = 'Po' if 'confirmation' in request.form else None
        
        # Create a new FormData instance and save it to the database
        form_data = FormData(emer=emer, mbiemer=mbiemer, specialiteti=specialiteti, confirmation=confirmation)
        db.session.add(form_data)
        db.session.commit()

        return redirect(url_for('thank_you'))
    
    return render_template('index.html')


@app.route('/thank-you')
def thank_you():
    return render_template('thank_you.html')

if __name__ == '__main__':
    app.run(debug=True)
