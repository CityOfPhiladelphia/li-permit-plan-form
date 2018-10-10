# Permit Plan Form

## Project Goals

This application serves two purposes:

1.	A form that would enable the examiner to enter information about a plan approval:
    - AP Number
    - Package: Roll/ Flat
    - Location: Bins/ Large Plan/ Zoning/ Electrical/ Plumbing
    - Number of Sheets
    - Multiple Apps: Y/N
        - If Y: Enter additional AP Numbers

2.	A search form that would enable the service rep to search database by AP number and retrieve necessary data:
    - Address (from Hansen)
    - AP Type (from Hansen)
    - Package (from App)
    - Location (from App)
    - Multiple Apps Y/N (from App)
        - List of Additional Apps (from APP)
    - Examiner (from Hansen Review Tab)
    - Date Advanced to Plans Reviewed Stage (from Hansen Back-End)
    - Number of Sheets (from Hansen App tab)

## How it works

### Plan Entry Form
- The user enters AP Numbers and the corresponding address is loaded under the AP number field (using AJAX) for the user to validate.
- The user completes the rest of the form and submits it. This information is inserted into a table in GISLICLD.

### Plan Search Form
- The user enters an AP Number and the fields above are loaded into a table for the user to see. The data will be pulled from the same table in GISLICLD noted above.