#!/usr/bin/python3
"""Routes for the app"""
from flask import Blueprint, current_app, jsonify, request, render_template, redirect, url_for, flash
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
@events_bp.route('/add_event', methods=['GET', 'POST'])
def add_event():
    form = EventForm()
    print("populating polling station choices")
    
    # Populate polling station choices
    polling_stations = db_storage.all(PollingStation)
    form.polling_station_name.choices = [(station.id, station.name) for station in polling_stations.values()]
    print("waiting to validate the form")
    
    if form.validate_on_submit():
        print("form is validated")
        polling_station_id = form.polling_station_name.data
        polling_station = db_storage.get(PollingStation, id=polling_station_id)
        print(f"Polling Station: {polling_station}")  # Debugging
        
        if not polling_station:
            form.polling_station_name.errors.append('Selected polling station is invalid.')
            return render_template('add_event.html', form=form)

        event = Events(
            event_name=form.event_name.data,
            impact_level=form.impact_level.data,
            event_leader=form.event_leader.data,
            event_location=form.event_location.data,
            contact_person=form.contact_person.data,
            event_description=form.event_description.data,
            start_date=form.start_date.data,
            end_date=form.end_date.data,
            polling_station_id=polling_station_id,
            user_id=current_user.id
        )
        print("next is to save the event")
        db_storage.new(event)
        db_storage.save()
        print("event saved")
        flash('Event added successfully', 'success')
    # Debugging output for form errors
    print("Form Errors:", form.errors)
    return render_template('add_event.html', form=form)


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

# create a route to delete an event 
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

# create a route to edit an event
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

#route to geyt all polling stations
@events_bp.route('/get_all_polling_stations', methods=['GET'])
def get_all_polling_stations():
    """Route to get all polling station names"""
    polling_stations = db_storage.all(PollingStation).values()
    polling_station_names = [station.name for station in polling_stations]
    return jsonify({'pollingStations': polling_station_names})

#route to get polling station info
@events_bp.route('/get_polling_station_info', methods=['GET'])
def get_polling_station_info():
    """Route to get polling station information"""
    polling_station_name = request.args.get('polling_station')
    print(f"Polling Station Name: {polling_station_name}")  # Debugging

    if not polling_station_name:
        return jsonify({'error': 'Polling station name is required'}), 400

    polling_station = db_storage.find_one(PollingStation, name=polling_station_name)
    print(f"Polling Station Found: {polling_station}")  # Debugging

    if not polling_station:
        return jsonify({'error': 'Polling station not found'}), 404

    ward = db_storage.find_one(Ward, id=polling_station.ward_id)
    print(f"Ward Found: {ward}")  # Debugging

    if not ward:
        return jsonify({'error': 'Ward not found'}), 404

    constituency = db_storage.find_one(Constituency, id=ward.constituency_id)
    print(f"Constituency Found: {constituency}")  # Debugging

    if not constituency:
        return jsonify({'error': 'Constituency not found'}), 404

    return jsonify({
        'ward': ward.name,
        'constituency': constituency.name
    })

#route to get events data
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

#route to view the calendar
@events_bp.route('/calendar', methods=['GET'])
def calendar():
    """Route to view the calendar"""
    return render_template('calendar.html', title='Calendar')
