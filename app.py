from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask('__name__')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///student.db'
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
db = SQLAlchemy(app)

class Details(db.Model):
    rno = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable = False)
    std = db.Column(db.Integer, nullable = False)
    gender = db.Column(db.String(10), nullable = False)
    grade = db.Column(db.String(10), nullable = False)
    contact = db.Column(db.Integer, nullable = False)

    def __repr__(self):
        return f"{self.name} - {self.std} - {self.gender} - {self.grade} - {self.contact}"

@app.route('/', methods = ['GET', 'POST'])
def home():
    if request.method == 'POST':
        print("Name: ",request.form['name'])
        print("Class: ",request.form['class'])
        print("Gender: ",request.form['gender'])
        print("Grade: ",request.form['grade'])
        print("Contact: ",request.form['contact'])

        # Storing Valsue in a variable
        names = request.form['name']
        stds = request.form['class']
        genders = request.form['gender']
        grades = request.form['grade']
        contacts = request.form['contact']

        details = Details(name = names, std = stds, gender = genders, grade = grades, contact = contacts)
        db.session.add(details)
        db.session.commit()

    student = Details.query.all()
    return render_template('index.html', students = student)
    

@app.route('/show')
def show():
    allDetails = Details.query.all()
    return render_template('show.html', allDetails = allDetails)

@app.route('/delete/<int:rno>')
def delete(rno):
    student = Details.query.filter_by(rno = rno).first()
    db.session.delete(student)
    db.session.commit()
    return redirect('/show')

@app.route('/update/<int:rno>', methods = ['POST', 'GET'])
def update(rno):
    if request.method == 'POST':
        names = request.form['name']
        stds = request.form['class']
        genders = request.form['gender']
        grades = request.form['grade']
        contacts = request.form['contact']

        update = Details.query.filter_by(rno = rno).first()
        update.name = names
        update.std = stds
        update.gender = genders
        update.grade = grades
        update.contact = contacts
        db.session.add(update)
        db.session.commit()
        return redirect('/show')

    student = Details.query.filter_by(rno = rno).first()
    return render_template('/update.html', student = student)


with app.app_context():
    db.create_all()


if __name__ == '__main__':
    app.run(debug = True)
