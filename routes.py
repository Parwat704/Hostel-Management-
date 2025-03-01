from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required
from app import app, db
from app.forms import LoginForm, RegistrationForm, StudentForm, RoomForm, PaymentForm
from app.models import User, Student, Room, Payment

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.password == form.password.data:
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password', 'danger')
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('index'))

@app.route('/add_student', methods=['GET', 'POST'])
@login_required
def add_student():
    form = StudentForm()
    if form.validate_on_submit():
        student = Student(name=form.name.data, email=form.email.data, room_id=form.room_id.data)
        db.session.add(student)
        db.session.commit()
        flash('Student added successfully!', 'success')
        return redirect(url_for('index'))
    return render_template('add_student.html', form=form)

@app.route('/add_room', methods=['GET', 'POST'])
@login_required
def add_room():
    form = RoomForm()
    if form.validate_on_submit():
        room = Room(room_number=form.room_number.data, capacity=form.capacity.data)
        db.session.add(room)
        db.session.commit()
        flash('Room added successfully!', 'success')
        return redirect(url_for('index'))
    return render_template('add_room.html', form=form)

@app.route('/view_students')
@login_required
def view_students():
    students = Student.query.all()
    return render_template('view_students.html', students=students)

@app.route('/view_rooms')
@login_required
def view_rooms():
    rooms = Room.query.all()
    return render_template('view_rooms.html', rooms=rooms)

@app.route('/add_payment', methods=['GET', 'POST'])
@login_required
def add_payment():
    form = PaymentForm()
    if form.validate_on_submit():
        payment = Payment(student_id=form.student_id.data, amount=form.amount.data, date=form.date.data)
        db.session.add(payment)
        db.session.commit()
        flash('Payment added successfully!', 'success')
        return redirect(url_for('index'))
    return render_template('add_payment.html', form=form)

@app.route('/view_payments')
@login_required
def view_payments():
    payments = Payment.query.all()
    return render_template('view_payments.html', payments=payments)

@app.route('/delete_student/<int:student_id>', methods=['POST'])
@login_required
def delete_student(student_id):
    student = Student.query.get_or_404(student_id)
    db.session.delete(student)
    db.session.commit()
    flash('Student deleted successfully!', 'success')
    return redirect(url_for('view_students'))

@app.route('/edit_student/<int:student_id>', methods=['GET', 'POST'])
@login_required
def edit_student(student_id):
    student = Student.query.get_or_404(student_id)
    form = StudentForm(obj=student)
    if form.validate_on_submit():
        student.name = form.name.data
        student.email = form.email.data
        student.room_id = form.room_id.data
        db.session.commit()
        flash('Student updated successfully!', 'success')
        return redirect(url_for('view_students'))
    return render_template('edit_student.html', form=form, student=student)