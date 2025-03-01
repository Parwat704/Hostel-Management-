from app import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"User('{self.username}')"

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'))

    def __repr__(self):
        return f"Student('{self.name}', '{self.email}')"

class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    room_number = db.Column(db.String(50), unique=True, nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    students = db.relationship('Student', backref='room', lazy=True)

    def __repr__(self):
        return f"Room('{self.room_number}', '{self.capacity}')"

class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'))
    amount = db.Column(db.Float, nullable=False)
    date = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f"Payment('{self.student_id}', '{self.amount}')"