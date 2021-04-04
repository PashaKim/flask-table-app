pip install virtualenv > logs/install_venv_log.txt
if exist venv/ (
   echo venv exist 
) else (
   echo venv not exist 
   py -m virtualenv venv > logs/create_venv_log.txt
)
call venv\Scripts\activate.bat
pip install -r requirements.txt
flask run

or use start.bat