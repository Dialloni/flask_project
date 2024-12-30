from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from forms import HealthDataForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///health_data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class HealthData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    exercise = db.Column(db.Integer, nullable=False)
    meditation = db.Column(db.Integer, nullable=False)
    sleep = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<HealthData {self.id}>'

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/form', methods=['GET', 'POST'])
def form():
    form = HealthDataForm()
    if form.validate_on_submit():
        # Create a new health data entry
        new_data = HealthData(
            date=form.date.data,
            exercise=form.exercise.data,
            meditation=form.meditation.data,
            sleep=form.sleep.data
        )
        # Add the new data to the database
        db.session.add(new_data)
        db.session.commit()
        # Redirect to the dashboard
        return redirect(url_for('dashboard'))
    return render_template('form.html', form=form)

@app.route('/dashboard')
def dashboard():
    # Retrieve all health data from the database
    all_data = HealthData.query.all()

    # Prepare data for charts
    dates = [data.date.strftime('%Y-%m-%d') for data in all_data]
    exercise_data = [data.exercise for data in all_data]
    meditation_data = [data.meditation for data in all_data]
    sleep_data = [data.sleep for data in all_data]

    return render_template('dashboard.html', dates=dates, exercise_data=exercise_data, meditation_data=meditation_data, sleep_data=sleep_data)

if __name__ == '__main__':
    app.run(debug=True)