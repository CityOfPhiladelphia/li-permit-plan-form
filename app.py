from flask import Flask, request, flash, render_template
from config import SECRET_KEY
from db import close_db, get_permit, insert_plan
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
            error = 'An error has occurred. Please try again later or contact LI GIS Team if the error permits.'
            flash(error)
            return render_template('search.html')

        if permit is None:
            error = 'Please enter a valid AP Number.'
            flash(error)
            return render_template('search.html')

        elif len(permit) == 0:
            error = 'No results found for that AP Number.'
            flash(error)
            return render_template('search.html') 
        
        return render_template('search.html', permit=permit)
    
    return render_template('search.html')

@requires_auth
@app.route('/form', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        #error = None
        apno = request.form.get('apno-input')
        #multipleapplications = request.form.get('multipleapps-input')
        package = request.form.get('package-input')
        location = request.form.get('location-input')
        sheetno = request.form.get('sheet-number-input')
        insert_plan(apno, package, location, sheetno)
        
    return render_template('form.html')

    

# if __name__ == '__main__':
#     http_server = WSGIServer(('0.0.0.0', 8100), app)
#     http_server.serve_forever()