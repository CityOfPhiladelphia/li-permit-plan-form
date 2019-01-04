from flask import (
    Blueprint, request, session, render_template, flash, redirect, url_for
)

from .db import get_permit_address, insert_plan, insert_plan_permit


bp = Blueprint('form', __name__)

@bp.route('/form', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':

        # Create a dictionary to store apnos and their associated addresses
        apno_dict = {}

        # Validate the apnos
        for apno in request.form.getlist('apno-input'):

            # If a permit with a valid apno doesn't exist, take the user back to the form and flash a message.
            permit_address = get_permit_address(apno)
            if permit_address is False:
                error = f'{apno} is not a valid AP Number.'
                flash(error)
                return render_template('form.html')

            # If a permit with a valid apno exists but no address was found, take the user back to the form and flash a message.
            elif permit_address is None:
                error = f'{apno} exists in Hansen, but no address was found. \n If the address was created today please ignore this error and submit this form. If not, please contact the LI GIS TEAM.'
                flash(error)

            # If it does exist, store the permit address in the dictionary
            apno_dict[apno] = permit_address

        # Get data from form and store it in a session
        session['apnos'] = apno_dict
        session['package'] = request.form.get('package-input')
        session['location'] = request.form.get('location-input')
        session['comments'] = request.form.get('comments-input')

        # Load the confirmation page
        return render_template('confirm.html')

    return render_template('form.html')

@bp.route('/confirm', methods=['GET', 'POST'])
def confirm():
    # Don't let users view or submit this page if they don't have session data
    if session['apnos'] is None:
        return render_template('form.html')

    if request.method == 'POST': 

        # Insert the plan into the plan table
        insert_plan(session['package'], session['location'], session['comments'])

        # Insert the apnos and plan data into the plan_permit table in the database
        # to associate each apno with a plan and permit
        for apno, address in session['apnos'].items():
            insert_plan_permit(apno)

        # Clear the session
        session.clear()
        success = 'The plan was successfully entered.'
        flash(success)
        return redirect(url_for('form.form'))
    
    return render_template('confirm.html')