import enum
from . import db
from datetime import datetime
from flask_login import UserMixin

# User model, hashing passwords is done also
class User(db.Model, UserMixin):
    __tablename__='users' 
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), index=True, unique=True, nullable=False)
    emailid = db.Column(db.String(100), index=True, nullable=False)
	# the storage should be at least 255 chars long
    password_hash = db.Column(db.String(255), nullable=False)

    tickets = db.relationship('Ticket', backref='user')
    # relation to call user.comments and comment.created_by
    comments = db.relationship('Comment', backref='user')

# An enumerator for the different event statuses
class Status(enum.Enum):
    Booked = "Booked"
    Cancelled = "Cancelled"
    Inactive = "Inactive"
    Upcoming = "Upcoming"

# An enumerator for the different event genres
class Genre(enum.Enum):
    Rock = "Rock"
    Rap = "Rap"
    hipHop = "Hip Hop"
    RnB = "R&B"
    Jazz = "Jazz"
    Pop = "Pop"
    Country = "Country"
    Metal = "Metal"
    def __repr__(): #string print method
        return ['booked', 'active']

# Event model, linked to comments
class Event(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    creator = db.Column(db.Integer) # User ID of event creator
    name = db.Column(db.String(80))
    description = db.Column(db.String(200))
    image = db.Column(db.String(400))
    status = db.Column(db.String(100)) # enum of statuses
    genre = db.Column(db.String(100))
    artists = db.Column(db.String(100)) # string array of artists
    startDate = db.Column(db.String(100))
    startTime = db.Column(db.String(100))
    endTime = db.Column(db.String(100))
    location = db.Column(db.String(100))
    ticketQuantity = db.Column(db.String(100))
    ticketPrice = db.Column(db.String(5))
    # ... Create the Comments db.relationship
    comments = db.relationship('Comment', backref='event')
	
    def __repr__(self): #string print method
        return "<Name: {}>".format(self.name)

# Ticket model, linked to users and event
class Ticket(db.Model):
    __tablename__ = 'tickets'
    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer)
    event = db.relationship('Event', backref='ticket')

    userId = db.Column(db.Integer, db.ForeignKey('users.id'))
    eventId = db.Column(db.Integer, db.ForeignKey('events.id'))

    def __repr__(self): 
        return "<Ticket: {}".format(self.eventId)

# Comment model, linked to users and event
class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(400))
    created_at = db.Column(db.DateTime, default=datetime.now())
    #add the foreign keys
    userId = db.Column(db.Integer, db.ForeignKey('users.id'))
    eventId = db.Column(db.Integer, db.ForeignKey('events.id'))

    def __repr__(self):
        return "<Comment: {}>".format(self.text)
