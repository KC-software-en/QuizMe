:: manage the scope of environment variable changes
:: start the localisation of environment changes. 
:: changes to environment variables made after this command are local to the batch file.
setlocal

:: go to the directory that contains manage.py
cd /d %~dp0 

:: run migrations for the database
:: write custom error messages for debugging
python manage.py makemigrations
if %errorlevel% neq 0 (
    echo Error: Failed to run makemigrations
)
python manage.py migrate
if %errorlevel% neq 0 (
    echo Error: Failed to run migrate
)

:: Run SQL for specific migrations
python manage.py sqlmigrate Education 0001
if %errorlevel% neq 0 (
    echo Error: Failed to run sqlmigrate Education 0001
)
python manage.py sqlmigrate Entertainment 0001
if %errorlevel% neq 0 (
    echo Error: Failed to run sqlmigrate Entertainment 0001
)
python manage.py sqlmigrate General_Knowledge 0001
if %errorlevel% neq 0 (
    echo Error: Failed to run sqlmigrate General_Knowledge 0001
)

:: migrate again
python manage.py migrate
if %errorlevel% neq 0 (
    echo Error: Failed to run migrate again
)

:: create an admin user for the database
python manage.py createsuperuser
if %errorlevel% neq 0 (
    echo Error: Failed to create a superuser
)

:: populate the database with the quiz question objects for each subcategory
python manage.py create_mythology_objects 20 Mythology
if %errorlevel% neq 0 (
    echo Error: Failed to populate Mythology objects
)
python manage.py create_science_and_nature_objects 17 "Science & Nature"
if %errorlevel% neq 0 (
    echo Error: Failed to populate Science & Nature objects
)
python manage.py create_history_objects 23 History
if %errorlevel% neq 0 (
    echo Error: Failed to populate History objects
)

:: let user view the output
pause

:: end the localisation started by setlocal. 
:: this restores the environment variables to their values before the corresponding setlocal command was executed
endlocal