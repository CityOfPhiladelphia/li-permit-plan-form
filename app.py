from flask import Flask, request, flash, render_template, jsonify, session, redirect, url_for
from flask_httpauth import HTTPDigestAuth
from gevent.pywsgi import WSGIServer

from config import SECRET_KEY, users
from db import (close_db, get_permit, get_plans, insert_plan, 
                get_permit_address, insert_plan_permit, get_apnos_associated_with_plan)

app = Flask(__name__)
# Close the database when the app shuts down
app.teardown_appcontext(close_db)
app.secret_key = SECRET_KEY
auth = HTTPDigestAuth()

@auth.get_password
def get_pw(username):
    if username in users:
        return users.get(username)
    return None

@app.route('/')
@auth.login_required
def index():
    return render_template('index.html')

@app.route('/search', methods=['GET', 'POST'])
@auth.login_required
def search():
    if request.method == 'POST':
        
        apno = request.form.get('apno-form')

        # Flash a message when something unexpected occurs
        try:
            permit = get_permit(apno)
        except:
            error = 'An error has occurred. Please try again later or contact LI GIS Team if the error persists.'
            flash(error)
            return render_template('search.html')

        # Flash a message when an invalid AP Number is entered
        if permit is None:
            error = 'Please enter a valid AP Number.'
            flash(error)
            return render_template('search.html')

        # Flash a message when no results are found for that AP Number
        elif len(permit) == 0:
            error = 'No permit was found for that AP Number.'
            flash(error)
            return render_template('search.html')

        # Flash a message when something unexpected occurs
        try:
            plans = get_plans(apno)
        except:
            error = 'An error has occurred. Please try again later or contact LI GIS Team if the error persists.'
            flash(error)
            return render_template('search.html', permit=permit)

        # Flash a message when no plans are found for that AP Number
        if len(plans) == 0:
            error = 'No plans were found for that AP Number.'
            flash(error)
            return render_template('search.html', permit=permit)

        # Create a list to store plans
        plan_list = []

        for plan in plans:
            # Create a dictionary to store plan information
            plan_dict = {}
            plan_dict['id'] = plan.plan_id
            plan_dict['package'] = plan.package
            plan_dict['location'] = plan.location
            plan_dict['sheetno'] = plan.sheetno
            plan_dict['comments'] = plan.comments
            plan_dict['apnos'] = get_apnos_associated_with_plan(plan.plan_id, apno)
            plan_list.append(plan_dict)
        
        return render_template('search.html', permit=permit, plans=plan_list)
    
    return render_template('search.html')

@app.route('/form', methods=['GET', 'POST'])
@auth.login_required
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
            # If it does exist, store the permit address in the dictionary
            apno_dict[apno] = permit_address

        # Get data from form and store it in a session
        session['apnos'] = apno_dict
        session['package'] = request.form.get('package-input')
        session['location'] = request.form.get('location-input')
        session['sheetno'] = request.form.get('sheet-number-input')
        session['comments'] = request.form.get('comments-input')

        # Load the confirmation page
        return render_template('confirm.html')

    return render_template('form.html')

@app.route('/confirm', methods=['GET', 'POST'])
@auth.login_required
def confirm():
    # Don't let users view or submit this page if they don't have session data
    if session['apnos'] is None:
        return render_template('form.html')

    if request.method == 'POST': 

        # Insert the plan into the plan table
        insert_plan(session['package'], session['location'], session['sheetno'], session['comments'])

        # Insert the apnos and plan data into the plan_permit table in the database
        # to associate each apno with a plan and permit
        for apno, address in session['apnos'].items():
            insert_plan_permit(apno)

        # Clear the session
        session.clear()
        success = f'The plan was successfully entered.'
        flash(success)
        return redirect(url_for('form'))
    
    return render_template('confirm.html')
    

if __name__ == '__main__':
    http_server = WSGIServer(('0.0.0.0', 8200), app)
    http_server.serve_forever()