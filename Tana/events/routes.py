#!/usr/bin/python3
"""Routes for the app"""
from flask import Blueprint, current_app, jsonify, request, render_template, redirect, url_for, flash
from Tana.models.eventcategory import EventCategory
from Tana.models.events import Events
from Tana import db_storage
from Tana.events.forms import EventForm
from flask_login import current_user, login_required
from Tana.models.roles import UserRole
from Tana.models.constituency import Constituency
from Tana.models.ward import Ward
from Tana.models.pollingstation import PollingStation

events_bp = Blueprint('events', __name__)

# create a route to add events
@events_bp.route('/add_event', methods=['GET', 'POST'], strict_slashes=False)
@login_required
def add_event():
    """Route to add an event"""
    form = EventForm()
    polling_stations = db_storage.all(PollingStation).values()
    form.polling_station_name.choices = [(ps.name, ps.name) for ps in polling_stations]

    if form.validate_on_submit():
        event_name = form.event_name.data
        event_description = form.event_description.data
        impact_level = form.impact_level.data
        event_leader = form.event_leader.data
        event_location = form.event_location.data
        contact_person = form.contact_person.data
        start_date = form.start_date.data
        end_date = form.end_date.data
        polling_station_name = form.polling_station_name.data
        user_id = current_user.id

        polling_station = db_storage.find_one(PollingStation, name=polling_station_name)

        if not polling_station:
            flash('Polling station not found!', 'danger')
            return redirect(url_for('events.add_event'))

        event = Events(
            event_name=event_name, 
            event_description=event_description, 
            impact_level=impact_level, 
            event_leader=event_leader, 
            event_location=event_location, 
            contact_person=contact_person,
            start_date=start_date,
            end_date=end_date,
            polling_station_id=polling_station.id,
            user_id=user_id
        )

        db_storage.new(event)
        db_storage.save()
        flash('Event has been created!', 'success')
        return redirect(url_for('events.view_events'))

    return render_template('add_event.html', title='Add Event', form=form, polling_stations=polling_stations)


# create a route to view events
@events_bp.route('/view_events', methods=['GET'], strict_slashes=False)
@login_required
def view_events():
    """Route to view events"""
    from Tana.models.members import users
    session = db_storage.get_session()
    
    event_name = request.args.get('event_name', '')
    impact_level = request.args.get('impact_level', '')
    polling_station = request.args.get('polling_station', '')
    entered_by = request.args.get('entered_by', '')

    query = session.query(Events).join(Events.polling_station).join(Events.user)

    if event_name:
        query = query.filter(Events.event_name.ilike(f'%{event_name}%'))
    
    if impact_level:
        query = query.filter(Events.impact_level == impact_level)
    
    if polling_station:
        query = query.filter(PollingStation.name.ilike(f'%{polling_station}%'))
    
    if entered_by:
        query = query.filter(users.name.ilike(f'%{entered_by}%'))

    events = query.order_by(Events.created_at.desc()).all()
    
    return render_template('events.html', events=events)


# route for viewing events only, no need to edit or delete. uses view_events.html
@events_bp.route('/view_events_only', methods=['GET'], strict_slashes=False)
def view_events_only():
    """Route to view events"""
    from Tana.models.members import users
    session = db_storage.get_session()

    event_name = request.args.get('event_name', '')
    impact_level = request.args.get('impact_level', '')
    polling_station = request.args.get('polling_station', '')
    entered_by = request.args.get('entered_by', '')

    query = session.query(Events).join(Events.polling_station).join(Events.user)

    if event_name:
        query = query.filter(Events.event_name.ilike(f'%{event_name}%'))
    
    if impact_level:
        query = query.filter(Events.impact_level == impact_level)
    
    if polling_station:
        query = query.filter(PollingStation.name.ilike(f'%{polling_station}%'))
    
    if entered_by:
        query = query.filter(users.name.ilike(f'%{entered_by}%'))

    events = query.order_by(Events.created_at.desc()).all()
    
    return render_template('events.html', events=events)

@events_bp.route('/delete_event/<int:event_id>', methods=['GET', 'POST'], strict_slashes=False)
@login_required
def delete_event(event_id):
    """route to delete an event"""
    event = db_storage.get(Events, id=event_id)
    if event is None:
        return redirect(url_for('events.view_events'))
    db_storage.delete(event)
    db_storage.save()
    flash('Event has been deleted!', 'success')
    return redirect(url_for('events.view_events'))

@events_bp.route('/edit_event/<int:event_id>', methods=['GET', 'POST'])
@login_required
def edit_event(event_id):
    """Route to edit an event"""
    event = db_storage.find_one(Events, id=event_id)
    form = EventForm(obj=event)

    if request.method == 'POST' and form.validate_on_submit():
        form.populate_obj(event)
        db_storage.save()
        flash('Event updated successfully', 'success')
        return redirect(url_for('events.view_events'))

    return render_template('edit_event.html', form=form, event=event)

@events_bp.route('/get_all_polling_stations', methods=['GET'])
def get_all_polling_stations():
    """Route to get all polling station names"""
    polling_stations = db_storage.all(PollingStation).values()
    polling_station_names = [station.name for station in polling_stations]
    return jsonify({'pollingStations': polling_station_names})

@events_bp.route('/get_polling_station_info', methods=['GET'])
def get_polling_station_info():
    """Route to get polling station information"""
    polling_station_name = request.args.get('polling_station')

    if not polling_station_name:
        return jsonify({'error': 'Polling station name is required'}), 400

    polling_station = db_storage.find_one(PollingStation, name=polling_station_name)

    if not polling_station:
        return jsonify({'error': 'Polling station not found'}), 404

    ward = db_storage.find_one(Ward, id=polling_station.ward_id)
    constituency = db_storage.find_one(Constituency, id=ward.constituency_id)

    return jsonify({
        'ward': ward.name,
        'constituency': constituency.name
    })

@events_bp.route('/events_data', methods=['GET'])
def events_data():
    events = db_storage.all(Events)
    events_list = [
        {
            'title': event.event_name,
            'start': event.start_date.isoformat(),
            'end': event.end_date.isoformat(),
            'location': event.event_location,
            'description': event.event_description
        }
        for event in events.values()
    ]
    return jsonify(events_list)


@events_bp.route('/calendar', methods=['GET'])
def calendar():
    """Route to view the calendar"""
    return render_template('calendar.html', title='Calendar')
