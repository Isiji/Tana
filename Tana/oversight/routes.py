#!/usr/bin/python3
"""Routes for the oversight"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, send_file
from Tana import db_storage
from Tana.models.secondaryoversight import SecondaryOversight
from Tana.oversight.forms import OversightForm
from flask_login import login_required, current_user
from sqlalchemy.exc import SQLAlchemyError
import logging
from io import BytesIO
from werkzeug.utils import secure_filename

oversight_bp = Blueprint('oversight_bp', __name__)

# used for viewing the oversight
@oversight_bp.route('/view_oversight', methods=['GET'], strict_slashes=False)
def view_oversight():
    """ Route for viewing secondary oversight."""
    oversights_dict = db_storage.all(SecondaryOversight)
    oversights = list(oversights_dict.values())
    return render_template('view_oversight.html', title='View Oversight', oversights=oversights)

# used for adding the oversight
@oversight_bp.route('/add_oversight', methods=['GET', 'POST'])
@login_required
def add_oversight():
    """Route for adding secondary oversight."""
    form = OversightForm()
    if form.validate_on_submit():
        try:
            name = form.name.data
            OAG_Report = form.OAG_Report.data.read() if form.OAG_Report.data else None
            document_filename = secure_filename(form.OAG_Report.data.filename) if form.OAG_Report.data else None
            date_updated = form.date_updated.data
            Ground_report = form.Ground_report.data
            status = form.status.data == 'Approved'
            
            oversight = SecondaryOversight(
                name=name,
                OAG_Report=OAG_Report,
                document_filename=document_filename,
                date_updated=date_updated,
                Ground_report=Ground_report,
                status=status
            )
            
            db_storage.new(oversight)
            db_storage.save()
            
            flash('Oversight has been submitted', 'success')
            return redirect(url_for('oversight_bp.view_oversight'))
        
        except Exception as e:
            db_storage.rollback()  # Rollback in case of errors
            flash(f'An error occurred: {str(e)}', 'danger')
    
    return render_template('oversight_form.html', title='Add Oversight', form=form)


# used for editing the oversight
@oversight_bp.route('/edit_oversight/<int:oversight_id>', methods=['GET', 'POST'], strict_slashes=False)
def edit_oversight(oversight_id):
    """ Route for editing secondary oversight."""
    oversight = db_storage.get(SecondaryOversight, id=oversight_id)
    if not oversight:
        flash(f'Oversight with ID {oversight_id} not found.', 'error')
        return redirect(url_for('oversight_bp.view_oversight'))

    form = OversightForm(obj=oversight)

    if form.validate_on_submit():
        try:
            # Only update the document if a new file is uploaded
            if form.OAG_Report.data:
                oversight.OAG_Report = form.OAG_Report.data.read()
                oversight.OAG_Report_filename = secure_filename(form.OAG_Report.data.filename)

            # Update other fields
            oversight.date_updated = form.date_updated.data
            oversight.Ground_report = form.Ground_report.data
            oversight.status = form.status.data
            # Add any other oversight attributes here as necessary

            db_storage.save()
            flash('Oversight has been updated!', 'success')
            return redirect(url_for('oversight_bp.view_oversight'))
        except Exception as e:
            db_storage.rollback()
            flash(f'An error occurred: {str(e)}', 'danger')

    return render_template('edit_oversight.html', title='Edit Oversight', form=form, oversight=oversight)

# used for deleting the oversight
@oversight_bp.route('/delete_oversight/<int:oversight_id>', methods=['POST'], strict_slashes=False)
def delete_oversight(oversight_id):
    """ Route for deleting secondary oversight."""
    oversight = db_storage.get(SecondaryOversight, oversight_id)
    db_storage.delete(oversight)
    db_storage.save()
    flash('Oversight has been deleted!', 'success')
    return redirect(url_for('oversight_bp.view_oversight'))

# used for downloading the oversight
@oversight_bp.route('/download_oversight/<int:oversight_id>', methods=['GET'])
def download_oversight(oversight_id):
    """Route to download an oversight document."""
    try:
        oversight = db_storage.get(SecondaryOversight, id=oversight_id)
        if not oversight:
            flash(f'Oversight with ID {oversight_id} not found.', 'error')
            return redirect(url_for('oversight_bp.view_oversight'))

        # Ensure document_filename is available
        if not oversight.document_filename:
            flash(f'Document filename not found for oversight with ID {oversight_id}.', 'error')
            return redirect(url_for('oversight_bp.view_oversight'))

        # Ensure OAG_Report is available
        if not oversight.OAG_Report:
            flash(f'Document data not found for oversight with ID {oversight_id}.', 'error')
            return redirect(url_for('oversight_bp.view_oversight'))

        return send_file(BytesIO(oversight.OAG_Report), as_attachment=True, download_name=oversight.document_filename)

    except SQLAlchemyError as e:
        logging.error(f"An SQLAlchemy error occurred: {e}")
        flash(f'An error occurred while downloading the oversight document: {e}', 'error')
        return redirect(url_for('oversight_bp.view_oversight'))

    except Exception as e:
        logging.error(f"An error occurred: {e}")
        flash(f'An error occurred while downloading the oversight document: {e}', 'error')
        return redirect(url_for('oversight_bp.view_oversight'))
