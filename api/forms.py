import enum
from .models import Genre, Status
from flask_wtf import FlaskForm
from wtforms.fields import TextAreaField, SubmitField, StringField, PasswordField, SelectField, DateTimeField, IntegerField, FloatField, DateField, SelectMultipleField
from wtforms.validators import InputRequired, Length, Email, EqualTo, NumberRange
from flask_wtf.file import FileRequired, FileField, FileAllowed
from wtforms.fields.html5 import DateField as html_date_field, TimeField as html_time_field

ALLOWED_FILE = {'PNG','JPG','png','jpg','JPEG','jpeg'}
genre = {"Rock","Rap","Hip Hop","R&B","Jazz","Pop","Country","Metal"}
status = {"Upcoming", "Booked", "Cancelled", "Inactive"}

#LoginForm that creates the login information
class LoginForm(FlaskForm):
    user_name=StringField("User Name", validators=[InputRequired('Enter user name')])
    password=PasswordField("Password", validators=[InputRequired('Enter user password')])
    submit = SubmitField("Login")

 # RegistrationForm input used to register new user
class RegisterForm(FlaskForm):
    user_name=StringField("User Name", validators=[InputRequired()])
    email_id = StringField("Email Address", validators=[Email("Please enter a valid email")])
    
    #linking two fields - password should be equal to data entered in confirm
    password=PasswordField("Password", validators=[InputRequired(),
                  EqualTo('confirm', message="Passwords should match")])
    confirm = PasswordField("Confirm Password")

    #submit button
    submit = SubmitField("Register")

#EventForm input used to create new event
class EventForm(FlaskForm):
    name = StringField('Event Name', validators=[InputRequired()]) #Creating all input fields
    description = TextAreaField('Description',validators=[InputRequired()])
    status = SelectField('Status', choices = status)
    genre = SelectField('Genre', choices = genre)
    image = FileField('Event Image', validators=[FileRequired(message='Image cannot be empty'), FileAllowed(ALLOWED_FILE, message='Only supports png,jpg,JPG,PNG')])   
    location = StringField('Location', validators=[InputRequired()])
    startTime = html_time_field('Start Time', validators= [InputRequired()])
    endTime = html_time_field('End Time', validators= [InputRequired()])
    artists = StringField('Artists', validators=[InputRequired()])
    ticketQuantity = IntegerField('Ticket Quantity', validators=[InputRequired()])
    ticketPrice =  IntegerField('Price', validators=[InputRequired()])
    startDate = html_date_field('Location', validators=[InputRequired()])
    submit = SubmitField("Create")
    buttonStyleEdit={'class': 'buttonStyle', 'style': 'background-color: #0275d8; color : white; margin-top : 1rem; width: 100%;'}
    submitEdit = SubmitField("Edit", render_kw=buttonStyleEdit)
    buttonStyleDelete={'class': 'buttonStyle', 'style': 'background-color: #f5b342; color : white; margin-top : 1rem; width: 100%;'}
    submitDelete = SubmitField("Delete", render_kw=buttonStyleDelete)

#DeleteForm input used to delete an event
class DeleteForm(FlaskForm):
    name = StringField('Event Name') 
    description = TextAreaField('Description')
    status = SelectField('Status', choices = status)
    genre = SelectField('Genre', choices = genre)
    image = FileField('Event Image', validators=[FileAllowed(ALLOWED_FILE, message='Only supports png,jpg,JPG,PNG')])   
    location = StringField('Location')
    startTime = html_time_field('Start Time')
    endTime = html_time_field('End Time')
    artists = StringField('Artists')
    ticketQuantity = IntegerField('Ticket Quantity')
    ticketPrice =  IntegerField('Price')
    startDate = html_date_field('Location')
    submit = SubmitField("Create")
    buttonStyleEdit={'class': 'buttonStyle', 'style': 'background-color: #0275d8; color : white; margin-top : 1rem; width: 100%;'}
    submitEdit = SubmitField("Edit", render_kw=buttonStyleEdit)
    buttonStyleDelete={'class': 'buttonStyle', 'style': 'background-color: #f5b342; color : white; margin-top : 1rem; width: 100%;'}
    submitDelete = SubmitField("Delete", render_kw=buttonStyleDelete)

#BookForm used to book a ticket from an event
class BookForm(FlaskForm):
  buttonStyle={'class': 'buttonStyle', 'style': 'background-color: #0275d8; color : white; margin-top : 1rem; width: 100%;'}
  ticketQuantity = IntegerField('Enter number of tickets to purchase:', validators=[InputRequired(), NumberRange(min=1, max=10000)])
  submit = SubmitField('Book', render_kw=buttonStyle)

#CommentForm used to post a comment onto an event page
class CommentForm(FlaskForm):
  textStyle={'class': 'textStyle', 'style': 'min-width: 30%; height: 100px'}
  buttonStyle={'class': 'buttonStyle', 'style': 'background-color: #0275d8; color : white; margin-top : 1rem;'}
  
  text = TextAreaField(' ', [InputRequired()], render_kw=textStyle)
  submit = SubmitField('Post', render_kw=buttonStyle)

#ProfileForm used to view your profile 
class ProfileForm(FlaskForm):
  buttonStyle={'class': 'buttonStyle', 'style': 'background-color: #0275d8; color : white; margin-top : 1rem; width: 100%;'}
  submitProfile = SubmitField('View', render_kw=buttonStyle)



