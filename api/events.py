from flask import Blueprint, render_template, request, redirect, url_for, flash
from wtforms.validators import Required
from .models import Event, Comment, Ticket, Status
from .forms import CommentForm, EventForm, BookForm, DeleteForm
from . import db
from werkzeug.utils import secure_filename
import os
import datetime
#additional import:
from flask_login import login_required, current_user
# Defining bp variable
bp = Blueprint('event', __name__, url_prefix='/events')

# Route handling dynamic, single event view pages
@bp.route('/<id>', methods = ['GET', 'POST'])
def eventView(id):
    event = Event.query.filter_by(id=id).first() # Gets the event with a given event ID
    cform = CommentForm() # Create comment form instance
    bform = BookForm() # Create booking form instance
    return render_template('events/event-view.html', event=event, cform=cform, bform=bform)

# Route handling for editing an event
@bp.route('/edit-event/<id>', methods = ['GET', 'POST'])
@login_required
def editEvent(id):
    form = DeleteForm() #Creates a new deleteform object
    event = Event.query.filter_by(id=id).first()
    # If the delete button is pressed, delete the event, comment and tickets from the database
    # which have the id that was passed.
    if form.submitDelete.data:
        Event.query.filter_by(id=id).delete()
        Comment.query.filter_by(eventId=id).delete()
        Ticket.query.filter_by(eventId=id).delete()
        db.session.commit()
        print('Successfully deleted event', 'deleted')
        return redirect(url_for('main.index'))
    # Check if every input required is valid
    if form.validate_on_submit():   
        if form.submitEdit.data: 
            # check and return image to be database appropriate
            db_file_path=check_upload_file(form)
            # create event object to be updated in db
            event = Event.query.filter_by(id=id).update(dict(
                name=form.name.data,
                description=form.description.data,
                image=db_file_path,
                status=form.status.data,
                genre=form.genre.data,
                artists=form.artists.data,
                startDate=form.startDate.data.strftime("%Y-%m-%d"),
                startTime=form.startTime.data.strftime("%H:%M"),
                endTime=form.endTime.data.strftime("%H:%M"),
                location=form.location.data,
                ticketQuantity=form.ticketQuantity.data,
                ticketPrice=form.ticketPrice.data
            ))
            if (type(form.ticketQuantity.data) != int): # Error handling for incorrect input
                error = "An integer value is required for the ticket quantity field"
                flash(error)
                return render_template('events/edit-event.html', event=event, form=form)
            elif (type(form.ticketPrice.data) != int):
                error = "An integer value is required for the ticket price field"
                flash(error)
                return render_template('events/edit-event.html', event=event, form=form)
            db.session.commit() # Commits updated event to the database
            print('Successfully edited new event', 'success')
            return redirect(url_for('event.eventView', id = id)) # Send to the event view of the edited event  
    return render_template('events/edit-event.html', event=event, form=form)


# createEvent Route: Used to handle functionality regarding event creation
@bp.route('/create-event', methods = ['GET', 'POST'])
@login_required
def createEvent():
    form = EventForm()
    if form.submit.data:
        if form.validate_on_submit():
            # check and return image to be database appropriate
            db_file_path=check_upload_file(form)
            # create event object to be sent to db
            event=Event( 
                name=form.name.data,
                creator= current_user.get_id(),
                description=form.description.data,
                image=db_file_path,
                status=form.status.data,
                genre=form.genre.data,
                artists=form.artists.data,
                startDate=form.startDate.data.strftime("%Y-%m-%d"),
                startTime=form.startTime.data.strftime("%H:%M"),
                endTime=form.endTime.data.strftime("%H:%M"),
                location=form.location.data,
                ticketQuantity=form.ticketQuantity.data,
                ticketPrice=form.ticketPrice.data
            )
            # add the object to the db session
            db.session.add(event)
            # commit to the database
            db.session.commit()
            print('Successfully created new event', 'success')
            return redirect(url_for('main.index'))
        else:
            # Check if user did not input int
            if (type(form.ticketQuantity.data) != int):
                error = "An integer value is required for the ticket quantity field"
                flash(error)
                return render_template('events/create-event.html', form=form)
            # Check if user did not input int
            elif (type(form.ticketPrice.data) != int):
                error = "An integer value is required for the ticket price field"
                flash(error)
                return render_template('events/create-event.html', form=form)
        
    return render_template('events/create-event.html', form=form)

def check_upload_file(form):
    #get file data from form  
    fp=form.image.data
    filename=fp.filename
    # store image file relative to current file of module
    BASE_PATH=os.path.dirname(os.path.abspath(__file__))
    upload_path=os.path.join(BASE_PATH,'static/image',secure_filename(filename))
    # file/static/image - upload location
    db_upload_path='/static/image/' + secure_filename(filename)
    # store relative path in DB as image location in HTML is relative
    # save the file and return the db upload path  
    fp.save(upload_path)
    return db_upload_path


@bp.route('/<event>/comment', methods = ['GET', 'POST'])  
@login_required
def comment(event):
    form = CommentForm()  
    # get event object associated to the page and comment
    event_obj = Event.query.filter_by(id=event).first()
    if form.validate_on_submit():  
      # read the comment from form
      comment = Comment(text=form.text.data,  
                        event=event_obj,
                        user=current_user) 
      # here the back-referencing works - comment.event is set
      # and the link is created
      db.session.add(comment) 
      db.session.commit() 

      print('Your comment has been added', 'success') 
    # using redirect sends a GET request to destination.show
    return redirect(url_for('event.eventView', id=event))

@bp.route('/<event>/booking', methods = ['GET', 'POST'])  
@login_required
def booking(event):
    form = BookForm()  
    # get event object associated to the page and book
    event_obj = Event.query.filter_by(id=event).first()
    error = None

    # if the user has inputted an incorrect value for ticket 
    # quantity or price, flash a message handled by the html
    if (type(form.ticketQuantity.data) != int):
        error = "An integer value is required for the booking field"
        flash(error)
        return redirect(url_for('event.eventView', id=event))
    else:
        # otherwise, set the ticket quantity and convert to integers
        formTicketQty = int(form.ticketQuantity.data)
        eventTicketQty = int(event_obj.ticketQuantity)
        
    # the form can only go through if there are sufficient tickets and the event is not of status booked
    if form.validate_on_submit() and formTicketQty <= eventTicketQty and event_obj.status != 'Booked':        
      # create ticket object   
      booking = Ticket( quantity=form.ticketQuantity.data,
                        event=event_obj,
                        user=current_user)
      # adjust the event's ticket quantity depending on the amount that the user purchased   
      eventTicketQty -= formTicketQty
      event_obj = Event.query.filter_by(id=event).update(dict(ticketQuantity=eventTicketQty))

      # change the status of the event if there are no tickets left 
      if eventTicketQty == 0:
          event_obj = Event.query.filter_by(id=event).update(dict(status="Booked"))  
      
      db.session.add(booking) 
      db.session.commit()

      print('Successfully Bought Tickets', 'Success') 
    # show the event view page again
    return redirect(url_for('event.eventView', id=event))