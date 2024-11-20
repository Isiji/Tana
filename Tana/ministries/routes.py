from flask import Blueprint, render_template, redirect, url_for, flash
from flask import request
from Tana.models.ministries import Ministries
from Tana.ministries.forms import MinistryForm
from Tana import DBStorage
from werkzeug.utils import secure_filename
import os
import logging
from io import BytesIO
from flask import send_file
from sqlalchemy.exc import SQLAlchemyError

logging.basicConfig(level=logging.DEBUG,  # Adjust level as needed
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[
                        logging.FileHandler('app.log'),  # Log to a file
                        logging.StreamHandler()  # Also log to console
                    ])

ministry_bp = Blueprint('ministries', __name__)

# Initialize database storage
db_storage = DBStorage()

@ministry_bp.route('/add_ministry', methods=['GET', 'POST'])
def add_ministry():
    """Route for adding ministries"""
    form = MinistryForm()
    if form.validate_on_submit():
        try:
            # Handle main document
            document_data = None
            document_filename = None
            if form.documents_presented.data:
                document_data = form.documents_presented.data.read()
                document_filename = secure_filename(form.documents_presented.data.filename)
                form.documents_presented.data.seek(0)  # Reset file pointer after reading

            # Create and save ministry instance
            ministry = Ministries(
                name=form.name.data,
                contact_person=form.contact_person.data,
                mobile_number=form.mobile_number.data,
                email=form.email.data,
                documents_presented=document_data,
                documents_filename=document_filename,
                date_documents_presented=form.date_documents_presented.data
            )

            db_storage.new(ministry)
            print("ministry has been added")
            print("now proceeding to save the ministry")
            db_storage.save()
            flash('Ministry has been added!', 'success')
            logging.info(f"Ministry '{ministry.name}' added to the database.")
            return redirect(url_for('ministries.list_ministries'))
        except Exception as e:
            db_storage.rollback()
            flash(f'An error occurred while adding the ministry: {str(e)}', 'danger')
            logging.error(f"Failed to add ministry '{form.name.data}'. Error: {str(e)}")
    else:
        logging.debug("Form validation failed")
        for field, errors in form.errors.items():
            for error in errors:
                logging.debug(f"Error in {field}: {error}")

    return render_template('add_ministry.html', title='Add Ministry', form=form)

@ministry_bp.route('/ministries')
def list_ministries():
    ministries = db_storage.all(Ministries)
    return render_template('list_ministries.html', ministries=ministries)

@ministry_bp.route('/ministries/edit/<int:id>', methods=['GET', 'POST'])
def edit_ministry(id):
    ministry = db_storage.get(Ministries, id=id)
    if not ministry:
        flash('Ministry not found.', 'error')
        return redirect(url_for('ministries.list_ministries'))
    
    form = MinistryForm(obj=ministry)
    
    if form.validate_on_submit():
        # Update ministry details
        ministry.name = form.name.data
        ministry.contact_person = form.contact_person.data
        ministry.mobile_number = form.mobile_number.data
        ministry.email = form.email.data
        ministry.documents_presented = form.documents_presented.data
        ministry.date_documents_presented = form.date_documents_presented.data

        # Commit changes to the database
        db_storage.save()
        flash('Ministry updated successfully!', 'success')
        return redirect(url_for('ministries.list_ministries'))
    
    return render_template('edit_ministry.html', form=form, ministry=ministry)

@ministry_bp.route('/ministries/delete/<int:id>', methods=['POST'])
def delete_ministry(id):
    """Delete a ministry"""
    ministry = db_storage.get(Ministries, id=id)
    if not ministry:
        flash('Ministry not found.', 'danger')
        return redirect(url_for('ministries.list_ministries'))
    
    try:
        db_storage.delete(ministry)
        db_storage.save()
        flash('Ministry deleted successfully!', 'success')
    except Exception as e:
        db_storage.rollback()
        flash(f'Error deleting ministry: {e}', 'danger')

    return redirect(url_for('ministries.list_ministries'))

#route to download the document
@ministry_bp.route('/download_ministry/<int:ministry_id>', methods=['GET'])
def download_ministry(ministry_id):
    """Route to download a ministry document"""
    try:
        ministry = db_storage.get(Ministries, id=ministry_id)
        if not ministry:
            flash(f'Ministry with ID {ministry_id} not found.', 'error')
            return redirect(url_for('ministries.ministries_list'))

        if not ministry.documents_presented:
            flash('No document available for download.', 'error')
            return redirect(url_for('ministries.ministries_list'))

        return send_file(BytesIO(ministry.documents_presented),
                         as_attachment=True,
                         download_name=ministry.documents_filename)

    except SQLAlchemyError as e:
        logging.error(f"An SQLAlchemy error occurred: {e}")
        flash(f'An error occurred while downloading the document: {e}', 'error')
        return redirect(url_for('ministries.ministries_list'))

    except Exception as e:
        logging.error(f"An error occurred: {e}")
        flash(f'An error occurred while downloading the document: {e}', 'error')
        return redirect(url_for('ministries.ministries_list'))