from flask import Blueprint, render_template, url_for, request, session, redirect
from flask_login import login_required, current_user

from website import events
from .models import Event, Ticket, User, Genre
from .forms import ProfileForm
from sqlalchemy import or_

bp = Blueprint('main', __name__)
   
# Route for main index page
@bp.route('/')
def index():
    events = Event.query.all() 
    genres = [e.value for e in Genre]
    user = current_user.get_id()
    return render_template('index.html', events=events, genres=genres, user=user)


# Route for profile ticket Page
@bp.route('/profile-tickets')
@login_required
def profileTickets():
    events = Event.query.all() 
    tickets = Ticket.query.filter_by(userId=current_user.get_id()).all() # correct ? distinct(eventId)
    return render_template('profile-tickets.html', tickets=tickets, events=events)

# Route for search fuctionality
@bp.route('/search')
def search():
    if request.args['search']:
        search_input = request.args['search']
        if (not search_input):
            return redirect(url_for('index'))
        else:
            dest = "%" + search_input + '%'
            location = "%" + search_input + '%'
            eventDescription = Event.query.filter(or_(Event.location.like(location), Event.description.like(dest), Event.status.like(dest), Event.genre.like(dest))).all() # add AND to check genre dropdown selection?
            return render_template('index.html', events=eventDescription)
    else:
        return redirect(url_for('main.index'))