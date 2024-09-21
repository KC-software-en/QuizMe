:: https://www.tutorialspoint.com/batch_script/batch_script_operators.htm
:: manage the scope of environment variable changes
:: start the localisation of environment changes. 
:: changes to environment variables made after this command are local to the batch file.
setlocal

:: initialise a flag variable to track the success of all commands
set success=1

:: go to the directory that contains manage.py
cd /d %~dp0 

:: run migrations for the database
:: write custom error messages for debugging
:: set the success variable to 0 if the command fails
python manage.py makemigrations
if %errorlevel% neq 0 (
    echo Error: Failed to run makemigrations
    set success=0
)
python manage.py migrate
if %errorlevel% neq 0 (
    echo Error: Failed to run migrate
    set success=0
)

:: Run SQL for specific migrations
python manage.py sqlmigrate Education 0001
if %errorlevel% neq 0 (
    echo Error: Failed to run sqlmigrate Education 0001
    set success=0
)
python manage.py sqlmigrate Entertainment 0001
if %errorlevel% neq 0 (
    echo Error: Failed to run sqlmigrate Entertainment 0001
    set success=0
)
python manage.py sqlmigrate General_Knowledge 0001
if %errorlevel% neq 0 (
    echo Error: Failed to run sqlmigrate General_Knowledge 0001
    set success=0
)

:: migrate again
python manage.py migrate
if %errorlevel% neq 0 (
    echo Error: Failed to run migrate again
    set success=0
)

:: create an admin user for the database
python manage.py createsuperuser
if %errorlevel% neq 0 (
    echo Error: Failed to create a superuser
    set success=0
)

:: populate the database with the quiz question objects for each subcategory
python manage.py create_mythology_objects 20 Mythology
if %errorlevel% neq 0 (
    echo Error: Failed to populate Mythology objects
    set success=0
)
python manage.py create_science_and_nature_objects 17 "Science & Nature"
if %errorlevel% neq 0 (
    echo Error: Failed to populate Science & Nature objects
    set success=0
)
python manage.py create_history_objects 23 History
if %errorlevel% neq 0 (
    echo Error: Failed to populate History objects
    set success=0
)

python manage.py create_film_objects 11 Film
if %errorlevel% neq 0 (
    echo Error: Failed to populate Film objects
    set success=0
)

:: check if all the commands were successful
if %success% equ 1 (
    echo Success, all commmands were executed!
) else (
    echo One or more commands failed to execute
)

:: let user view the output
pause

:: end the localisation started by setlocal. 
:: this restores the environment variables to their values before the corresponding setlocal command was executed
endlocal