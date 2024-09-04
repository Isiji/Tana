from flask import Blueprint, render_template, redirect, url_for, flash
from flask import request
from Tana.models.ministries import Ministries
from Tana.ministries.forms import MinistryForm
from Tana import DBStorage
from werkzeug.utils import secure_filename
import os
import logging

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
    """ Route for adding a ministry """
    print("add ministry route has been hit")
    form = MinistryForm()
    if form.validate_on_submit():
        print("form has been validated")
        ministry = None
        try:
            documents = form.documents_presented.data
            documents_filename = None
            if documents:
                documents_filename = secure_filename(documents.filename)
                documents.save(os.path.join('uploads', documents_filename))  # Save file to the uploads folder

            ministry = Ministries(
                name=form.name.data,
                contact_person=form.contact_person.data,
                mobile_number=form.mobile_number.data,
                email=form.email.data,
                documents_presented=open(os.path.join('uploads', documents_filename), 'rb').read() if documents else None,
                documents_filename=documents_filename,
                date_documents_presented=form.date_documents_presented.data
            )

            logging.debug(f"Attempting to add ministry: {ministry}")
            db_storage.new(ministry)
            db_storage.save()
            flash('Ministry added successfully!', 'success')
            return redirect(url_for('ministries.add_ministry'))
        except Exception as e:
            db_storage.rollback()
            logging.error(f"Error adding ministry: {e}")
            print(f"Error adding ministry: {e}")
            flash('An error occurred while adding the ministry. Please try again.', 'danger')
            if ministry:
                logging.debug(f"Ministry data: {ministry}")
            logging.debug(f"Form data: {form.data}")
    else:
        print("Form validation failed")
        for field, errors in form.errors.items():
            for error in errors:
                print(f"Error in {field}: {error}")

    return render_template('add_ministry.html', form=form)
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
    
    return render_template('edit_ministry.html', form=form)

@ministry_bp.route('/ministries/delete/<int:id>', methods=['POST'])
def delete_ministry(id):
    ministry = db_storage.get(Ministries, id=id)
    if ministry:
        db_storage.delete(ministry)
        db_storage.save()
        flash('Ministry deleted successfully!', 'success')
    else:
        flash('Ministry not found.', 'error')
    
    return redirect(url_for('ministries.list_ministries'))
