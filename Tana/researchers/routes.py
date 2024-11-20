from flask import Blueprint, render_template, request, redirect, url_for, flash, send_file
from flask_login import login_required
from io import BytesIO
from Tana.models.committee_records import CommitteeRecord
from Tana.researchers.forms import CommitteeRecordForm
from Tana import db_storage
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.utils import secure_filename
import logging

# Define the blueprint
researchers = Blueprint('researchers', __name__)

# Hardcoded list of committees
COMMITTEES = [
    {'id': 1, 'name': 'Energy Committee'},
    {'id': 2, 'name': 'Delegated Legislation Committee'},
    {'id': 3, 'name': 'Pan African Parliament Committee'},
    {'id': 4, 'name': 'Bunge Sports Club'},
    {'id': 5, 'name': 'CPAC'},
    {'id': 6, 'name': 'CPIC'},
]


# Define the routes
@researchers.route('/researcher_dashboard', methods=['GET'])
@login_required
def researcher_dashboard():
    """ Route to display the researcher dashboard """
    return render_template('researcher.html', title='Researcher Dashboard')



# Define the routes
@researchers.route('/committees', methods=['GET'])
@login_required
def committees():
    """ Route to display the committees """
    form = CommitteeRecordForm()
    return render_template('committees.html', title='Committees', form=form, committees=COMMITTEES)

# Define the route for the committee records
@researchers.route('/committee/<int:committee_id>/records', methods=['GET'])
@login_required
def committee_records(committee_id):
    """ Route to display the records of a committee """
    records = db_storage.filter(CommitteeRecord, CommitteeRecord.committee_id == committee_id)
    return render_template('committee_records.html', records=records, committee_id=committee_id)

# Define the route for a specific committee
@researchers.route('/committee/<int:committee_id>', methods=['GET', 'POST'])
@login_required
def committee(committee_id):
    """ Route to display a specific committee """
    committee = next((c for c in COMMITTEES if c['id'] == committee_id), None)
    if not committee:
        flash('Committee not found.', 'danger')
        return redirect(url_for('researchers.committees'))

    form = CommitteeRecordForm()
    if form.validate_on_submit():
        document = form.document.data.read() if form.document.data else None
        recommendations = form.recommendations.data.read() if form.recommendations.data else None
        document_filename = secure_filename(form.document.data.filename) if form.document.data else None
        recommendations_filename = secure_filename(form.recommendations.data.filename) if form.recommendations.data else None

        record = CommitteeRecord(
            serial_number=form.serial_number.data,
            date=form.date.data,
            title=form.title.data,
            document=document,
            recommendations=recommendations,
            document_filename=document_filename,
            recommendations_filename=recommendations_filename,
            committee_id=committee_id
        )
        db_storage.new(record)
        db_storage.save()
        flash('Record added successfully!', 'success')
        return redirect(url_for('researchers.committee_records', committee_id=committee_id))

    records = db_storage.filter(CommitteeRecord, CommitteeRecord.committee_id == committee_id)
    return render_template('committee.html', committee=committee, records=records, form=form)

# Define the route to download a document
@researchers.route('/download_document/<int:record_id>', methods=['GET'])
@login_required
def download_document(record_id):
    """ Route to download the document """
    try:
        record = db_storage.get(CommitteeRecord, id=record_id)
        
        if not record:
            flash(f'Record with ID {record_id} not found.', 'error')
            return redirect(url_for('researchers.committee_records', committee_id=record_id))

        if record.document:
            filename = record.document_filename or 'document.pdf'  # Use document_filename
            return send_file(
                BytesIO(record.document),
                as_attachment=True,
                download_name=filename  # Updated argument to `download_name`
            )
        else:
            flash('Document not found.', 'danger')
            return redirect(url_for('researchers.committee_records', committee_id=record_id))

    except SQLAlchemyError as e:
        logging.error(f"An SQLAlchemy error occurred: {e}")
        flash(f'An error occurred while downloading the document: {e}', 'error')
        return redirect(url_for('researchers.committee_records', committee_id=record_id))

    except Exception as e:
        logging.error(f"An error occurred: {e}")
        flash(f'An error occurred while downloading the document: {e}', 'error')
        return redirect(url_for('researchers.committee_records', committee_id=record_id))


# Define the route to download recommendations
@researchers.route('/download_recommendations/<int:record_id>', methods=['GET'])
@login_required
def download_recommendations(record_id):
    """ Route to download the recommendations"""
    try:
        record = db_storage.get(CommitteeRecord, id=record_id)
        
        if not record:
            flash(f'Record with ID {record_id} not found.', 'danger')
            return redirect(url_for('researchers.committee_records', committee_id=record_id))
        
        if record.recommendations:
            filename = record.recommendations_filename or 'recommendations.pdf'  # Use recommendations_filename
            return send_file(
                BytesIO(record.recommendations),
                as_attachment=True,
                download_name=filename  # Updated argument to `download_name`
            )
        else:
            flash('Recommendations not found.', 'danger')
            return redirect(url_for('researchers.committee_records', committee_id=record_id))

    except SQLAlchemyError as e:
        logging.error(f"An SQLAlchemy error occurred: {e}")
        flash(f'An error occurred while downloading the recommendations: {e}', 'error')
        return redirect(url_for('researchers.committee_records', committee_id=record_id))

    except Exception as e:
        logging.error(f"An error occurred: {e}")
        flash(f'An error occurred while downloading the recommendations: {e}', 'error')
        return redirect(url_for('researchers.committee_records', committee_id=record_id))
