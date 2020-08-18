# Permit Plan Form
http://192.168.103.131:8200
Username and Password are in the config file located on 192.168.103.131 VM

## Project Outline

This application serves two purposes:

1.	A form that enables the examiner to enter information about a plan approval:
    - AP Number(s)
    - Package Type: Roll/ Flat
    - Location: Bins/ Large Plan/ Zoning/ Electrical/ Plumbing
    - Number of Sheets

2.	A search form that enables the service rep to search a database by AP number and retrieve necessary data:
    - Permit Information:
        - Address
        - AP Type/Permit Description
        - Examiner who approved the application
        - Date Advanced to Plans Reviewed Stage
    - Plan Information:
        - Package (from App)
        - Location (from App)
        - Number of Sheets (from Hansen App tab)
        - Comments

The data repository used for this form is stored in the following tables on PERMITP: eclipse_plan_app_plan, eclipse_plan_app_permit, and eclipse_plan_app_plan_permit. Combined data from Eclipse and Hansen is ETL'd into eclipse_plan_app_permit nightly through the use of a scheduled process (see the etl folder).

Some historical notes:
As of 9/19/2019 becuause of issues running the query this ETL process was split into two parts -- first the data from Hansen is loaded into an MVW on GISLNI via our standard MVW refresh process; and then second the etl script in this repo updates plan_app_permit by joining the data from that MVW to lni_addr. On 1/14/20 we started using a separate database just for this app -- PERMITP.

## Installation
```bash
$ pip install -r requirements.txt
```
- Get the config.py file from me and put it in your base project directory
- Make sure li_dbs is either in this same directory or in your Python\Lib\site-packages folder.

### ETL
```bash
$ python etl/main.py
```

### Development Web Server
```bash
$ export FLASK_APP=li_permit_plan_form
$ export FLASK_ENV=development
$ flask run
```

### Production Web Server
```bash
$ export FLASK_APP=wsgi
$ flask run
```
