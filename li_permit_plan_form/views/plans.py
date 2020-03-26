from flask import (
    Blueprint, render_template, flash, redirect, url_for, request
)

from li_permit_plan_form.auth import auth
from li_permit_plan_form.db import (
    get_all_plans, delete_plan, get_permit_address, get_plan_from_id, 
    get_all_apnos_associated_with_plan, update_plan, update_plan_permits
)


bp = Blueprint('plans', __name__)

@bp.route('/plans')
@auth.login_required
def plans():
    # Get all the plans
    plans = get_all_plans()

    return render_template('plans.html', plans=plans)


@bp.route('/delete/<int:plan_id>', methods=['POST'])
@auth.login_required
def delete(plan_id):
    # Try to delete the plan
    try:
        delete_plan(plan_id)
        # Flash a success message if it works
        success = f'You have successfully deleted Plan {plan_id}'
        flash(success)
    # Flash an error message if it doesn't work
    except:
        error = 'Something went wrong. Please contact LI GIS Team'
        flash(error)
    return redirect(url_for('plans.plans'))

@bp.route('/edit/<int:plan_id>', methods=['GET', 'POST'])
@auth.login_required
def edit(plan_id):
    if request.method == 'POST':
        # Validate the apnos
        apnos = request.form.getlist('apno-input')
        
        for apno in apnos:

            # If a permit with a valid apno doesn't exist, take the user back to the form and flash a message.
            permit_address = get_permit_address(apno)
            if permit_address is False:
                error = f'{apno} is not a valid AP or Permit Number.'
                flash(error)
                plan = get_plan_from_id(plan_id)
                apnos = get_all_apnos_associated_with_plan(plan_id)
                return render_template('edit.html', plan=plan, apnos=apnos)

            # If a permit with a valid apno exists but no address was found, take the user back to the form and flash a message.
            elif permit_address is None:
                error = f'{apno} exists in Hansen or eCLIPSE, but no address was found. Please contact LI GIS Team.'
                flash(error)
                plan = get_plan_from_id(plan_id)
                apnos = get_all_apnos_associated_with_plan(plan_id)
                return render_template('edit.html', plan=plan, apnos=apnos)

        # Get input from the form
        package = request.form.get('package-input')
        location = request.form.get('location-input')
        comments = request.form.get('comments-input')

        # Update the plan
        update_plan(plan_id, package, location, comments)

        # Update the plan_permits
        update_plan_permits(plan_id, apnos)

        # Go back to the plans page when submitted and display a success message
        success = 'Your edit was successful.'
        flash(success)
        return redirect(url_for('plans.plans'))

    # Get the plan
    plan = get_plan_from_id(plan_id)

    # Get all the apnos
    apnos = get_all_apnos_associated_with_plan(plan_id)

    return render_template('edit.html', plan=plan, apnos=apnos)