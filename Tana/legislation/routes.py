#!/usr/bin/python3
"""Routes for the legislation"""
from flask import Blueprint, render_template, request, redirect, url_for, flash
from Tana.models.members import users
from Tana.models.roles import UserRole
from Tana import db_storage, bcrypt
from Tana.models.offices import Offices
from flask_login import login_user, current_user, logout_user, login_required, LoginManager
from Tana.models.motions import Motions
from Tana.models.questions import Questions
from Tana.models.statements import Statements
from Tana.legislation.forms import MotionsForm, StatementsForm, LegislationForm, QuestionsForm
import logging
from datetime import datetime
from io import BytesIO
from flask import send_file
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.utils import secure_filename

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


legislation_bp = Blueprint('legislation', __name__)

#route for the legislation
@legislation_bp.route('/legislation')
def legislation():
    """route for the legislation"""
    return render_template('legislation.html', title='Legislation')

#route for adding a motion using addmotion form
@legislation_bp.route('/add_motion', methods=['GET', 'POST'])
def add_motion():
    """Route for adding motions"""
    form = MotionsForm()
    if form.validate_on_submit():
        try:
            document_data = form.document.data.read()
            document_filename = secure_filename(form.document.data.filename)
            
            follow_up_document_data = None
            follow_up_document_filename = None
            if form.follow_up_document.data:
                follow_up_document_data = form.follow_up_document.data.read()
                follow_up_document_filename = secure_filename(form.follow_up_document.data.filename)
            
            motion = Motions(
                name=form.name.data,
                document=document_data,
                filename=document_filename,
                follow_up_document=follow_up_document_data,
                follow_up_filename=follow_up_document_filename,
                date=form.date.data,
                status=form.status.data,
                created_at=datetime.utcnow()
            )
            db_storage.new(motion)
            db_storage.save()
            flash('Motion has been created!', 'success')
            logger.info(f"Motion '{motion.name}' added to the database.")
            return redirect(url_for('legislation.motions'))
        except Exception as e:
            db_storage.rollback()
            flash(f'An error occurred: {str(e)}', 'danger')
            logger.error(f"Failed to add motion '{form.name.data}' to the database. Error: {str(e)}")
    return render_template('add_motion.html', title='Add Motion', form=form)


#route for viewing motions
@legislation_bp.route('/motions', methods=['GET'])
def motions():
    """ route for viewing motions"""
    motions_dict = db_storage.all(Motions)
    motions = list(motions_dict.values())
    return render_template('motions.html', title='View Motions', motions=motions)

#create function to delete motions
@legislation_bp.route('/delete_motion/<int:motion_id>', methods=['POST'], strict_slashes=False)
def delete_motion(motion_id):
    """ Route for deleting a motion """
    motion = db_storage.get(Motions, id=motion_id)
    db_storage.delete(motion)
    db_storage.save()
    flash('Motion has been deleted!', 'success')
    return redirect(url_for('legislation.motions'))

#create function to edit motions
@legislation_bp.route('/edit_motion/<int:motion_id>', methods=['GET', 'POST'], strict_slashes=False)
def edit_motion(motion_id):
    """ Route for editing motions """
    motion = db_storage.get(Motions, id=motion_id)
    if not motion:
        flash(f'Motion with ID {motion_id} not found.', 'error')
        return redirect(url_for('legislation.view_motions'))
    
    form = MotionsForm(obj=motion)
    if form.validate_on_submit():
        try:
            motion.name = form.name.data
            motion.date = form.date.data
            motion.status = form.status.data
            if form.document.data:
                motion.document = form.document.data.read()
                motion.filename = secure_filename(form.document.data.filename)
            db_storage.save()
            flash('Motion has been updated!', 'success')
            logging.info(f"Motion '{motion.name}' (ID: {motion_id}) has been updated successfully.")
            return redirect(url_for('legislation.view_motions'))
        except Exception as e:
            db_storage.rollback()
            logging.error(f"Error editing motion ID {motion_id}: {e}")
            flash('An error occurred while editing the motion. Please try again.', 'danger')
            logging.debug(f"Form data: {form.data}")
    else:
        logging.debug(f"Form validation errors: {form.errors}")

    return render_template('edit_motion.html', title='Edit Motion', form=form, motion=motion)


#route for viewing motions
@legislation_bp.route('/view_motions', methods=['GET'])
def view_motions():
    """ route for viewing motions"""
    motions_dict = db_storage.all(Motions)
    motions = list(motions_dict.values())
    return render_template('motions.html', title='View Motions', motions=motions)

#route for viewing statements
@legislation_bp.route('/statements', methods=['GET', 'POST'])
def statements():
    """route for the statements"""
    return render_template('view_statements.html', title='Statements')

#create route for adding statements
@legislation_bp.route('/add_statement', methods=['GET', 'POST'])
def add_statement():
    """Route for adding statements"""
    form = StatementsForm()
    
    if form.validate_on_submit():
        try:
            # Handle file uploads
            document_data = form.document.data.read() if form.document.data else None
            document_filename = secure_filename(form.document.data.filename) if form.document.data else None
            follow_up_letter_data = form.follow_up_letter.data.read() if form.follow_up_letter.data else None

            # Create a new statement instance
            statement = Statements(
                name=form.name.data,  # Ensure you include the name field
                document=document_data,
                follow_up_letter=follow_up_letter_data,
                date=form.date.data,
                status=form.status.data,
                filename=document_filename,
                created_at=datetime.utcnow()
            )

            # Save the statement to the database
            db_storage.new(statement)
            db_storage.save()
            flash('Statement has been created!', 'success')
            logger.info(f'Statement "{statement.name}" created successfully.')
            return redirect(url_for('legislation.view_statements'))
        except Exception as e:
            db_storage.rollback()
            flash(f'An error occurred: {str(e)}', 'danger')
            logger.error(f'Error creating statement: {str(e)}')
    
    return render_template('add_statement.html', title='Add Statement', form=form)

#create route to view statements
@legislation_bp.route('/view_statements', methods=['GET'])
def view_statements():
    """ route for viewing statements"""
    statements_dict = db_storage.all(Statements)
    statements = list(statements_dict.values())
    return render_template('view_statements.html', title='View Statements', statements=statements)

#create function to edit statements
@legislation_bp.route('/edit_statement/<int:statement_id>', methods=['GET', 'POST'])
def edit_statement(statement_id):
    """ Route for editing statements """
    statement = db_storage.get(Statements, id=statement_id)
    if not statement:
        flash(f'Statement with ID {statement_id} not found.', 'error')
        return redirect(url_for('legislation.view_statements'))

    form = StatementsForm(obj=statement)
    if form.validate_on_submit():
        try:
            if form.document.data:
                statement.document = form.document.data.read()
                statement.filename = secure_filename(form.document.data.filename)

            if form.follow_up_letter.data:
                statement.follow_up_letter = form.follow_up_letter.data.read()

            statement.name = form.name.data
            statement.date = form.date.data
            statement.status = form.status.data
            
            db_storage.save()
            flash('Statement has been updated!', 'success')
            logger.info(f'Statement "{statement.name}" updated successfully.')
            return redirect(url_for('legislation.view_statements'))
        except Exception as e:
            db_storage.rollback()
            flash(f'An error occurred: {str(e)}', 'danger')
            logger.error(f'Error updating statement: {str(e)}')

    return render_template('edit_statement.html', title='Edit Statement', form=form, statement=statement)



#create function to delete statements
@legislation_bp.route('/delete_statement/<int:statement_id>', methods=['POST'], strict_slashes=False)
def delete_statement(statement_id):
    """ Route for deleting a statement """
    statement = db_storage.get(Statements, id=statement_id)
    db_storage.delete(statement)
    db_storage.save()
    flash('Statement has been deleted!', 'success')
    return redirect(url_for('legislation.view_statements'))


#create route for questions
@legislation_bp.route('/questions', methods=['GET', 'POST'])
@login_required
def questions():
    """route for the questions"""
    return render_template('view_questions.html', title='Questions')

#create route to add questions
@legislation_bp.route('/add_question', methods=['GET', 'POST'])
def add_question():
    """ Route for adding questions """
    form = QuestionsForm()
    if form.validate_on_submit():
        try:
            file_data = form.document.data.read() if form.document.data else None
            filename = secure_filename(form.document.data.filename) if form.document.data else None

            new_question = Questions(
                name=form.name.data,
                document=file_data,
                filename=filename,
                date=form.date.data,
                status=form.status.data,
                created_at=datetime.utcnow()
            )
            db_storage.new(new_question)
            db_storage.save()  # Commit the session to save the new question
            flash('Question added successfully!', 'success')
            logger.info(f"Question '{new_question.name}' added to the database.")
            return redirect(url_for('legislation.view_questions'))
        except Exception as e:
            db_storage.rollback()  # Rollback in case of error
            flash(f'An error occurred: {e}', 'danger')
            logger.error(f"Failed to add question '{new_question.name}' to the database. Error: {e}")
    else:
        # Log form errors
        logger.error(f"Form validation failed: {form.errors}")
    return render_template('add_question.html', form=form)



#route to view questions
@legislation_bp.route('/view_questions', methods=['GET', 'POST'])
def view_questions():
    '''route for viewing questions'''
    questions_dict = db_storage.all(Questions)
    questions = list(questions_dict.values())
    return render_template('view_questions.html', title='View Questions', questions=questions)

#create function to edit questions
@legislation_bp.route('/edit_question/<int:question_id>', methods=['GET', 'POST'], strict_slashes=False)
def edit_question(question_id):
    """ Route for editing questions """
    question = db_storage.get(Questions, id=question_id)
    form = QuestionsForm(obj=question)
    if form.validate_on_submit():
        try:
            question.name = form.name.data
            question.date = form.date.data
            question.status = form.status.data
            if form.document.data:
                question.document = form.document.data.read()
            db_storage.save()
            flash('Question has been updated!', 'success')
            return redirect(url_for('legislation.view_questions'))
        except Exception as e:
            logging.error(f"Error editing statement: {e}")
            flash('An error occurred while editing the question. Please try again.', 'danger')
    return render_template('edit_question.html', title='Edit Question', form=form, question=question)

#create function to delete statements
@legislation_bp.route('/delete_question/<int:question_id>', methods=['POST'], strict_slashes=False)
def delete_question(question_id):
    """ Route for deleting a question """  
    question = db_storage.get(Questions, id=question_id)
    db_storage.delete(question)
    db_storage.save()
    flash('Question has been deleted!', 'success')
    return redirect(url_for('legislation.view_questions'))


#create a route for functions
@legislation_bp.route('/functions', methods=['GET', 'POST'])
def functions():
    """route for the functions"""
    return render_template('functions.html', title='Functions')

#roue for downloading motion document
@legislation_bp.route('/download_motion/<int:motion_id>', methods=['GET'])
def download_motion(motion_id):
    """ Route to download a motion document """
    try:
        motion = db_storage.get(Motions, id=motion_id)
        if not motion:
            flash(f'Motion with ID {motion_id} not found.', 'error')
            return redirect(url_for('legislation.view_motions'))

        return send_file(BytesIO(motion.document), as_attachment=True, download_name=motion.filename)

    except SQLAlchemyError as e:
        logging.error(f"An SQLAlchemy error occurred: {e}")
        flash(f'An error occurred while downloading the motion: {e}', 'error')
        return redirect(url_for('legislation.view_motions'))

    except Exception as e:
        logging.error(f"An error occurred: {e}")
        flash(f'An error occurred while downloading the motion: {e}', 'error')
        return redirect(url_for('legislation.view_motions'))

#route for downloading follow up document    
@legislation_bp.route('/download_follow_up_document/<int:motion_id>', methods=['GET'])
def download_follow_up_document(motion_id):
    ''' Route to download a motion follow-up document '''
    try:
        motion = db_storage.get(Motions, id=motion_id)
        if not motion or not motion.follow_up_document:
            flash(f'Motion with ID {motion_id} or its follow-up document not found.', 'error')
            return redirect(url_for('legislation.view_motions'))

        return send_file(BytesIO(motion.follow_up_document), as_attachment=True, download_name=f"follow_up_{motion.filename}")

    except SQLAlchemyError as e:
        logging.error(f"An SQLAlchemy error occurred: {e}")
        flash(f'An error occurred while downloading the follow-up document: {e}', 'error')
        return redirect(url_for('legislation.view_motions'))

    except Exception as e:
        logging.error(f"An error occurred: {e}")
        flash(f'An error occurred while downloading the follow-up document: {e}', 'error')
        return redirect(url_for('legislation.view_motions'))

# route for downloading statement document
@legislation_bp.route('/download_statement/<int:statement_id>', methods=['GET'])
def download_statement(statement_id):
    """ Route to download a statement document"""
    try:
        statement = db_storage.get(Statements, id=statement_id)
        if not statement:
            flash(f'Statement with ID {statement_id} not found.', 'error')
            return redirect(url_for('legislation.view_statements'))

        # Create a zip file if follow-up letter exists
        if statement.follow_up_letter:
            from zipfile import ZipFile
            from io import BytesIO
            
            # Create a bytes buffer for the zip file
            buffer = BytesIO()
            with ZipFile(buffer, 'w') as zip_file:
                # Add the statement document to the zip file
                buffer_document = BytesIO(statement.document)
                zip_file.writestr(statement.filename, buffer_document.getvalue())
                
                # Add the follow-up letter to the zip file
                buffer_follow_up_letter = BytesIO(statement.follow_up_letter)
                zip_file.writestr('follow_up_letter_' + statement.filename, buffer_follow_up_letter.getvalue())
                
            buffer.seek(0)
            return send_file(buffer, as_attachment=True, download_name=f'statement_{statement_id}.zip')

        # If no follow-up letter, just send the statement document
        return send_file(BytesIO(statement.document), as_attachment=True, download_name=statement.filename)

    except SQLAlchemyError as e:
        logging.error(f"An SQLAlchemy error occurred: {e}")
        flash(f'An error occurred while downloading the statement: {e}', 'error')
        return redirect(url_for('legislation.view_statements'))

    except Exception as e:
        logging.error(f"An error occurred: {e}")
        flash(f'An error occurred while downloading the statement: {e}', 'error')
        return redirect(url_for('legislation.view_statements'))

#route for downloading question document
@legislation_bp.route('/download_question/<int:question_id>/<string:document_type>', methods=['GET'])
def download_question(question_id, document_type):
    """ Route to download a question document"""
    try:
        question = db_storage.get(Questions, id=question_id)
        if not question:
            flash(f'Question with ID {question_id} not found.', 'error')
            return redirect(url_for('legislation.view_questions'))

        if document_type == 'document':
            if not question.document:
                flash(f'No document available for question with ID {question_id}.', 'error')
                return redirect(url_for('legislation.view_questions'))
            return send_file(BytesIO(question.document), as_attachment=True, download_name=question.filename)
        elif document_type == 'follow_up_document':
            if not question.follow_up_document:
                flash(f'No follow-up document available for question with ID {question_id}.', 'error')
                return redirect(url_for('legislation.view_questions'))
            return send_file(BytesIO(question.follow_up_document), as_attachment=True, download_name=question.follow_up_filename)
        else:
            flash(f'Invalid document type: {document_type}.', 'error')
            return redirect(url_for('legislation.view_questions'))

    except SQLAlchemyError as e:
        logging.error(f"An SQLAlchemy error occurred: {e}")
        flash(f'An error occurred while downloading the question: {e}', 'error')
        return redirect(url_for('legislation.view_questions'))

    except Exception as e:
        logging.error(f"An error occurred: {e}")
        flash(f'An error occurred while downloading the question: {e}', 'error')
        return redirect(url_for('legislation.view_questions'))


#route for downloading follow up letter
@legislation_bp.route('/download_follow_up_letter/<int:statement_id>', methods=['GET'])
def download_follow_up_letter(statement_id):
    """ Route to download a statement follow-up letter """
    try:
        statement = db_storage.get(Statements, id=statement_id)
        if not statement:
            flash(f'Statement with ID {statement_id} not found.', 'error')
            return redirect(url_for('legislation.view_statements'))

        if not statement.follow_up_letter:
            flash(f'No follow-up letter available for statement with ID {statement_id}.', 'error')
            return redirect(url_for('legislation.view_statements'))

        return send_file(BytesIO(statement.follow_up_letter), as_attachment=True, download_name='follow_up_letter_' + statement.filename)

    except SQLAlchemyError as e:
        logging.error(f"An SQLAlchemy error occurred: {e}")
        flash(f'An error occurred while downloading the follow-up letter: {e}', 'error')
        return redirect(url_for('legislation.view_statements'))

    except Exception as e:
        logging.error(f"An error occurred: {e}")
        flash(f'An error occurred while downloading the follow-up letter: {e}', 'error')
        return redirect(url_for('legislation.view_statements'))
