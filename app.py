from flask import Flask, request, flash, render_template, jsonify

from config import SECRET_KEY
from db import close_db, get_permit, get_plans, insert_plan, validate_apno, insert_plan_permit 
from auth import requires_auth
# from gevent.pywsgi import WSGIServer

app = Flask(__name__)
# Close the database when the app shuts down
app.teardown_appcontext(close_db)
app.secret_key = SECRET_KEY

@requires_auth
@app.route('/')
def index():
    return render_template('index.html')

@requires_auth
@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        
        error = None
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
        
        return render_template('search.html', permit=permit, plans=plans)
    
    return render_template('search.html')

@requires_auth
@app.route('/form', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':

        # Get data from form
        apnos = request.form.getlist('apno-input')
        package = request.form.get('package-input')
        location = request.form.get('location-input')
        sheetno = request.form.get('sheet-number-input')

        # Insert the plan into the plan table
        insert_plan(package, location, sheetno)

        # For each apno, try to insert the apno andplan data into the plan_permit table in the database
        # to associate each apno with a plan and permit
        for apno in apnos:
            # First, make sure the apno is valid
            if validate_apno(apno):
                insert_plan_permit(apno)
                
                success = f'The plan for AP Number {apno} was successfully entered.'
                flash(success)
            # Flash an error message when an invalid AP Number is inputed.
            else: 
                error = f'{apno} is not a valid AP Number. Please try again.'
                flash(error)

    return render_template('form.html')

    

# if __name__ == '__main__':
#     http_server = WSGIServer(('0.0.0.0', 8100), app)
#     http_server.serve_forever()