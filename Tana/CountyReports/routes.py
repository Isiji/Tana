from flask import Blueprint, render_template, redirect, url_for, flash, request
from Tana.CountyReports.forms import ReportDataForm, FolderForm
from Tana.models.county_reports import CountyReports
from Tana import DBStorage
from werkzeug.utils import secure_filename
from datetime import datetime
from flask import send_file

report_bp = Blueprint('report_bp', __name__)
db_storage = DBStorage()


@report_bp.route('/create_folder/<parent_id>', methods=['GET', 'POST'])
@report_bp.route('/create_folder', defaults={'parent_id': None}, methods=['GET', 'POST'])
def create_folder(parent_id=None):
    form = FolderForm()
    if form.validate_on_submit():
        # Set optional fields to None or default values
        folder = CountyReports(
            name=form.folder_name.data,
            contact_person=None,  # Optional or default placeholder
            mobile_number=None,  # Optional or default placeholder
            email=None,  # Optional or default placeholder
            report_data=None,  # Placeholder for non-folder entries
            report_data_filename=None,  # Placeholder for non-folder entries
            date_report_uploaded=None,  # Placeholder for non-folder entries
            parent_id=parent_id  # Parent folder ID
        )
        try:
            db_storage.new(folder)
            db_storage.save()
            flash(f'Folder "{folder.name}" created successfully!', 'success')
            return redirect(url_for('report_bp.view_folder', folder_id=folder.id))
        except Exception as e:
            db_storage.rollback()
            flash(f'Error creating folder: {e}', 'danger')
    return render_template('create_folder.html', form=form, parent_id=parent_id)


@report_bp.route('/folder/<int:folder_id>', methods=['GET'])
def view_folder(folder_id):
    folder = db_storage.get(CountyReports, id=folder_id)
    if not folder:
        flash('Folder not found.', 'danger')
        return redirect(url_for('report_bp.view_folders'))

    subfolders = db_storage.filter(CountyReports, CountyReports.parent_id == folder_id)
    reports = db_storage.filter(
        CountyReports,
        CountyReports.parent_id == folder_id,
        CountyReports.report_data_filename.isnot(None)
    )
    return render_template('view_folder.html', folder=folder, subfolders=subfolders, reports=reports)


@report_bp.route('/folder/<int:folder_id>/add_report', methods=['GET', 'POST'])
def add_report(folder_id):
    folder = db_storage.get(CountyReports, folder_id)
    if not folder:
        flash('Folder not found.', 'danger')
        return redirect(url_for('report_bp.view_folders'))

    form = ReportDataForm()
    if form.validate_on_submit():
        report_file = form.report_file.data.read()
        filename = secure_filename(form.report_file.data.filename)

        report = CountyReports(
            name=form.name.data,
            contact_person=form.contact_person.data,
            mobile_number=form.mobile_number.data,
            email=form.email.data,
            report_data=report_file,
            report_data_filename=filename,
            date_report_uploaded=form.date_report_uploaded.data or datetime.utcnow(),
            parent_id=folder_id
        )
        db_storage.new(report)
        db_storage.save()
        flash(f'Report "{report.name}" added to folder "{folder.name}".', 'success')
        return redirect(url_for('report_bp.view_folder', folder_id=folder.id))

    return render_template('add_report.html', form=form, folder=folder)


@report_bp.route('/delete_folder/<int:folder_id>', methods=['POST'])
def delete_folder(folder_id):
    folder = db_storage.get(CountyReports, folder_id)
    if not folder:
        flash('Folder not found.', 'danger')
        return redirect(url_for('report_bp.view_folders'))

    try:
        db_storage.delete(folder)
        db_storage.save()
        flash(f'Folder "{folder.name}" deleted successfully.', 'success')
    except Exception as e:
        db_storage.rollback()
        flash(f'Error deleting folder: {e}', 'danger')

    return redirect(url_for('report_bp.view_folders'))


@report_bp.route('/delete_report/<int:report_id>', methods=['POST'])
def delete_report(report_id):
    report = db_storage.get(CountyReports, report_id)
    if not report:
        flash('Report not found.', 'danger')
        return redirect(url_for('report_bp.view_folders'))

    try:
        folder_id = report.parent_id
        db_storage.delete(report)
        db_storage.save()
        flash(f'Report "{report.name}" deleted successfully.', 'success')
    except Exception as e:
        db_storage.rollback()
        flash(f'Error deleting report: {e}', 'danger')

    return redirect(url_for('report_bp.view_folder', folder_id=folder_id))


@report_bp.route('/view_folders', methods=['GET'])
def view_folders():
    try:
        folders = db_storage.filter(CountyReports, CountyReports.parent_id == None)
        return render_template('view_folders.html', folders=folders)
    except Exception as e:
        print(f"An error occurred: {e}")
        flash('An error occurred while fetching folders.', 'danger')
        return redirect(url_for('report_bp.view_folders'))

