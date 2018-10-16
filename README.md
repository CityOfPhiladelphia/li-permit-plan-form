# Permit Plan Form

## Project Outline

This application serves two purposes:

1.	A form that enables the examiner to enter information about a plan approval:
    - AP Number(s)
    - Package Type: Roll/ Flat
    - Location: Bins/ Large Plan/ Zoning/ Electrical/ Plumbing
    - Number of Sheets

2.	A search form that enables the service rep to search a database by AP number and retrieve necessary data:
    - Permit Information:
        - Address (from Hansen)
        - AP Type (from Hansen)
        - Examiner (from Hansen Review Tab)
        - Date Advanced to Plans Reviewed Stage (from Hansen Back-End)
    - Plan Information:
        - Package (from App)
        - Location (from App)
        - Number of Sheets (from Hansen App tab)
        - Other AP numbers that are associated with this plan

The data repository used for this form is stored in the following tables on GISLICLD: plan_app_plan, plan_app_permit, and plan_app_plan_permit. Data from Hansen is ETL'd into plan_app_permit nightly through the use of a scheduled process that runs etl/main.py

## Usage
pip install -r requirements.txt

Get the config.py file from one of us containing username and passwords and put it in your li-permit-plan-form directory. Make sure li_dbs is either in this same directory or in your Python\Lib\site-packages folder.

Run app.py