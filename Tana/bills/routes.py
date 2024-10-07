#!/usr/bin/python3
"""Bills routes"""
from flask import render_template, flash, redirect, url_for, request, Blueprint
from Tana import db_storage
from Tana.models.bills import Bills
from Tana.bills.forms import BillsForm, Emptyform
import logging
from io import BytesIO
from flask import send_file
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.utils import secure_filename
import logging


bills_bp = Blueprint('bills', __name__)

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Route for adding a bill
@bills_bp.route('/add_bill', methods=['GET', 'POST'], strict_slashes=False)
def add_bill():
    """ Route for adding a bill """
    print("add bill route has been hit")
    form = BillsForm()
    if form.validate_on_submit():
        print("form has been validated")
        try:
            document_data = form.document.data.read()
            document_filename = secure_filename(form.document.data.filename)

            bill = Bills(
                name=form.name.data,
                submitted_date=form.submitted_date.data,
                first_reading=form.first_reading.data,
                first_reading_date=form.first_reading_date.data if form.first_reading_date.data else None,
                second_reading=form.second_reading.data,
                second_reading_date=form.second_reading_date.data if form.second_reading_date.data else None,
                third_reading=form.third_reading.data,
                third_reading_date=form.third_reading_date.data if form.third_reading_date.data else None,
                presidential_assent=form.presidential_assent.data,
                presidential_assent_date=form.presidential_assent_date.data if form.presidential_assent_date.data else None,
                commencement=form.commencement.data,
                commencement_date=form.commencement_date.data if form.commencement_date.data else None,
                document=document_data,
                filename=document_filename
            )
            
            logging.debug(f"Attempting to add bill: {bill}")
            db_storage.new(bill)
            db_storage.save()
            flash('Bill has been added!', 'success')
            return redirect(url_for('bills.view_bills'))
        except Exception as e:
            db_storage.rollback()
            logging.error(f"Error adding bill: {e}")
            print(f"Error adding bill: {e}")
            flash('An error occurred while adding the bill. Please try again.', 'danger')
            logging.debug(f"Bill data: {bill}")
            logging.debug(f"Form data: {form.data}")
    else:
        print("Form validation failed")
        for field, errors in form.errors.items():
            for error in errors:
                print(f"Error in {field}: {error}")
    return render_template('add_bill.html', form=form)


# Route for viewing all bills
@bills_bp.route('/view_bills', methods=['GET'], strict_slashes=False)
def view_bills():
    """ Route for viewing all bills """
    bills_dict = db_storage.all(Bills)
    bills = list(bills_dict.values())
    form = Emptyform()  # Empty form for CSRF token
    return render_template('view_bills.html', bills=bills, form=form)

# Route for editing a bill
@bills_bp.route('/edit_bill/<int:bill_id>', methods=['GET', 'POST'], strict_slashes=False)
def edit_bill(bill_id):
    """ Route for editing a bill """
    bill = db_storage.get(Bills, id=bill_id)
    if not bill:
        flash(f'Bill with ID {bill_id} not found.', 'error')
        return redirect(url_for('bills.view_bills'))

    form = BillsForm(obj=bill)
    if form.validate_on_submit():
        try:
            # Only update the document if a new file is uploaded
            if form.document.data:
                bill.document = form.document.data.read()
                bill.filename = secure_filename(form.document.data.filename)
            
            # Update other fields
            bill.name = form.name.data
            bill.submitted_date = form.submitted_date.data
            bill.first_reading = form.first_reading.data
            bill.first_reading_date = form.first_reading_date.data
            bill.second_reading = form.second_reading.data
            bill.second_reading_date = form.second_reading_date.data
            bill.third_reading = form.third_reading.data
            bill.third_reading_date = form.third_reading_date.data
            bill.presidential_assent = form.presidential_assent.data
            bill.presidential_assent_date = form.presidential_assent_date.data
            bill.commencement = form.commencement.data
            bill.commencement_date = form.commencement_date.data
            
            db_storage.save()
            flash('Bill has been updated!', 'success')
            logger.info(f'Bill "{bill.name}" updated successfully.')
            return redirect(url_for('bills.view_bills'))
        except Exception as e:
            db_storage.rollback()
            flash(f'An error occurred: {str(e)}', 'danger')
            logger.error(f'Error updating bill: {str(e)}')
    
    return render_template('edit_bill.html', title='Edit Bill', form=form, bill=bill)


# Route for deleting a bill
@bills_bp.route('/delete_bill/<int:bill_id>', methods=['POST'], strict_slashes=False)
def delete_bill(bill_id):
    """ Delete a bill """
    bill = db_storage.get(Bills, id=bill_id)
    if not bill:
        flash('Bill not found', 'danger')
        return redirect(url_for('bills.view_bills'))
    
    db_storage.delete(bill)
    db_storage.save()
    flash('Bill has been deleted!', 'success')
    return redirect(url_for('bills.view_bills'))


# Route to download a bill
@bills_bp.route('/download_bill/<int:bill_id>', methods=['GET'])
def download_bill(bill_id):
    """Route to download a bill."""
    try:
        bill = db_storage.get(Bills, id=bill_id)
        if not bill:
            flash(f'Bill with ID {bill_id} not found.', 'error')
            return redirect(url_for('bills.view_bills'))

        return send_file(BytesIO(bill.document), as_attachment=True, download_name=bill.filename)

    except SQLAlchemyError as e:
        logging.error(f"An SQLAlchemy error occurred: {e}")
        flash(f'An error occurred while downloading the bill: {e}', 'error')
        return redirect(url_for('bills.view_bills'))

    except Exception as e:
        logging.error(f"An error occurred: {e}")
        flash(f'An error occurred while downloading the bill: {e}', 'error')
        return redirect(url_for('bills.view_bills'))