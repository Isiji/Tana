#!/usr/bin/python3
"""routes for the coordinators"""
from flask import Blueprint, render_template, request, redirect, url_for, flash
from Tana.models.members import users
from Tana.models.roles import UserRole
from Tana import db_storage, bcrypt
from Tana.models.offices import Offices
from flask_login import login_user, current_user, logout_user, login_required, LoginManager
from Tana.coordinators.forms import CountyOfficeUpdateForm
from Tana.models.county_office_update import CountyOfficeUpdate

coordinators = Blueprint('coordinators', __name__)

#route for the coordinator dashboard
@coordinators.route('/coordinator_dashboard')
@login_required
def coordinator_dashboard():
    """Route for the coordinator dashboard"""
    return render_template('coordinator.html', title='Coordinator Dashboard')

#route for adding a county office update
@coordinators.route('/add_county_office_update', methods=['GET', 'POST'])
@login_required
def add_county_office_update():
    """Route to add a county office update."""
    form = CountyOfficeUpdateForm()
    if form.validate_on_submit():
        update = CountyOfficeUpdate(
            date=form.date.data,
            party_involved=form.party_involved.data,
            issues=form.issues.data,
            delegation=form.delegation.data,
            contact_person=form.contact_person.data,
            action_taken=form.action_taken.data
        )
        db_storage.new(update)
        db_storage.save()
        flash('County office update has been submitted!', 'success')
        return redirect(url_for('coordinators.view_county_office_updates'))
    return render_template('county_office_update_form.html', title='Add County Office Update', form=form)

#route for viewing all county office updates
@coordinators.route('/view_county_office_updates', methods=['GET'])
@login_required
def view_county_office_updates():
    """Route to view all county office updates."""
    updates_dict = db_storage.all(CountyOfficeUpdate)
    updates = list(updates_dict.values())
    return render_template('view_county_office_updates.html', title='View County Office Updates', updates=updates)

#route for editing a county office update
@coordinators.route('/edit_county_office_update/<int:update_id>', methods=['GET', 'POST'])
@login_required
def edit_county_office_update(update_id):
    """Route to edit a county office update."""
    update = db_storage.get(CountyOfficeUpdate, id=update_id)
    if not update:
        flash('County office update not found.', 'error')
        return redirect(url_for('coordinators.view_county_office_updates'))

    form = CountyOfficeUpdateForm(obj=update)
    if form.validate_on_submit():
        update.date = form.date.data
        update.party_involved = form.party_involved.data
        update.issues = form.issues.data
        update.delegation = form.delegation.data
        update.contact_person = form.contact_person.data
        update.action_taken = form.action_taken.data
        db_storage.save()
        flash('County office update has been updated!', 'success')
        return redirect(url_for('coordinators.view_county_office_updates'))

    return render_template('county_office_update_form.html', title='Edit County Office Update', form=form)

#route for deleting a county office update
@coordinators.route('/delete_county_office_update/<int:update_id>', methods=['POST'])
@login_required
def delete_county_office_update(update_id):
    """Route to delete a county office update."""
    update = db_storage.get(CountyOfficeUpdate, id=update_id)
    if not update:
        flash('County office update not found.', 'error')
        return redirect(url_for('coordinators.view_county_office_updates'))

    db_storage.delete(update)
    db_storage.save()
    flash('County office update has been deleted!', 'success')
    return redirect(url_for('coordinators.view_county_office_updates'))
