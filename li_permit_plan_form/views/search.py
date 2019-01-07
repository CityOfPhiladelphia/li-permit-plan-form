from flask import Blueprint, request, render_template, flash

from li_permit_plan_form.db import get_permit, get_plans, get_apnos_associated_with_plan


bp = Blueprint('search', __name__)

@bp.route('/search', methods=['GET', 'POST'])
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